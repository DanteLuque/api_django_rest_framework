#from django.db import IntegrityError
#from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework.views import APIView

from inmuebleslist_app.models import Edificacion, Empresa
from inmuebleslist_app.api.serializers import EdificacionSerializer, EmpresaSerializer

'''
CBV (APIView)
Más estructurado.
Puedes definir métodos get, post, put, patch, delete dentro de la misma clase.
Fácil de extender y reutilizar con herencia.
DRF además ofrece atajos sobre esto (GenericAPIView, ModelViewSet, etc.) para CRUDs más rápidos.
'''

class EmpresaAVList(APIView):
    def get(self, req):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)
    
    def post(self, req):
        serializer = EmpresaSerializer(data=req.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        else:
            Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

class EdificacionList(APIView):
    def get(self, request):
        edificaciones = Edificacion.objects.all()
        serializer = EdificacionSerializer(edificaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EdificacionDetail(APIView):
    def get_object_by_pk(self, pk): #funcion personalizada, esto no le pertenece a APIView
        try:
            return Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return None

    def get(self, request, pk):
        inmueble = self.get_object_by_pk(pk)
        if not inmueble:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EdificacionSerializer(inmueble)
        return Response(serializer.data)

    def put(self, request, pk):
        inmueble = self.get_object_by_pk(pk)
        if not inmueble:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EdificacionSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inmueble = self.get_object_by_pk(pk)
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
def edificaciones_list(req):
    edificaciones = Edificacion.objects.all()
    # many indica que devolvera varios items
    serializer = EdificacionSerializer(edificaciones, many=True)
    return Response(serializer.data)



@api_view()
def edificaciones_detail(req, id):
    inmueble = get_object_or_404(Edificacion, pk=id) # este shorcut hace lo mismo que el try/except pero aqui el msg es generico
    serializer = EdificacionSerializer(inmueble)
    return Response(serializer.data)

# Asi es como se ve sin el shortcut
#@api_view()
#def edificaciones_detail(req, id):
#    try:
#        inmueble = Edificacion.objects.get(pk=id)
#        serializer = EdificacionSerializer(inmueble)
#        return Response(serializer.data)
#    except Edificacion.DoesNotExist:
#        return Response(
#            {"error": "Edificacion no encontrado"},
#            status=status.HTTP_404_NOT_FOUND
#        )


@api_view(['POST'])
def add_inmueble(req):
    # si no pasa una instancia, save() llama a create(), caso contrario, update()
    serializer = EdificacionSerializer(data=req.data)
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
        inmueble = Edificacion.objects.get(pk=id)
    except Edificacion.DoesNotExist:
        return Response(
            {"error": "Edificacion no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = EdificacionSerializer(inmueble, data=req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_inmueble(req, id):  
    try:
        inmueble = Edificacion.objects.get(pk=id)
        inmueble.delete()
    except Edificacion.DoesNotExist:
        return Response(
            {"error": "Edificacion no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(status=status.HTTP_204_NO_CONTENT)
'''