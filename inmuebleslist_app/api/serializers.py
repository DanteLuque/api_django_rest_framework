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