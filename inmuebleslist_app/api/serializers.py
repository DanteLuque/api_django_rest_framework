from rest_framework import serializers
from inmuebleslist_app.models import Inmueble

# Metodos personalizados para validacion
def min_length(min_len):
    def validacion(value):
        if len(value) < min_len:
            raise serializers.ValidationError(f"Debe tener al menos {min_len} caracteres")
    return validacion

def max_length(max_len):
    def validacion(value):
        if len(value) > max_len:
            raise serializers.ValidationError(f"Debe tener máximo {max_len} caracteres")
    return validacion    
    
def positiveValue(value):
    if value <= 0:
        raise serializers.ValidationError("El valor debe ser mayor a cero")

class InmuebleSerializer(serializers.Serializer):
    # Campos calculados (obteniendo la longitud de direccion)
    longitud_direccion = serializers.SerializerMethodField()
    
    id = serializers.IntegerField(read_only=True)
    direccion = serializers.CharField(validators=[min_length(3), max_length(255)])
    pais = serializers.CharField(validators=[min_length(3), max_length(70)])
    descripcion = serializers.CharField()
    precio = serializers.FloatField(validators=[positiveValue])
    imagen = serializers.CharField()
    active = serializers.BooleanField()
    
    def get_longitud_direccion(self, object):
        cantidad_caracteres = len(object.direccion)
        return cantidad_caracteres
    
    def create(self, validated_data):
        return Inmueble.objects.create(**validated_data) #desempaquetamos todo el diccionario y se lo pasamos al create
    
    def update(self, instancia ,validated_data):
        instancia.direccion = validated_data.get('direccion', instancia.direccion)
        instancia.pais = validated_data.get('pais', instancia.pais)
        instancia.descripcion = validated_data.get('descripcion', instancia.descripcion)
        instancia.imagen = validated_data.get('imagen', instancia.imagen)
        instancia.active = validated_data.get('active', instancia.active)
        instancia.save()
        return instancia
    
    # metodos hereados del serializers
    def validate(self, data):
        if data['direccion']==data['pais']:
            raise serializers.ValidationError("La direccion y el pais deben ser diferentes.")
        
    def validate_descripcion(self, data): #validate_ + el campo a validar
        if len(data) < 3:
            raise serializers.ValidationError("la descripcion debe tener más de 3 caracteres")
        
    def validate_empty_values(self, data):  
        return super().validate_empty_values(data)
    
"""
# DRF nos ofrece algo llamado ModelSerializer que te permite simplificar el mapeo de los campos, seteo de campos para auditoria,
# el manejo de las funciones create y update, etc. Es recomedable usar esto si el mapeo de los campos va dirigido a un solo modelo,
# pero si se trata de un formulario cuyos inputs reciben datos por ejemplo para dos modelos (cliente, usuario), es mejor
# usar el Serializer convencional.
# 
# Al usar el ModelSerializer aplicas el principio DRY (Don't Repeat Yourself) que significa "no te repitas" es util, pero solo si
# la logica a manejar no es compleja
# En los ModelSerializer ya no es necesario los metodos create y update

from rest_framework import serializers
from inmuebleslist_app.models import Inmueble

class InmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmueble
        # fields = "__all__" #esto es para mapear todos los campos, ya no habria necesidad de especificar todos
        # exclude = ['id'] # mapea todos los campos excepto los que vamos a excluir
        fields = ['id', 'direccion', 'pais', 'descripcion', 'imagen', 'active']
        read_only_fields = ['id']
"""