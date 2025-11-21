"""
sistema de gestion de inventario
aplicacion principal con menu interactivo y validaciones completas.
"""

import servicios
import archivos

# inventario global (lista de diccionarios)
inventario = []


def mostrarmenu():
    """muestra el menu principal del sistema."""
    print("\n" + "="*50)
    print("        SISTEMA DE GESTIÓN DE INVENTARIO")
    print("="*50)
    print("  1. Agregar producto")
    print("  2. Mostrar inventario")
    print("  3. Buscar producto")
    print("  4. Actualizar producto")
    print("  5. Eliminar producto")
    print("  6. Ver estadísticas")
    print("  7. Guardar en CSV")
    print("  8. Cargar desde CSV")
    print("  9. Salir")
    print("="*50)


def validaropcionmenu():
    """valida que la opcion del menu sea un numero entre 1 y 9."""
    while True:
        try:
            opcion = input("\nSelecciona una opción (1-9): ").strip()
            
            # validar que no este vacio
            if opcion == "":
                print(" ingresa una opcion")
                continue
            
            # validar que sea un numero
            if not opcion.isdigit():
                print(" ingresa un número valido")
                continue
            
            # convertir a entero
            opcionnum = int(opcion)
            
            # validar rango
            if opcionnum < 1 or opcionnum > 9:
                print(" el numero tiene que estar entre 1 o 9")
                continue
            
            return opcionnum
        
        except Exception as e:
            print(f" error {e}")


def validartexto(mensaje):
    """valida entrada de texto (no vacio, sin caracteres especiales)."""
    while True:
        texto = input(mensaje).strip()
        
        # validar que no este vacio
        if texto == "":
            print(" este campo no puede estar vacio")
            continue
        
        # validar que no sea solo numeros
        if texto.isdigit():
            print("el nombre no pueden ser letras")
            continue
        
        # validar que no contenga comas (problema para csv)
        if ',' in texto:
            print("no puede contener comas")
            continue
        
        return texto


def validarprecio():
    """valida que el precio sea un numero positivo."""
    while True:
        try:
            precioinput = input("Precio: $").strip()
            
            # validar que no este vacio
            if precioinput == "":
                print("el precio no puede quedar vacio")
                continue
            
            # convertir a float
            precio = float(precioinput)
            
            # validar que sea positivo
            if precio <= 0:
                print(" el precio debe ser mayor a 0")
                continue
            
            return precio
        
        except ValueError:
            print(f"'{precioinput}' no es un número válido.")


def validarcantidad():
    """valida que la cantidad sea un numero entero no negativo."""
    while True:
        try:
            cantidadinput = input("Cantidad: ").strip()
            
            # validar que no este vacio
            if cantidadinput == "":
                print("la cantidad no puede estar vacia")
                continue
            
            # validar que sea solo digitos
            if not cantidadinput.isdigit():
                print(f" '{cantidadinput}' no es un número entero válido")
                continue
            
            # convertir a entero
            cantidad = int(cantidadinput)
            
            # validar que no sea negativo
            if cantidad <= 0:
                print(" la cantidad debe ser mayor a 0")
                continue
            
            return cantidad
        
        except ValueError:
            print(f"'{cantidadinput}' no es un número valido")


def validarprecioopcional():
    """valida precio opcional (puede estar vacio)."""
    while True:
        try:
            precioinput = input("Nuevo precio $").strip()
            
            # si esta vacio, retornar none
            if precioinput == "":
                return None
            
            # convertir a float
            precio = float(precioinput)
            
            # validar que sea positivo
            if precio <= 0:
                print("el precio debe ser mayor que 0")
                continue
            
            return precio
        
        except ValueError:
            print(f"'{precioinput}' no es un número válido.")


def validarcantidadopcional():
    """valida cantidad opcional (puede estar vacia)."""
    while True:
        try:
            cantidadinput = input("nueva cantidad").strip()
            
            # si esta vacio, retornar none
            if cantidadinput == "":
                return None
            
            # validar que sea solo digitos
            if not cantidadinput.isdigit():
                print(f"'{cantidadinput}' no es un número entero válido")
                continue
            
            # convertir a entero
            cantidad = int(cantidadinput)
            
            # validar que no sea negativo
            if cantidad < 0:
                print("la cantidad no puede ser negativa")
                continue
            
            return cantidad
        
        except ValueError:
            print(f" '{cantidadinput}' no es un número valido")


def validarconfirmacion(mensaje):
    """valida confirmacion s/n."""
    while True:
        respuesta = input(mensaje).strip().upper()
        
        if respuesta == "":
            print("debes responder S o N.")
            continue
        
        if respuesta in ['S', 'SI', 'N', 'NO']:
            return respuesta in ['S', 'SI']
        
        print("respuesta invalida ingresa S o N.")


