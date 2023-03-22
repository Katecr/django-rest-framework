# Django Rest Framework

<div style="margin-bottom:50px;"></div>

# Tabla de contenido
1. [Instalación inicial](#instalación-inicial)
2. [Configuración inicial de proyecto](#configuración-inicial-de-proyecto)
3. [SERIALIZER y APIVIEW de usuario](#serializer-y-apiview-de-usuario)
4. [Estados HTTP](#estados-http)
5. [Serializer](#serializer)
6. [Validaciones del Serializer](#validaciones-del-serializer)
    - [Método create en un Serializer](#método-create-en-un-serializer)
    - [Método update en un Serializer](#método-update-en-un-serializer)
    - [Método SAVE en un Serializer](#método-save-en-un-serializer)
7. [To representation en un Serializer](#to-representation-en-un-serializer)
8. [Encriptar contraseña en un Serializer](#encriptar-contraseña-en-un-serializer)

<div style="margin-bottom:50px;"></div>   

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

<div style="margin-bottom:50px;"></div>  

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


<div style="margin-bottom:50px;"></div>  

---
## SERIALIZER y APIVIEW de usuario
---

* **serializer**: es aquel que toma la estructura de un modelo para convertir su estructura en un formato json

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

<div style="margin-bottom:50px;"></div>  

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

<div style="margin-bottom:50px;"></div>  

---
## Serializer
---

Se pueden utilizar también sin modelos definidos

1. Ejemplo de serializer sin modelo creación en el archivo serializers.py

```python

from rest_framework import serializers


class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
```

2. Forma de utilizarlo en api.py

```python

from apps.users.api.serializers import TestUserSerializer


@api_view(['GET','POST'])
def user_api_view(request):
    #list
    if request.method == 'GET':
        #queryset
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True) #many= que son muchos o varios valores

        test_data = {
            'name': 'test',
            'email': 'test@example.com'
        }

        test_user = TestUserSerializer(data = test_data)

        if test_user.is_valid():
            print('paso validaciones')
        
        return Response(users_serializer.data, status= status.HTTP_200_OK)
```

<div style="margin-bottom:50px;"></div> 

---
## Validaciones del Serializer
    
---

```python

from rest_framework import serializers


class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()

    def validate_name(self, value):
        # custom validation
        if 'test2' in value:
            raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre')

        print(self.context)
        return value

    def validate_email(self, value):
        # custom validation
        if value == '':
            raise serializers.ValidationError('Tiene que indicar un correo')

        if self.context['name'] in value:
            raise serializers.ValidationError('El email no puede contener el nombre')
        return value

    def validate(self, data):
        return data
```

<div style="margin-bottom:50px;"></div> 

---
## Método create en un Serializer
---

cuando llamamos .save() pasa por un metodo intermedio llamado create()

recibe como parametros:

**self** 

**validated_data** = es la información valida que acaba de recibir el serializador

``` python
    def create(self, validated_data):
        return User.objects.create(**validated_data)
```

<div style="margin-bottom:50px;"></div> 

---
## Método update en un Serializer
---

cuando llamamos .save() en un función de actualizar o PUT, no pasa por create() sino por la función update()

recibe como parametros:

**self** 

**instance** = instancia u objecto al cual se esta haciendo referencia

**validated_data** = es la información valida que acaba de recibir el serializador

``` python
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.save()
        return instance
```


> Las validaciones del serializador se ejecutan tanto para crear como para actualizar, si se desean diferentes, deben escribirse en su propio método.

<div style="margin-bottom:50px;"></div>

---
## Método SAVE en un Serializer
---

El método save es el encargado de buscar el create o update, pero si este ese sobreescribe, ya solo hace lo que se le indique.

> Un buen uso de sobreescribirlo es cuando no queramos guardar algo en la base de datos. Como por ejemplo un formaulario, o un envio de correo.

``` python
    def save(self):
        pass
```

También el modelo tiene un metodo save(), es el utilizado en la logica del create y del update, si se desea sobreescribir se debe crear en el models.py

``` python
    def save(self,*args,**kwargs):
        pass
```

> Tienen el mismo nombre pero dependiendo de quien los llama se ejecutan.


<div style="margin-bottom:50px;"></div>

---
## To representation en un Serializer
---

Dentro de los serializadores se encuentra una Función llamada **to_representation()** utilizamos esta función cuando queremos devolver un diccionario con campos especifivos no todos los del modelo.

> Esta función llama a la automatización del modelo en el campo filds, que va recorriendo los campos convirtiendoles en diccionario (clave - valor)

1. Se debe modificar la consulta del modelo especificando los campos ejemplo:
``` python
#queryset
users=User.objects.all().values('id','username','password','email')
```

2. En el archivo serializer.py, se crea la función to_representation() que recibe dos parametros self y la instancia iterada en el momento.
``` python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    #asignar los items que se desean
    def to_representation(self,instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'password': instance['password'],
            'email': instance['email']
        }
```

> Esta función se utiliza en el GET, para mostrar solo cierta información, no influye en el create, update o delete. 

<div style="margin-bottom:50px;"></div>   

---
## Encriptar contraseña en un Serializer
---

Para encriptar la contraseña es necesario sobreescribir el método create y update en el serializador.

1. Sobreescribir la función create()
``` python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
       user = User(**validated_data) # tengo una instancia con la info enviada
       user.set_password(validated_data['password'])
       user.save()
       return user
```

2. Sobreescribir la función update()
``` python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self,instance, validated_data):
        update_user = super().update(instance,validated_data) 
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user
```