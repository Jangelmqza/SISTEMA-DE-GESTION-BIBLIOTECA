#Sistema de gestión de biblioteca
#Creado por: Jose Angel Márquez Ramírez

from datetime import datetime, date
import baseTarea10

#agregar un libro
def agregar_libro(biblioteca, isbn, titulo, autor, año, copias):
    if isbn in biblioteca:
        biblioteca["libros"][isbn]["copias_disponibles"] += copias
        biblioteca["libros"][isbn]["copias_totales"] += copias
        return (f"Se han agregado {copias} al libro {titulo}.")
    else:
        biblioteca["libros"][isbn] = {
            "titulo" : titulo,
            "autor" : autor,
            "año" : año,
            "copias_disponibles" : copias,
            "copias_totales" : copias
        }
        return (f"El libro {titulo} ha sido agregado al catalogo")

#prestar un libro 
def prestar_libro(biblioteca, usuario_id, isbn):
    if usuario_id not in biblioteca["usuarios"]:
        return("Usuario no encontrado")
    
    usuario = biblioteca["usuarios"][usuario_id]

    #vaidacion para 3 libros 
    if len (usuario["libros prestados"]) >= 3:
        return ("Limite de libros alcanzado.")

    if isbn in biblioteca["libros"]:
        libro = biblioteca["libros"][isbn]
        if libro["copias_disponibles"] > 0:
            libro["copias_disponibles"] -=1
            biblioteca["usuarios"][usuario_id]["libros_prestados"].append(isbn)
            biblioteca["historial_prestamos"].append({
                "usuario": usuario_id,
                "isbn": isbn,
                "fecha": "2025-11-04"
            })
            return f"Prestamo exitoso: {libro["titulo"]}"  
        else:
            return "No hay copias disponibles"
    else:
        return"Libro no encontrado"

#Retornar libros 
def retornar_libro(biblioteca, usuario_id, isbn):
    if usuario_id not in biblioteca["usuarios"]:
        return("Usuario no encontrado.")
    usuario = biblioteca["usuarios"][usuario_id]

    if isbn in usuario["libros_prestados"]:
        biblioteca["libros"][isbn]["copias_disponibles"] += 1
        usuario["libros_prestados"].remove(isbn)

        mensaje_multa = ""
        for prestamo in reversed(biblioteca["historial_prestamos"]):
                if prestamo["usuario_id"] == usuario_id and prestamo["isbn"] == isbn and "devuelto" not in prestamo:
                    fecha_prestamo = datetime.strptime(prestamo["fecha"], "%Y-%m-%d")
                    fecha_devolucion = datetime.today()
                    prestamo["devuelto"] = str(fecha_devolucion.date())
                    
                    # Desafío: Implementar multas (Asumiendo 14 días límite)
                    dias_transcurridos = (fecha_devolucion - fecha_prestamo).days
                    if dias_transcurridos > 14:
                        dias_retraso = dias_transcurridos - 14
                        mensaje_multa = f" (Alerta: Retraso de {dias_retraso} días. Aplica multa)."
                    break
                    
        return f"Devolución de '{biblioteca['libros'][isbn]['titulo']}' exitosa.{mensaje_multa}"
    else:
        return "El usuario no tiene este libro prestado."

#consultar disponibilidad 
def consultar_disponibilidad(biblioteca, isbn):
    if isbn in biblioteca["libros"]:
        libro = biblioteca["libros"][isbn]
        return f"'{libro['titulo']}' por {libro['autor']} - Copias disponibles: {libro['copias_disponibles']}"
    else:
        return "Libro no encontrado."
    
#consultar libros de un usuario
def libros_usuario(biblioteca, usuario_id):
    usuario = biblioteca["usuarios"][usuario_id]
    prestados = []
    for isbn in usuario["libros_prestados"]:
        libro = biblioteca["libros"][isbn]
        prestados.append(f"{libro['titulo']} por {libro['autor']}")
    return prestados

