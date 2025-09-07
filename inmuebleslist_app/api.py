from inmuebleslist_app.models import Inmueble
from django.http import JsonResponse

def inmuebles_list(req):
    inmuebles = Inmueble.objects.all()
    data = {
        'inmuebles': list(inmuebles.values()) #parseamos los values de tipo diccionario a una lista
    }
    
    return JsonResponse(data) #parseamos la data a un json

def inmuebles_detail(req, id):
    inmueble = Inmueble.objects.get(pk=id)
    data = {
        'direccion': inmueble.direccion,
        'pais': inmueble.pais,
        'imagen': inmueble.imagen,
        'active': inmueble.active,
        'descripcion': inmueble.descripcion,
    }
    
    return JsonResponse(data)