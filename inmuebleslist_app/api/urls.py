from django.urls import path
from inmuebleslist_app.api.views import InmuebleList, InmuebleDetail
#from inmuebleslist_app.api.api import inmuebles_list, inmuebles_detail, add_inmueble, edit_inmueble, delete_inmueble

urlpatterns = [
    path("", InmuebleList.as_view(), name="inmueble-list"),
    path("<int:pk>/", InmuebleDetail.as_view(), name="inmueble-detail"),
]


# urlpatterns = [
#     path('list/', inmuebles_list, name='inmueble-list'),
#     path('add/', add_inmueble, name='add-list'),
#     path('<int:id>/', inmuebles_detail, name='inmueble-detail'),
#     path('edit/<int:id>/', edit_inmueble, name='edit-inmueble'),
#     path('delete/<int:id>/', delete_inmueble, name='delete-inmueble'),
# ]
