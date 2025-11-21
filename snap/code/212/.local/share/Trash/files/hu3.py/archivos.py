"""
modulo para manejo de archivos csv.
guardar y cargar inventario con validaciones.
"""

def guardarcsv(inventario, ruta, incluirheader=True):
    """
    guarda el inventario en un archivo csv.
    retorna true si se guardo correctamente, false si hubo error.
    """
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n⚠️  el inventario está vacío, no hay nada que guardar")
        return False
    
    try:
        # abrir archivo para escritura
        archivo = open(ruta, 'w', encoding='utf-8')
        
        # escribir encabezado
        if incluirheader:
            archivo.write("nombre,precio,cantidad\n")
        
        # escribir cada producto
        for producto in inventario:
            linea = f"{producto['nombre']},{producto['precio']},{producto['cantidad']}\n"
            archivo.write(linea)
        
        archivo.close()
        print(f"\n inventario guardado exitosamente en {ruta}")
        return True
    
    except PermissionError:
        print(f"\n error: no tienes permisos para escribir en '{ruta}'")
        return False
    
    except Exception as e:
        print(f"\n error al guardar el archivo: {e}")
        return False


def cargarcsv(ruta):
    """
    carga productos desde un archivo csv.
    retorna tupla: (listaproductos, filasinvalidas)
    """
    productos = []
    filasinvalidas = 0
    
    try:
        # abrir archivo para lectura
        archivo = open(ruta, 'r', encoding='utf-8')
        lineas = archivo.readlines()
        archivo.close()
        
        # validar que el archivo no este vacio
        if len(lineas) == 0:
            print("\n error, el archivo está vacío.")
            return ([], 0)
        
        # validar encabezado
        encabezado = lineas[0].strip()
        if encabezado != "nombre,precio,cantidad":
            print(f"\n error, Encabezado inválido.")
            print(f"   esperado, nombre,precio,cantidad")
            print(f"   encontrado {encabezado}")
            return ([], 0)
        
        # procesar cada linea de datos
        for numlinea in range(1, len(lineas)):
            linea = lineas[numlinea].strip()
            
            # saltar lineas vacias
            if linea == "":
                continue
            
            # dividir por comas
            partes = linea.split(',')
            
            # validar que tenga exactamente 3 columnas
            if len(partes) != 3:
                filasinvalidas += 1
                continue
            
            try:
                nombre = partes[0].strip()
                preciostr = partes[1].strip()
                cantidadstr = partes[2].strip()
                
                # validar que el nombre no este vacio
                if nombre == "":
                    filasinvalidas += 1
                    continue
                
                # convertir precio a float
                precio = float(preciostr)
                
                # convertir cantidad a int
                cantidad = int(cantidadstr)
                
                # validar que no sean negativos
                if precio < 0 or cantidad < 0:
                    filasinvalidas += 1
                    continue
                
                # agregar producto valido
                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "cantidad": cantidad
                })
            
            except ValueError:
                # error al convertir precio o cantidad
                filasinvalidas += 1
                continue
        
        return (productos, filasinvalidas)
    
    except FileNotFoundError:
        print(f"\n error,no se encontró el archivo '{ruta}'")
        return ([], 0)
    
    except UnicodeDecodeError:
        print(f"\n error, el archivo tiene problemas de codificación")
        return ([], 0)
    
    except Exception as e:
        print(f"\n error al cargar el archivo: {e}")
        return ([], 0)