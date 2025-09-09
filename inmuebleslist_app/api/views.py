from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework.views import APIView

from inmuebleslist_app.models import Inmueble
from inmuebleslist_app.api.serializers import InmuebleSerializer

'''
CBV (APIView)
Más estructurado.
Puedes definir métodos get, post, put, patch, delete dentro de la misma clase.
Fácil de extender y reutilizar con herencia.
DRF además ofrece atajos sobre esto (GenericAPIView, ModelViewSet, etc.) para CRUDs más rápidos.
'''

class InmuebleList(APIView):
    def get(self, request):
        inmuebles = Inmueble.objects.all()
        serializer = InmuebleSerializer(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InmuebleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InmuebleDetail(APIView):
    def get_object_by_pk(self, pk):
        try:
            return Inmueble.objects.get(pk=pk)
        except Inmueble.DoesNotExist:
            return None

    def get(self, request, pk):
        inmueble = self.get_object_by_pk(pk)
        if not inmueble:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InmuebleSerializer(inmueble)
        return Response(serializer.data)

    def put(self, request, pk):
        inmueble = self.get_object_by_pk(pk)
        if not inmueble:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InmuebleSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inmueble = self.get_object(pk)
        if not inmueble:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        inmueble.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
(@api_view) son function-based views (FBV): funciones simples decoradas para soportar HTTP methods.
FBV (@api_view)
Más simple y rápido de escribir.
Ideal para endpoints pequeños o prototipos.
Pero si tu API crece, se puede volver repetitivo.


@api_view()  # por defecto, indicamos que es de tipo GET
def inmuebles_list(req):
    inmuebles = Inmueble.objects.all()
    # many indica que devolvera varios items
    serializer = InmuebleSerializer(inmuebles, many=True)
    return Response(serializer.data)



@api_view()
def inmuebles_detail(req, id):
    inmueble = get_object_or_404(Inmueble, pk=id) # este shorcut hace lo mismo que el try/except pero aqui el msg es generico
    serializer = InmuebleSerializer(inmueble)
    return Response(serializer.data)

# Asi es como se ve sin el shortcut
#@api_view()
#def inmuebles_detail(req, id):
#    try:
#        inmueble = Inmueble.objects.get(pk=id)
#        serializer = InmuebleSerializer(inmueble)
#        return Response(serializer.data)
#    except Inmueble.DoesNotExist:
#        return Response(
#            {"error": "Inmueble no encontrado"},
#            status=status.HTTP_404_NOT_FOUND
#        )


@api_view(['POST'])
def add_inmueble(req):
    # si no pasa una instancia, save() llama a create(), caso contrario, update()
    serializer = InmuebleSerializer(data=req.data)
    if serializer.is_valid():
        try:
            serializer.save()  # metodo para crear o actualizar
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(
                {"error": "Violación de integridad en BD", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors)


@api_view(['PATCH'])
def edit_inmueble(req, id):
    try:
        inmueble = Inmueble.objects.get(pk=id)
    except Inmueble.DoesNotExist:
        return Response(
            {"error": "Inmueble no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = InmuebleSerializer(inmueble, data=req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_inmueble(req, id):  
    try:
        inmueble = Inmueble.objects.get(pk=id)
        inmueble.delete()
    except Inmueble.DoesNotExist:
        return Response(
            {"error": "Inmueble no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(status=status.HTTP_204_NO_CONTENT)
'''