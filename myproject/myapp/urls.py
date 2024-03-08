

from django.urls import path
from .views import *

urlpatterns = [
    path("",index),
    path('add/', AddPersonAPIView.as_view(), name='add_person_api'),
    path('update/<str:person_id>/', UpdatePersonAPIView.as_view(), name='update_person_api'),
    path('delete/<str:person_id>/', DeletePersonAPIView.as_view(), name='delete_person_api'),
    path('get/<str:person_id>/', GetPersonAPIView.as_view(), name='get_person_api'),
    # path('add/',add_person),
    # path('show/', get_all_person)
    
]
