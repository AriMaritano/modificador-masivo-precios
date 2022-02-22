from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.files.storage import default_storage
import pandas as pd
from .utils import *
from .models import File
from os import path, remove
from pathlib import Path


def ver_precios(req):
    results = None
    contains = None
    exclude = None
    last_file = None
    message = None
    mayor = None
    menor = None
    if len(File.objects.all()) > 0:
        last_file = File.objects.order_by('-date_uploaded')[0]
    if req.method == "POST":
        if 'file1' in req.FILES:
            file = req.FILES['file1']
            drive = pd.read_csv(file, encoding="utf-8", sep="~")
            new_file = File(file=file, filename=file.name)
            new_file.save()
            drive = drive[["Código", "Nombre", "Rubro", "Valor de precio de venta", "Precio de costo"]]
            last_file = new_file
        if last_file != None:
            if 'contains' in req.POST:
                if req.POST['contains'] != "":
                    drive = pd.read_csv(last_file.file, encoding="utf-8", sep="~")
                    drive = drive[["Código", "Nombre", "Rubro", "Valor de precio de venta", "Precio de costo"]]
                    contains = req.POST['contains']
                    if req.POST['exclude'] != "":
                        exclude = req.POST['exclude']
                    if req.POST['mayor'] != "" and req.POST['mayor'] != "None":
                        mayor = req.POST['mayor']
                    if req.POST['menor'] != "" and req.POST['menor'] != "None":
                        menor = req.POST['menor']
                    results = df_to_zip(ver(drive, contains, exclude, mayor, menor))
        else:
            message = "No se puede consultar sin archivo"
    context = {
        'file':last_file,
        'results':results,
        'contains':contains,
        'exclude':exclude,
        'message': message,
        'mayor':mayor,
        'menor':menor
    }
    return render(req, 'precios/ver_precios.html', context)


def ver_cambios(req):
    contains = None
    exclude = None
    precio = None
    costo = None
    mayor = None
    menor = None
    if req.method=="POST":
        if req.POST['contains'] != "" and req.POST['contains'] != "None":
            contains = req.POST['contains']
        if req.POST['exclude'] != "" and req.POST['exclude'] != "None":
            exclude = req.POST['exclude']
        if req.POST['mayor'] != "" and req.POST['mayor'] != "None":
            mayor = req.POST['mayor']
        if req.POST['menor'] != "" and req.POST['menor'] != "None":
            menor = req.POST['menor']
        if req.POST['precio'] != "" and req.POST['precio'] != "None":
            precio = req.POST['precio']
        if req.POST['costo'] != "" and req.POST['costo'] != "None":
            costo = req.POST['costo']
    last_file = File.objects.order_by('-date_uploaded')[0]
    df = pd.read_csv(last_file.file, encoding="utf-8", sep="~")
    new_df = cambiar_precios(df, contains, exclude, precio, costo, mayor, menor)
    print("New df: ", mayor, menor)
    results = df_to_zip(ver(new_df, contains, exclude, mayor, menor))
    context = {
        'results':results,
        'contains':contains,
        'exclude':exclude,
        'precio':precio,
        'costo':costo,
        'mayor':mayor,
        'menor':menor
        }
    return render(req, 'precios/cambiar_precios.html', context)


def guardar_cambios(req):
    contains = None
    exclude = None
    precio = None
    costo = None
    mayor = None
    menor = None
    if req.POST['contains'] != "" and req.POST['contains'] != "None":
        contains = req.POST['contains']
    if req.POST['exclude'] != "" and req.POST['exclude'] != "None":
        exclude = req.POST['exclude']
    if req.POST['precio'] != "" and req.POST['precio'] != "None":
        precio = req.POST['precio']
    if req.POST['costo'] != "" and req.POST['costo'] != "None":
        costo = req.POST['costo']
    if req.POST['mayor'] != "" and req.POST['mayor'] != "None":
        mayor = req.POST['mayor']
    if req.POST['menor'] != "" and req.POST['menor'] != "None":
        menor = req.POST['menor']
    last_file = File.objects.order_by('-date_uploaded')[0]
    df = pd.read_csv(last_file.file, encoding="utf-8", sep="~")
    new_prices = cambiar_precios(df, contains, exclude, precio, costo, mayor, menor)
    if '_edit' in last_file.filename:
        print("edit")
        filename = last_file.filename
        filepath = path.join(settings.MEDIA_ROOT, filename)
        new_prices.to_csv(filepath, sep="~", index=False, line_terminator="\r\n")
        last_file.file = filepath
        last_file.save()
    else:
        print("no edit")
        filename = last_file.filename[:-4]+"_edit.txt"
        filepath = path.join(settings.MEDIA_ROOT, filename)
        new_prices.to_csv(filepath, sep="~", index=False, line_terminator="\r\n")
        new_file = File(file=filepath, filename=filename)
        new_file.save()
    return redirect('ver_precios')



def show_files(req):
    files = File.objects.all()
    context = {
        'files':files
    }
    return render(req, 'precios/files.html', context)


def delete_files(req):
    if req.method == "POST":
        file_id = req.POST['id']
        file = File.objects.get(id=file_id)
        file.delete()
        filepath = file.file.path
        remove(filepath)
    context = {
    }
    return redirect('show_files')



def download(request): #path
    if len(File.objects.all()) > 0:
        filepath = File.objects.order_by('-date_uploaded')[0].file.path
        if path.exists(filepath):
            with open(filepath, 'rb') as file:
                response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + path.basename(filepath)
                return response
    raise Http404