def opcionagregar():
    """opcion 1: agregar producto."""
    print("\n--- AGREGAR PRODUCTO ---")
    
    try:
        nombre = validartexto("Nombre del producto: ")
        precio = validarprecio()
        cantidad = validarcantidad()
        
        if servicios.agregarproducto(inventario, nombre, precio, cantidad):
            print(f"\n '{nombre}' agregado exitosamente.")
        else:
            print(f"\n el producto '{nombre}' ya existe en el inventario.")
    
    except KeyboardInterrupt:
        print("\n operación cancelada")
    except Exception as e:
        print(f"\n error inesperado {e}")


def opcionmostrar():
    """opcion 2: mostrar inventario."""
    print("\n--- INVENTARIO COMPLETO ---")
    try:
        servicios.mostrarinventario(inventario)
    except Exception as e:
        print(f"\n error al mostrar inventario: {e}")


def opcionbuscar():
    """opcion 3: buscar producto."""
    print("\n--- BUSCAR PRODUCTO ---")
    
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n  el inventario está vacío, no hay productos para buscar")
        return
    
    try:
        nombre = validartexto("Nombre del producto a buscar: ")
        producto = servicios.buscarproducto(inventario, nombre)
        
        if producto is not None:
            print(f"\n Producto encontrado:")
            print(f"   Nombre: {producto['nombre']}")
            print(f"   Precio: ${producto['precio']:.2f}")
            print(f"   Cantidad: {producto['cantidad']} unidades")
            subtotal = producto['precio'] * producto['cantidad']
            print(f"   Subtotal: ${subtotal:.2f}")
        else:
            print(f"\n❌ No se encontró el producto '{nombre}'.")
    
    except KeyboardInterrupt:
        print("\n operación cancelada")
    except Exception as e:
        print(f"\n error inesperado: {e}")


def opcionactualizar():
    """opcion 4: actualizar producto."""
    print("\n--- ACTUALIZAR PRODUCTO ---")
    
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n el inventario está vacío, no hay productos para actualizar")
        return
    
    try:
        nombre = validartexto("nombre del producto a actualizar: ")
        
        # verificar que el producto exista
        producto = servicios.buscarproducto(inventario, nombre)
        if producto is None:
            print(f"\n no se encontró el producto '{nombre}'.")
            return
        
        # mostrar datos actuales
        print(f"\n datos actuales ")
        print(f"   Precio: ${producto['precio']:.2f}")
        print(f"   Cantidad: {producto['cantidad']} unidades")
        
        # pedir nuevos valores
        nuevoprecio = validarprecioopcional()
        nuevacantidad = validarcantidadopcional()
        
        # validar que al menos se haya ingresado un valor
        if nuevoprecio is None and nuevacantidad is None:
            print("\n no se actualizó ningún valor.")
            return
        
        # actualizar
        if servicios.actualizarproducto(inventario, nombre, nuevoprecio, nuevacantidad):
            print(f"\n✅ Producto '{nombre}' actualizado exitosamente.")
        else:
            print(f"\n❌ No se pudo actualizar el producto.")
    
    except KeyboardInterrupt:
        print("\n operación cancelada")
    except Exception as e:
        print(f"\n error inesperado: {e}")


def opcioneliminar():
    """opcion 5: eliminar producto."""
    print("\n--- ELIMINAR PRODUCTO ---")
    
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n  el inventario está vacío, no hay productos para eliminar")
        return
    
    try:
        nombre = validartexto("nombre del producto a eliminar ")
        
        # verificar que el producto exista
        if servicios.buscarproducto(inventario, nombre) is None:
            print(f"\n no se encontró el producto '{nombre}'.")
            return
        
        # confirmar eliminacion
        if validarconfirmacion(f"¿Estás seguro de eliminar '{nombre}'? (S/N): "):
            if servicios.eliminarproducto(inventario, nombre):
                print(f"\n producto '{nombre}' eliminado exitosamente.")
            else:
                print(f"\n no se pudo eliminar el producto")
        else:
            print("\n eliminación cancelada")
    
    except KeyboardInterrupt:
        print("\n  operación cancelada")
    except Exception as e:
        print(f"\n error inesperado {e}")


