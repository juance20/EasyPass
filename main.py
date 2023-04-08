import art
import os
import json
import sys
import random

#Definimos la función para mostrar el menú principal
def print_menu():
    print(art.text2art("EasyPass"))

    print("""
1. Guardar nueva contraseña
2. Buscar contraseña
3. Mostrar todas las contraseñas
4. Eliminar contraseña
5. Actualizar contraseña
6. Salir
    """)

#---------------------------------------------------------------------------------------------------

def clear():
    #Si el sistema operativo es windows, usamos el comando cls
    if os.name == "nt":
        os.system("CLS")
    
    #Si el sistema operativo es linux o mac, usamos el comando clear
    elif os.name == "posix":
        os.system("clear")

#---------------------------------------------------------------------------------------------------

def generar_contraseña():
    #Establecemos los caracteres que vamos a utilizar para generar la contraseña
    chars = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz0123456789!¡¿?'#$%&/()=´`^¨~+¨*[]-.,;:_<>"
    n = 0
    passwd = ""
    while n < 32:
        #Vamos añadiendo caracteres seleccionados aleatoriamente de la cadena anterior hasta tener 32
        passwd = passwd + random.choice(chars)
        n += 1

    return passwd

#---------------------------------------------------------------------------------------------------

def guardar_contraseña():
    #Pedimos al usuario las credenciales
    usr = input("Por favor, ingrese el nombre de usuario: ")
    passwd = input("Por favor, ingrese la contraseña (dejar en blanco para generar automáticamente): ")
    print("Recomendación!")
    print("Quizá quiera añadir una descripción en caso de repetir varias veces el nombre de usuario")
    desc = input("Descripción (puede quedar en blanco): ")

    #Verificamos el input del usuario
    if usr == "":
        print("El usuario está vacío!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    #Si está en blanco, generamos la contraseña
    if passwd == "":
        passwd = generar_contraseña()

    #Creamos un nuevo objeto JSON para guardarlo
    new = {"usr": usr,
           "passwd": passwd,
           "desc": desc}
    
    try:
        with open("database.json", "r+") as file:
            #Añadimos a la base de datos el nuevo objeto
            file_data = json.load(file)
            file_data.append(new)
            file.seek(0)
            #Escribimos los nuevos datos en el archivo
            json.dump(file_data, file, indent=4)

    except FileNotFoundError:
        #Si no existe el archivo, lo creamos y luego guardamos las credenciales
        with open("database.json", "w") as file:
            file.write("[]")


        with open("database.json", "r+") as file:
            file_data = json.load(file)
            file_data.append(new)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    print("La contraseña fue añadida exitosamente!")
    print("Presione ENTER para continuar")
    input()
    clear()

#------------------------------------------------------------------------------------------

def buscar_contraseña():
    #Pedimos las credenciales al usuario
    usr = input("Ingrese el nombre de usuario: ")
    results = []

    #Leemos la base de datos
    with open("database.json", "r") as file:
        data = json.load(file)

    #Recorremos todos los objetos de la base de datos y seleccionamos aquellos que coinciden en el nombre de usuario
    for obj in data:
        if obj["usr"] == usr:
            results.append(obj)
    
    #Verificamos si hay coincidencias o no
    if len(results) == 0:
        print("No hay ningun registro con ese usuario!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    else:
        #Limpiamos la pantalla y mostramos los resultados
        clear()
        print("Resultados: ")
        for obj in results:
            print(f"""---------------
Usuario: {obj["usr"]}
Contraseña: {obj["passwd"]}
Descripción: {obj["desc"]}
---------------""")
    
    print("Presione ENTER para continuar")
    input()
    clear()

#--------------------------------------------------------------------------------------

def mostrar_contraseñas():
    results = []

    #Leemos la base de datos
    with open("database.json", "r") as file:
        data = json.load(file)

    for obj in data:
        results.append(obj)
    
    #Verificamos si hay elementos guardados
    if len(results) == 0:
        print("No hay ninguna contraseña registrada!")
    
    else:
        #Limpiamos la pantalla y mostramos las credenciales

        clear()
        print("Resultados: ")
        for obj in results:
            print(f"""---------------
Usuario: {obj["usr"]}
Contraseña: {obj["passwd"]}
Descripción: {obj["desc"]}
---------------""")
    
    print("Presione ENTER para continuar")
    input()
    clear()

#----------------------------------------------------------------------------------------------

def eliminar_contraseña():
    results = []

    #Leemos la base de datos
    with open("database.json", "r") as file:
        data = json.load(file)

    for obj in data:
        results.append(obj)
    
    #Verificamos que haya credenciales guardadas
    if len(results) == 0:
        print("No hay ninguna contraseña registrada!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    else:
        #Mostramos las crendenciales junto a un ID
        clear()
        i = 0
        for i in range(len(results)):
            
            print(f"""---------------
ID: {i}
Usuario: {data[i]["usr"]}
Contraseña: {data[i]["passwd"]}
Descripción: {data[i]["desc"]}
---------------""")

    #Pedimos al usuario que seleccione las credenciales para eliminar
    id = input("\nIngrese el ID de la contraseña a eliminar: ")
    
    #Verificamos que el ID es válido
    if not id.isnumeric():
        print("El ID no es válido!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    elif int(id) >= len(results) or i < 0:
        print("El ID no es válido!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return

    with open("database.json", "r+") as file:
            file_data = json.load(file)
            file_data.pop(int(id))
    
    #Sobreescribimos los datos sin las credenciales seleccionadas
    with open("database.json", "w") as file:
        json.dump(file_data, file, indent=4)
    
    print("Contraseña removida exitosamente")              
    print("Presione ENTER para continuar")
    input()
    clear()

#----------------------------------------------------------------------------

def actualizar_contraseña():
    results = []

    #Leemos la base de datos
    with open("database.json", "r") as file:
        data = json.load(file)

    for obj in data:
        results.append(obj)
    
    #Verificamos que hay credenciales guardadas
    if len(results) == 0:
        print("No hay ninguna contraseña registrada!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    else:
        #Mostramos las credenciales junto a un ID
        clear()
        i = 0
        for i in range(len(results)):
            
            print(f"""---------------
ID: {i}
Usuario: {data[i]["usr"]}
Contraseña: {data[i]["passwd"]}
Descripción: {data[i]["desc"]}
---------------""")
                  
    #Pedimos al usuario que seleccione las credenciales
    id = input("\nIngrese el ID de la contraseña a actualizar: ")
    
    #Verificamos el ID
    if not id.isnumeric():
        print("El ID no es válido!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return
    
    if not (int(id) < len(results) and i >= 0):
        print("El ID no es válido!")
        print("Presione ENTER para continuar")
        input()
        clear()
        return

    #Solicitamos la nueva contraseña
    new_passwd = input("Ingrese la nueva contraseña (dejar en blanco para generar automáticamente): ")

    #Si está en blanco, la generamos
    if new_passwd == "":
        new_passwd = generar_contraseña()

    #Leemos y actualizamos los datos
    with open("database.json", "r+") as file:
            file_data = json.load(file)
            file_data[int(id)]["passwd"] = new_passwd
    
    with open("database.json", "w") as file:
        json.dump(file_data, file, indent=4)
    
    print("Contraseña actualizada exitosamente")           
    print("Presione ENTER para continuar")
    input()
    clear()

if __name__ == "__main__":
    while True:
        print_menu()
        op = input("\nIngrese una opción: ")
        if op == "1":
            guardar_contraseña()
        elif op == "2":
            buscar_contraseña()
        elif op == "3":
            mostrar_contraseñas()
        elif op == "4":
            eliminar_contraseña()
        elif op == "5":
            actualizar_contraseña()
        elif op == "6":
            print("Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida!")
            print("Presione ENTER para continuar")
            input()
            clear()
        



    


