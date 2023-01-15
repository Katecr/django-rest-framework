# Django Rest Framework

---
## Instalación inicial
---

1. Creamos la carpeta del proyecto

```bash
mkdir nombre_carpeta
```

2. Dentro de la carpeta creamos el entorno virtual

```python
python -m venv nombre_entorno
```

3. Luego de creado activarlo
> Este comando sirve para windows
```python
nombre_entorno/Scripts/activate
```

4. también puede agregarse un alias al comando
```bash
doskey nombre_alias = nombre_entorno/Scripts/activate
```

> Solo ejecutar el nombre_alias para encender el entorno

5. instalar django rest framework
```python
pip install djangorestframework
```

6. Crear la carpeta del proyecto
```python
django-admin startproject nombre_proyecto
```

7. Dirigirnos a la carpeta del proyecto creada en el punto 6

---

## Configuración inicial de proyecto
---

1. Separar el settings

    * crear carpeta settings
    * archivo __init__.py
    * archivo base.py
    * archivo local.py
    * archivo production.py
    * separar INSTALLED_APPS
    * cambiar idioma (si se desea)

2. Crear carpeta apps
    * crear archivo __init__.py
    * dentro de la carpeta **apps**, crear app
    ```python
    django-admin startapp nombre_app
    ```

3. Para guardar el historial del usuario se puede instalar
```python
pip install django-simple-history
```
En THIRD_APPS añadir 'simple_history'

En MIDDLEWARE  añadir 'simple_history.middleware.HistoryRequestMiddleware'


4. Si el modelo de la app utiliza imagenes es necesario instalar la libreria Pillow
```python
pip install pillow
```

5. Hacer migraciones (Aun esta la base de datos default sqlite)
```python
py manage.py makemigrations
```
```python
py manage.py migrate
```

6. Crear super usuario
```python
py manage.py createsuperuser
```

7. Iniciar servidor
```python
py manage.py runserver
```

> Si quiere utilizar otro puerto
```python
py manage.py runserver 3030
```

---
## SERIALIZER y APIVIEW de usuario
---

* **serializer**: es aquel que toma la estructura de un modelo para convertir su estrcutura en un formato json

> a continuación es una manera de realizarlo, no es una verdad absoluta.


1. Eliminar dentro de la app el archivo ___views.py___
2. Eliminar dentro de la app el archivo ___tests.py___
3. Crear dentro de la app una carpeta llamada api

> Dentro de la carpeta api creamos lo siguiente:

1. archivo __init__.py
2. archivo serializers.py --> reemplaza forms.py
3. archivo api.py --> reemplaza views.py
4. archivo urls.py --> es el mismo archivo de las urls

* **apiview**: para generar vistas con funciones, utilizamos un decorador

1. en el archivo api.py importar el decorador

```python
from rest_framework.decorators import api_view
```

2. Crear la función

```python
@api_view(['GET'])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True)
        return Response(users_serializer.data)
```

3. En urls.py se invoca de la siguiente manera:
```python
path('user/', user_api_view, name="user")
```

4. obtener parametro de la url

```python
path('user_function/<int:pk>/', user_detail_view, name="user_detail")
```

```python
@api_view(['GET','PUT', 'DELETE'])
def user_detail_view(request, pk =None):
    if request.method == 'GET':
        if pk is not None:
            user = User.objects.filter(id=pk).first()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)

    elif request.method == 'PUT':
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)

    elif request.method == 'DELETE':
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response('eliminado')
```

---
## Estados HTTP
---
> https://www.django-rest-framework.org/api-guide/status-codes/

1. Importar modulo de django_rest_framework

```python
from rest_framework import status
```

2. Utilizarlo en una función
```python
@api_view(['GET','PUT', 'DELETE'])
def user_detail_view(request, pk =None):
    #queryset
    user = User.objects.filter(id=pk).first()
    #validation
    if user:
        if request.method == 'GET':
            if pk is not None:
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status= status.HTTP_200_OK)
        # update    
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status= status.HTTP_200_OK)
            return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        #delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'user deleted correct'}, status= status.HTTP_200_OK)
    else:
        return Response({'message':'user not found'}, status= status.HTTP_400_BAD_REQUEST)
```