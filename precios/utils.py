import pandas as pd

def cambiar_precios(df, nombre=None, exclude=None, precio=None, costo=None, mayor=None, menor=None):
    if nombre:
        new_df = ver(df, nombre, exclude, mayor, menor)
        code_list = []
        for codigo in new_df["Código"]:
            code_list.append(codigo)
        if costo:
            for codigo in new_df["Código"]:
                df.loc[df["Código"]==codigo, ["Precio de costo"]] = int(costo)
        if precio:
            for codigo in new_df["Código"]: 
                df.loc[df["Código"]==codigo, ["Valor de precio de venta"]] = int(precio)
    return df

    
def ver(df, nombre, exclude=None, mayor=None, menor=None):
    df = df[df["Nombre"].str.contains(nombre.upper())]
    if exclude:
        exclude = exclude.replace(" ", "")
        for word in exclude.split(","):
            df = df[df["Nombre"].str.contains(word.upper())==False]
    if mayor:
        df = df[df["Valor de precio de venta"]>=int(mayor)]
    if menor:
        df = df[df["Valor de precio de venta"]<=int(menor)]
    return df

def df_to_zip(df):
    codigos = df["Código"]
    nombres = df["Nombre"]
    precios = df["Valor de precio de venta"]
    costos = df["Precio de costo"]
    results = list(zip(codigos, nombres, precios, costos))
    return results

def corregir_precios(file):
    fin = open(file, "rt")
    fout = open("files\\Test", "wt")
    for line in fin:
        fout.write(line)
    fin.close()
    fout.close()