def opcionestadisticas():
    """opcion 6: ver estadisticas."""
    print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
    
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n el inventario está vacío, no hay estadísticas que mostrar")
        return
    
    try:
        # obtener estadisticas (retorna tupla)
        unidades, valor, mascaro, mayorstock = servicios.calcularestadisticas(inventario)
        
        print(f"\n📊 RESUMEN DEL INVENTARIO:")
        print(f"   • productos diferentes: {len(inventario)}")
        print(f"   • unidades totales: {unidades}")
        print(f"   • valor total: ${valor:.2f}")
        
        print(f"\n👑 PRODUCTO MÁS CARO:")
        print(f"   • nombre: {mascaro['nombre']}")
        print(f"   • precio: ${mascaro['precio']:.2f}")
        
        print(f"\n📦 PRODUCTO CON MAYOR STOCK:")
        print(f"   • nombre: {mayorstock['nombre']}")
        print(f"   • cantidad: {mayorstock['cantidad']} unidades")
    
    except Exception as e:
        print(f"\n error inesperado: {e}")


def opcionguardar():
    """opcion 7: guardar en csv."""
    print("\n--- GUARDAR EN CSV ---")
    
    # validar que el inventario no este vacio
    if len(inventario) == 0:
        print("\n el inventario está vacío. No hay nada que guardar.")
        return
    
    try:
        ruta = input("nombre del archivo, dale enter ").strip()
        
        if ruta == "":
            ruta = "inventario.csv"
        
        # agregar extension .csv si no la tiene
        if not ruta.endswith('.csv'):
            ruta += '.csv'
        
        archivos.guardarcsv(inventario, ruta)
    
    except KeyboardInterrupt:
        print("\n operación cancelada")
    except Exception as e:
        print(f"\n error inesperado: {e}")


def opcioncargar():
    """opcion 8: cargar desde csv."""
    print("\n--- CARGAR DESDE CSV ---")
    
    try:
        ruta = input("nombre del archivo, enter para sobreescribir ").strip()
        
        if ruta == "":
            ruta = "inventario.csv"
        
        # agregar extension .csv si no la tiene
        if not ruta.endswith('.csv'):
            ruta += '.csv'
        
        # cargar productos
        productoscargados, filasinvalidas = archivos.cargarcsv(ruta)
        
        # si no se cargo nada, salir
        if len(productoscargados) == 0:
            if filasinvalidas > 0:
                print(f"\n se omitieron {filasinvalidas} filas inválidas.")
            return
        
        # decidir si sobrescribir o fusionar
        if len(inventario) > 0:
            print(f"\nel inventario actual tiene {len(inventario)} productos.")
            
            if validarconfirmacion("¿sobrescribir inventario actual? (S/N): "):
                # sobrescribir
                inventario.clear()
                inventario.extend(productoscargados)
                accion = "reemplazo"
            else:
                # fusionar
                accion = "fusión"
                print("política de fusión: se sumará la cantidad y se actualizará el precio.")
                
                for prodnuevo in productoscargados:
                    prodexistente = servicios.buscarproducto(inventario, prodnuevo['nombre'])
                    
                    if prodexistente is not None:
                        # actualizar producto existente
                        prodexistente['cantidad'] += prodnuevo['cantidad']
                        prodexistente['precio'] = prodnuevo['precio']
                    else:
                        # agregar como nuevo
                        inventario.append(prodnuevo)
        else:
            # inventario vacio, simplemente cargar
            inventario.extend(productoscargados)
            accion = "carga inicial"
        
        # mostrar resumen
        print(f"\n carga completada:")
        print(f"   • productos cargados: {len(productoscargados)}")
        print(f"   • filas inválidas omitidas: {filasinvalidas}")
        print(f"   • acción realizada: {accion}")
        print(f"   • total en inventario {len(inventario)} productos")
    
    except KeyboardInterrupt:
        print("\n operación cancelada.")
    except Exception as e:
        print(f"\n error inesperado: {e}")


def main():
    """funcion principal del programa."""
    print("\n" + "="*55)
    print("   sistema de gestión de inventario")
    print("="*55)
    
    while True:
        try:
            mostrarmenu()
            opcion = validaropcionmenu()
            
            if opcion == 1:
                opcionagregar()
            elif opcion == 2:
                opcionmostrar()
            elif opcion == 3:
                opcionbuscar()
            elif opcion == 4:
                opcionactualizar()
            elif opcion == 5:
                opcioneliminar()
            elif opcion == 6:
                opcionestadisticas()
            elif opcion == 7:
                opcionguardar()
            elif opcion == 8:
                opcioncargar()
            elif opcion == 9:
                print("\n" + "="*55)
                print(" has salido del sistema, baiii")
                print("="*55)
                break
        
        except KeyboardInterrupt:
            print("\n\n operación interrumpida, volviendo al menú..")
        
        except Exception as e:
            print(f"\n error inesperado: {e}")
            print("el programa continuará ejecutándose..")


if __name__ == "__main__":
    main()