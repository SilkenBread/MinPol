import os
import re
import json
import subprocess
from minizinc import Instance, Model, Solver, Driver
from typing import Dict, Any, Optional
import minizinc
import numpy as np


def convertir_a_dzn(ruta_archivo):
    try:
        # Leer el contenido del archivo
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()
        
        # Procesar el contenido del archivo
        n = int(lineas[0].strip())
        m = int(lineas[1].strip())
        p = list(map(int, lineas[2].strip().split(',')))
        v = list(map(float, lineas[3].strip().split(',')))
        ce = list(map(float, lineas[4].strip().split(',')))
        
        # Procesar la matriz C
        C = []
        for i in range(5, 5 + m):
            fila = list(map(float, lineas[i].strip().split(',')))
            C.append(fila)
        
        ct = float(lineas[5 + m].strip())
        MaxMovs = int(lineas[6 + m].strip())
        
        # Formatear el contenido al formato .dzn
        contenido_dzn = f"n = {n};\nm = {m};\n"
        contenido_dzn += f"p = {p};\n"
        contenido_dzn += f"v = {v};\n"
        contenido_dzn += f"ce = {ce};\n"
        contenido_dzn += "C = [| " + "\n| ".join([", ".join(map(str, fila)) for fila in C]) + " |];\n"
        contenido_dzn += f"ct = {ct};\nMaxMovs = {MaxMovs};\n"
        
        # Guardar el archivo en formato .dzn
        nombre_base = os.path.basename(os.path.splitext(ruta_archivo)[0])  
        ruta_directorio_dzn = os.path.join("data", "dzn")      
        os.makedirs(ruta_directorio_dzn, exist_ok=True)                    
        nombre_archivo_dzn = os.path.join(ruta_directorio_dzn, f"{nombre_base}.dzn")
        
        # Guardar el archivo en la nueva ruta
        with open(nombre_archivo_dzn, 'w') as f:
            f.write(contenido_dzn)
        
        return nombre_archivo_dzn # Devuelve la ruta del archivo convertido
        
    except Exception as e:
        raise RuntimeError(f"Error al procesar el archivo: {e}")

def leer_dzn(ruta_archivo_dzn):
    datos = {}
    with open(ruta_archivo_dzn, 'r') as archivo:
        contenido = archivo.read()
        
        # Buscar y almacenar las variables usando expresiones regulares
        datos['n'] = int(re.search(r'n\s*=\s*(\d+);', contenido).group(1))
        datos['m'] = int(re.search(r'm\s*=\s*(\d+);', contenido).group(1))
        
        datos['p'] = list(map(int, re.search(r'p\s*=\s*\[(.*?)\];', contenido).group(1).split(',')))
        datos['v'] = list(map(float, re.search(r'v\s*=\s*\[(.*?)\];', contenido).group(1).split(',')))
        datos['ce'] = list(map(float, re.search(r'ce\s*=\s*\[(.*?)\];', contenido).group(1).split(',')))
        
        
        
        datos['ct'] = float(re.search(r'ct\s*=\s*(\d+\.\d+);', contenido).group(1))
        datos['MaxMovs'] = int(re.search(r'MaxMovs\s*=\s*(\d+);', contenido).group(1))
    
    return datos

def parse_minizinc_result(resultado):
    """
    Parsea el resultado de MiniZinc y retorna un diccionario con los valores estructurados.
    
    Args:
        resultado: Objeto resultado de MiniZinc
        
    Returns:
        dict: Diccionario con todos los valores parseados
    """
    # Convertir el resultado a string para procesarlo
    resultado_str = str(resultado)
    
    # Diccionario para almacenar los resultados
    parsed_result = {}
    
    # Extraer matriz de movimientos
    matriz_pattern = r'\[\|(.*?)\|\]'
    matriz_match = re.search(matriz_pattern, resultado_str, re.DOTALL)
    if matriz_match:
        # Procesar la matriz
        matriz_str = matriz_match.group(1)
        # Dividir por filas y limpiar
        filas = [row.strip() for row in matriz_str.split('|')]
        # Convertir cada fila a lista de números
        matriz = []
        for fila in filas:
            numeros = [int(n) for n in fila.split(',')]
            matriz.append(numeros)
        parsed_result['matriz_movimientos'] = np.array(matriz)
    
    # Extraer distribución inicial
    dist_inicial_pattern = r'Distribución Inicial: \[(.*?)\]'
    dist_inicial_match = re.search(dist_inicial_pattern, resultado_str)
    if dist_inicial_match:
        dist_inicial = [int(x) for x in dist_inicial_match.group(1).split(',')]
        parsed_result['distribucion_inicial'] = dist_inicial
    
    # Extraer distribución final
    dist_final_pattern = r'Distribución Final: \[(.*?)\]'
    dist_final_match = re.search(dist_final_pattern, resultado_str)
    if dist_final_match:
        dist_final = [int(x) for x in dist_final_match.group(1).split(',')]
        parsed_result['distribucion_final'] = dist_final
    
    # Extraer acumulado
    acumulado_pattern = r'Acumulado: \[(.*?)\]'
    acumulado_match = re.search(acumulado_pattern, resultado_str)
    if acumulado_match:
        acumulado = [int(x) for x in acumulado_match.group(1).split(',')]
        parsed_result['acumulado'] = acumulado
    
    # Extraer mediana
    mediana_pattern = r'Mediana: ([\d.]+)'
    mediana_match = re.search(mediana_pattern, resultado_str)
    if mediana_match:
        parsed_result['mediana'] = float(mediana_match.group(1))
    
    # Extraer total de personas movidas
    personas_movidas_pattern = r'Total de personas movidas: (\d+)'
    personas_movidas_match = re.search(personas_movidas_pattern, resultado_str)
    if personas_movidas_match:
        parsed_result['total_personas_movidas'] = int(personas_movidas_match.group(1))
    
    # Extraer total de pasos realizados
    pasos_pattern = r'Total de pasos realizados: (\d+)'
    pasos_match = re.search(pasos_pattern, resultado_str)
    if pasos_match:
        parsed_result['total_pasos_realizados'] = int(pasos_match.group(1))
    
    # Extraer polarización
    polarizacion_pattern = r'Polarización: ([\d.]+)'
    polarizacion_match = re.search(polarizacion_pattern, resultado_str)
    if polarizacion_match:
        parsed_result['polarizacion'] = float(polarizacion_match.group(1))
    
    # Extraer costo total
    costo_pattern = r'Costo Total: ([\d.]+)'
    costo_match = re.search(costo_pattern, resultado_str)
    if costo_match:
        parsed_result['costo_total'] = float(costo_match.group(1))
    
    return parsed_result

def ejecutar_dzn(ruta_archivo_dzn: str):    
    # Cargar el modelo de MiniZinc
    modelo = Model("./Proyecto.mzn")
    
    # Cargar el archivo .dzn con los datos
    modelo.add_file(ruta_archivo_dzn)
    
    # Seleccionar el solver Gecode
    gecode = Solver.lookup("gecode")
    
    # Crear una instancia del modelo con el solver Gecode
    instancia = Instance(gecode, modelo)
    
    # Resolver el modelo
    resultado = instancia.solve()
    print(resultado)
    return parse_minizinc_result(resultado)
