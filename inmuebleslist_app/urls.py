from django.urls import path
from inmuebleslist_app.api import inmuebles_list
from inmuebleslist_app.api import inmuebles_detail

urlpatterns = [
    path('list/', inmuebles_list, name='inmueble-list'),
    path('<int:id>/', inmuebles_detail, name='inmueble-detail'),
]
