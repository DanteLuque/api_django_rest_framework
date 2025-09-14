from django.urls import path
from inmuebleslist_app.api.views import EdificacionList, EdificacionDetail, EmpresaAVList
#from inmuebleslist_app.api.api import inmuebles_list, inmuebles_detail, add_inmueble, edit_inmueble, delete_inmueble

urlpatterns = [
    path("", EdificacionList.as_view(), name="edificacion"),
    path("<int:pk>/", EdificacionDetail.as_view(), name="edificacion-detail"),
    path("empresa/", EmpresaAVList.as_view(), name='empresa'),
]


# urlpatterns = [
#     path('list/', inmuebles_list, name='inmueble-list'),
#     path('add/', add_inmueble, name='add-list'),
#     path('<int:id>/', inmuebles_detail, name='inmueble-detail'),
#     path('edit/<int:id>/', edit_inmueble, name='edit-inmueble'),
#     path('delete/<int:id>/', delete_inmueble, name='delete-inmueble'),
# ]
