from crud import CRUD


crud = CRUD()
archivo = "datos.csv"

crud.crear_archivo(archivo)

while True:
    print("\n--- MENU ---")
    print("1. Crear persona")
    print("2. Listar personas")
    print("3. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        nombre = input("Nombre: ")
        edad = input("Edad: ")

        id_creado = crud.crear(archivo, nombre, edad)
        print(f"Persona creada con ID: {id_creado}")

    elif opcion == "2":
        datos = crud.listar(archivo)
        print("\n--- LISTADO ---")
        for fila in datos:
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Edad: {fila[2]}")

    elif opcion == "3":
        print("Saliendo...")
        break

    else:
        print("Opción no válida")