"""
modulo de servicios para gestion de inventario.
funciones crud y calculo de estadisticas.
"""

def agregarproducto(inventario, nombre, precio, cantidad):
    """
    agrega un producto al inventario.
    retorna true si se agrego, false si ya existe.
    """
    # verificar si ya existe
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return False
    
    # agregar producto
    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })
    return True


def mostrarinventario(inventario):
    """
    muestra todos los productos del inventario en formato tabla.
    """
    if len(inventario) == 0:
        print("\n⚠️  El inventario está vacío.")
        return
    
    print("\n" + "="*75)
    print(f"{'NOMBRE':<25} {'PRECIO':>15} {'CANTIDAD':>15} {'SUBTOTAL':>15}")
    print("="*75)
    
    for producto in inventario:
        subtotal = producto["precio"] * producto["cantidad"]
        print(f"{producto['nombre']:<25} ${producto['precio']:>14.2f} {producto['cantidad']:>15} ${subtotal:>14.2f}")
    
    print("="*75)


def buscarproducto(inventario, nombre):
    """
    busca un producto por nombre (no distingue mayusculas).
    retorna el diccionario del producto o none si no existe.
    """
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizarproducto(inventario, nombre, nuevoprecio=None, nuevacantidad=None):
    """
    actualiza precio y/o cantidad de un producto.
    retorna true si se actualizo, false si no existe.
    """
    producto = buscarproducto(inventario, nombre)
    
    if producto is None:
        return False
    
    if nuevoprecio is not None:
        producto["precio"] = nuevoprecio
    
    if nuevacantidad is not None:
        producto["cantidad"] = nuevacantidad
    
    return True


def eliminarproducto(inventario, nombre):
    """
    elimina un producto del inventario.
    retorna true si se elimino, false si no existe.
    """
    for i in range(len(inventario)):
        if inventario[i]["nombre"].lower() == nombre.lower():
            inventario.pop(i)
            return True
    return False


def calcularestadisticas(inventario):
    """
    calcula estadisticas del inventario.
    retorna tupla: (unidadestotales, valortotal, productomascaro, productomayorstock)
    """
    if len(inventario) == 0:
        return (0, 0.0, None, None)
    
    # unidades totales
    unidadestotales = 0
    for producto in inventario:
        unidadestotales += producto["cantidad"]
    
    # valor total usando lambda
    calcularsubtotal = lambda p: p["precio"] * p["cantidad"]
    valortotal = 0.0
    for producto in inventario:
        valortotal += calcularsubtotal(producto)
    
    # producto mas caro
    productomascaro = inventario[0]
    for producto in inventario:
        if producto["precio"] > productomascaro["precio"]:
            productomascaro = producto
    
    # producto con mayor stock
    productomayorstock = inventario[0]
    for producto in inventario:
        if producto["cantidad"] > productomayorstock["cantidad"]:
            productomayorstock = producto
    
    return (unidadestotales, valortotal, productomascaro, productomayorstock)