from rest_framework import serializers
from inmuebleslist_app.models import Inmueble

class InmuebleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    direccion = serializers.CharField()
    pais = serializers.CharField()
    descripcion = serializers.CharField()
    imagen = serializers.CharField()
    active = serializers.BooleanField()
    
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
    
    
"""
# DRF nos ofrece algo llamado ModelSerializer que te permite simplificar el mapeo de los campos, seteo de campos para auditoria,
# el manejo de las funciones create y update, etc. Es recomedable usar esto si el mapeo de los campos va dirigido a un solo modelo,
# pero si se trata de un formulario cuyos inputs reciben datos por ejemplo para dos modelos (cliente, usuario), es mejor
# usar el Serializer convencional.
# 
# Al usar el ModelSerializer aplicas el principio DRY (Don't Repeat Yourself) que significa "no te repitas" es util, pero solo si
# la logica a manejar no es compleja

from rest_framework import serializers
from inmuebleslist_app.models import Inmueble

class InmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmueble
        fields = ['id', 'direccion', 'pais', 'descripcion', 'imagen', 'active']
        read_only_fields = ['id']
"""