from django.urls import path
from . import views

urlpatterns = [
    path("", views.ver_precios, name="ver_precios"),
    path("ver-cambios", views.ver_cambios, name="ver_cambios"),
    path("guardar-cambios", views.guardar_cambios, name="guardar_cambios"),
    path("files", views.show_files, name="show_files"),
    path("delete-files", views.delete_files, name="delete_files"),
    path("download", views.download, name="download"),
]

