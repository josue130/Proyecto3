from django.template import Template, Context
from django.http import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import os
import json



User_actual= ''
@csrf_exempt
def Main(request):
    global User_actual
    doc_externo = open("C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/Main.html")
    plt = Template(doc_externo.read())
    with open(User_actual, 'r') as file:
        data = json.load(file)
    doc_externo.close()
    
    if request.method == 'POST':
        ruta = request.POST.get('ruta')
        nombre = request.POST.get('nombre')
        contenido = request.POST.get('contenido')
       
        
        add_item(User_actual, ruta, nombre, "file", contenido)
        
        data = cargarJson(data)
        ctx = Context({'data':data})
        documento = plt.render(ctx)
        return HttpResponse(documento)
    else:
       
        #return render(request, 'plantilla.html', {'data': data})
        data = cargarJson(data)
        ctx = Context({'data':data})
        documento = plt.render(ctx)
        return HttpResponse(documento)
    

@csrf_exempt
def login_view(request):
    global User_actual
    doc_externo = open("C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/login.html")

    plt = Template(doc_externo.read())

    doc_externo.close()

    ctx = Context()

    documento = plt.render(ctx)
    if request.method == 'POST':
        if 'login' in request.POST:
            # El botón "Iniciar sesión" ha sido presionado
            username = request.POST['username']
            
            filename = f'{username}.json'
            User_actual = filename
            #add_item(filename, "local/subdir", "archivo1.txt", "file", "Contenido del archivo")
            #add_item(filename, "local", "Videos", "directory")
            #add_item(filename, "local/Videos", "VideosDatos.txt", "file", "Contenido del archivo")
            return redirect('/Main/')  # Redirige al nombre registrado en las URLs
        elif 'register' in request.POST:
            return redirect('/register/')

    return HttpResponse(documento)

@csrf_exempt
def register_view(request):
    global User_actual
    doc_externo = open("C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/register.html")
    plt = Template(doc_externo.read())
    doc_externo.close()
    ctx = Context()
    documento = plt.render(ctx)
    if request.method == 'POST':
        username = request.POST['username']
        capacidad_str = request.POST['capacidad']
        capacidad_int = int(capacidad_str)

        filename = f'{username}.json'
        User_actual = filename
        create_user_json(username,capacidad_int)  # Llama a la función para crear el JSON

        return redirect('/Main/')
    return HttpResponse(documento)




#_-------------------------------------------------------------------------------------------

#Entradas: Nombre de usuario log
#Restricciones: El usuario debe de estar creado
#Salida: Retorna un string simulando un html que contiene la estructura de una file system
#con los datos del Json


def cargarJson(estructura):
    html = "<ul>"
   
    for nombre, elemento in estructura.items():
        if elemento['type'] == 'file':
            path = elemento['path'] 
            
            html += f"<li class='file' onclick='mostrarOpcionesArchivo(\"{nombre}\",\"{path}\")'>{nombre}</li>"
          
        elif elemento['type'] == 'directory':
            path = elemento['path'] 
            html += f"<li class='file' onclick='mostrarOpcionesArchivo(\"{nombre}\",\"{path}\") '>{nombre} - Tipo: Directorio"
            html += cargarJson(elemento['content'])
            html += "</li>"
           
    html += "</ul>"
    return html
          

   

def add_item(filename, path, item_name, item_type, content=None):
    filesystem = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    current_dir[item_name] = {
        "type": item_type,
        "content": content if item_type == "file" else {}
    }
    with open(filename, "w") as file:
        json.dump(filesystem, file)

def create_user_json(username,capacidad):
    filename = f'{username}.json'
    if not os.path.exists(filename):
        user_data = {
            "local": {
            "type": "directory",
            "path":"local",
            "tamano":4,
            "content": {}
            },
            "compartido": {
            "type": "directory",
            "path":"compartido",
            "tamano":10,
            "content": {}
            },
            "User":{
                "type": "none",
                "capacidad":capacidad
            }
        }
        with open(filename, 'w') as file:
            json.dump(user_data, file)