#busqueda parcial 
def busqueda_parcial(biblioteca, termino):
    resultados = []
    for isbn, libro in biblioteca["libros"].items():
        if termino.lower() in libro["titulo"].lower() or termino.lower() in libro["autor"].lower():
            resultados.append(f"{libro['titulo']} por {libro['autor']} (ISBN: {isbn})")
    return resultados

#reporte de libros mas prestrados 
def reporte_libros_populares(biblioteca):
    conteo_prestamos = {}
    for prestamo in biblioteca["historial_prestamos"]:
        isbn = prestamo["isbn"]
        conteo_prestamos[isbn] = conteo_prestamos.get(isbn, 0) + 1

    libros_ordenados = sorted(conteo_prestamos.items(), key=lambda x: x[1], reverse=True)
    
    reporte = "Libros más prestados:\n"
    for isbn, conteo in libros_ordenados:
        libro = biblioteca["libros"][isbn]
        reporte += f"- {libro['titulo']} por {libro['autor']} (ISBN: {isbn}) - Prestado {conteo} veces\n"
    
    return reporte

def menu(biblioteca):
    while True:
        print("="*20, "MENÚ", "="*20)
        print("1. Agregar un libro al catálogo")
        print("2. Prestar un libro")
        print("3. Devolver un libro")
        print("4. Consultar disponibilidad de un libro")
        print("5. Ver libros prestados de un usuario")
        print("6. Buscar libros por título o autor")
        print("7. Ver reporte de libros más prestados")
        print("8. Salir del sistema")
        opcion = int(input("Elige una opcion (1-8): "))

        match opcion:
            case 1:
                print( "\n="*10, "Agregar libro", "="*10)
                titulo = str(input("Titulo del libro: "))
                autor = str(input("Autor: "))
                año = str(input("Año de publicación: "))
                copias = int(input("Copias: "))

                print(agregar_libro(biblioteca, isbn, titulo, autor, año, copias))

            case 2:
                print("\n="*10, "PRESTAR UN LIBRO", "="*10)
                usuario_id = input("Ingresa el usuario: ")
                isbn = input("Ingrese el ISBN del libro: ")
                resultado = prestar_libro(biblioteca, usuario_id, isbn)
                print(resultado)

            case 3:
                print("\n="*10, "DEVOLVER UN LIBRO", "="*10)
                usuario_id = input("Ingresa el usuario: ")
                isbn = input("Ingrese el ISBN del libro: ")
                resultado = retornar_libro(biblioteca, usuario_id, isbn)
                print(resultado)
            case 4:
                print("\n="*10, "Consultar disponibilidad", "="*10)
                isbn = input("Ingrese el ISBN del libro: ")
                resultado = consultar_disponibilidad(biblioteca, isbn)
                print(resultado)
            case 5:
                print("\n="*10, "Consultar libros", "="*10)
                usuario_id = input ("ingrese el usuario ")
                libros = libros_usuario(biblioteca, usuario_id)
                if libros:
                    print(f"Libros prestados por {biblioteca['usuarios'][usuario_id]['nombre']}:")
                    for libro in libros:
                        print(f"- {libro}")
                else:
                    print("No hay libros prestados para este usuario.")
                
            case 6:
                print("\n="*10, "Buscar libros", "="*10)
                termino = input("Ingrese el término de búsqueda: ")
                resultados = busqueda_parcial(biblioteca, termino)
                if resultados:
                    print("Resultados de la búsqueda:")
                    for resultado in resultados:
                        print(f"- {resultado}")
                else:
                    print("No se encontraron libros que coincidan con el término de búsqueda.")

            case 7:
                print("\n="*10, "Reporte de libros más prestados", "="*10)
                reporte = reporte_libros_populares(biblioteca)
                print(reporte)

            case 8:
                print("Saliendo del programa...")
                break

if __name__ == "__main__":
    menu(baseTarea10.biblioteca)
    
