# Django Rest Framework

<div style="margin-bottom:50px;"></div>

# Tabla de contenido
[Consideraciones importantes](#consideraciones-importantes)
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
9. [Documentación clases django rest framework](#documentación-clases-de-rest-framework)
    - [ListAPIView general](#listapiview-general)
10. [Serializar Relaciones en Modelos](#formas-de-serializar-relaciones-en-modelos)
    - [Método 1](#método-1)
    - [Método 2](#método-2)
    - [Método 3](#método-3)
11. [Vistas Genéricas](#vistas-genéricas)
    - [CreateAPIView](#createapiview)
    - [RetrieveAPIView](#retrieveapiview)
    - [DestroyAPIView](#destroyapiview)
    - [UpdateAPIView](#updateapiview)
    - [ListCreateAPIView](#listcreateapiview)
    - [RetrieveUpdateAPIView](#retrieveupdateapiview)
    - [DestroyUpdateAPIView](#destroyupdateapiview)
    - [RetrieveUpdateDestroy](#retrieveupdatedestroy)
12. [ViewSets y Routers](#viewsets-y-routers)
13. [Auto-Documentacion de API: SWAGGER](#auto-documentacion-de-api-swagger)
14. [TOKEN y JWT: Teoría y Funcionamiento](#token-y-jwt-teoría-y-funcionamiento)
    - [Simple JWT](#jwt-para-django-simple-jwt)
    - [Django Rest Framework: Authentication](#django-rest-framework-authentication)
15. [LOGIN con TOKEN + SESIONES](#login-con-token--sesiones)
16. [Logout + TOKEN + Sesiones](#logout--token--sesiones)
17. [TIEMPO de EXPIRACIÓN a Token](#tiempo-de-expiración-a-token)
18. [AUTENTICACION General para todas las VISTAS](#autenticacion-general-para-todas-las-vistas)
19. [Configurar CORS en la API](#configurar-cors-en-la-api)

<div style="margin-bottom:50px;"></div>   

---
## Consideraciones importantes
---

**request**: el request ya modifica su contenido para ser accedido
- ***request.POST***: -> request.data(incluye archivos e imágenes enviados)
- ***request.GET***: -> request.query_params

<div style="margin:20px 0;"></div>

Se tiene nuevas variables en el request
- ***accepted_rederer***: -> JSONRenderer()
- ***accepted_media_type***: -> application/json

<div style="margin:20px 0;"></div>

**response**: el response viene con la siguiente estructura
```python
response(data, status=None, template_name=None, headers=None, content_type=None)
```
- **data:** son los datos ya SERIALIZADOS que se envían como respuesta.
- **status:** código HTTP de estado para la respuesta, por defecto retorna código HTTP_200_OK.
- **template_name:** plantilla a utilizar si es que se utiliza HTMLRenderer como medio de renderizado.
-  **content_type:** tipo de contenido de la respuesta, este tipo es definido automáticamente cuando se trata la petición pero hay casos donde se debe especificar manualmente.

<div style="margin:20px 0;"></div>

**ruta**: ruta comparativa de django vs django rest_framework

- ***DJANGO*** Modelo -> Form -> Vista -> Ruta
- ***DJANGO REST FRAMEWORK*** Modelo -> Serializador -> Vista -> Router

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

> Un buen uso de sobreescribirlo es cuando no queramos guardar algo en la base de datos. Como por ejemplo un formulario, o un envio de correo.

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

<div style="margin-bottom:50px;"></div>   

---
## Documentación clases de Rest Framework
---
Este es un sitio para indagar sobre las clases permitidas en Django Rest Framework, ya que la documentación no aborda mucho este tema.

> https://www.cdrf.co/

<div style="margin-bottom:50px;"></div> 

---
## ListAPIView general
---

Es una vista utilizada para listar un modelo

``` python
from rest_framework.generics import ListAPIView

from apps.products.api.serializers.general_serializer import MeasureUnitSerializer

class MeasureUnitListAPIView(generics.ListAPIView):
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
        return MeasureUnit.objects.filter(state = True)
```

<div style="margin-bottom:50px;"></div> 

---
## Formas de Serializar Relaciones en Modelos
---

Esto hace referencia a la respuesta de un modelo en json, predeterminadamente en un módelo ForeignKey, devuelve el id y no el nombre del campo, para solucionar esto puede realizarse lo siguiente:

### Método 1
Desde el serializador, llamamos el serializador general

product_serializers.py
``` python
from rest_framework import serializers

from apps.products.models import Product
from apps.products.api.serializers.general_serializer import MeasureUnitSerializer, CategoryProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    measure_unit = MeasureUnitSerializer() #nombre tal cual en el modelo
    category_product = CategoryProductSerializer()

    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','delete_date')
```

### Método 2
Utilizando la clase Meta del modelo de la cual hace referencia la clave foranea. especificamente en la función __str__

product_serializers.py
``` python
from rest_framework import serializers

from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    measure_unit = serializers.StringRelatedField() #nombre tal cual en el modelo
    category_product =  serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','delete_date')
```

### Método 3
Utilizando la función to_representation() del serializador

product_serializers.py
``` python
from rest_framework import serializers

from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','delete_date')

    def to_representation(self, intance):
        return {
            'id': intance.id,
            'description': intance.description,
            'image': intance.image if intance.image != '' else '',
            'measure_unit': intance.measure_unit.description,
            'category_product': intance.category_product.description,
        }
```

<div style="margin-bottom:50px;"></div> 

---
## Vistas genéricas
---
### CreateAPIView
se utiliza para crear una instancia en el modelo

``` python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
```


### RetrieveAPIView
obtener una sola instancia y no un listado del modelo, es decir el detalle de una instancia

``` python
class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    # def get(self,request,pk=None):
    #     pass
```

### DestroyAPIView
eliminar una instancia del modelo

``` python
from rest_framework import generics

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
```

cambiar el estado de una instancia del modelo, sobreescribiendo el método delete()

``` python
from rest_framework import generics

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def delete(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'message':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
```

### UpdateAPIView
actualizar una instancia del modelo

``` python
from rest_framework import generics

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def patch(self, request, pk= None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk= None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)

```

> El método tiene PUT Y PATCH

1. **PUT:** modifica toda la instancia 
2. **PATCH:** modifica solo un campo de la instancia


### ListCreateAPIView 
es una vista basada en clases que permite unir en una sola dos metodos listar y crear, es decir, la misma ruta la utilizamos en GET: para listar y en POST para crear

```python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset= ProductSerializer.Meta.model.objects.filter(state = True)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
```

> Se debe agregar el queryset para el GET o sobreescribir el get_queryset()

### RetrieveUpdateAPIView 
permite unir en una sola dos metodos obtener detalle y actualizar, es decir, la misma ruta la utilizamos en GET: para obtener y en POST para actualizar

```python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
    
    #se puede sobreescribir el método PUT
    def put(self, request, pk = None):
        return Response({'error': 'Hola'})

```

### DestroyUpdateAPIView 
permite unir en una sola dos metodos obtener eliminar y actualizar, es decir, la misma ruta la utilizamos en GET: para obtener y en POST para eliminar

```python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer


class ProductDestroyAPIView(generics.DestroyUpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def delete(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
```
### RetrieveUpdateDestroy 
permite unir en una misma ruta el obtener un elemento y permitir PUT para modificar o DELETE para eliminar

```python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    def delete(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk= None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk= None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
```

<div style="margin-bottom:50px;"></div> 

---
## ViewSets y Routers
---

***ViewSets*** son una agrupación de todos los métodos http en una sola clase

> https://www.django-rest-framework.org/api-guide/viewsets/

```python
from rest_framework import viewsets

class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
```

> Un ViewSet no se puede asignar a una ruta común en el archivo url.py


***Routers*** son las rutas especiales para trabajar con viewsets

> https://www.django-rest-framework.org/api-guide/routers/

1. Crear un archivo dentro de la carpeta api llado routers.py

2. Crear el router

```python
from rest_framework.routers import DefaultRouter

from apps.products.api.views.product_views import ProductViewSet

router = DefaultRouter()

router.register(r'', ProductViewSet)

urlpatterns = router.urls #exportamos las rutas y las mandamos a la variable urlpatterns, que es una lista.
```

3. Modificamos el enlace en las urls de la raiz del proyecto
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('apps.products.api.routers')),
]
```

**Ejemplo**
```python
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.api.serializers.product_serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state = True)

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(product_serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk= None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk= None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
```

<div style="margin-bottom:50px;"></div> 

---
## Auto-Documentacion de API: SWAGGER
---

> https://drf-yasg.readthedocs.io/en/stable/readme.html

> https://swagger.io/



<div style="margin-bottom:50px;"></div> 

---
## TOKEN y JWT: Teoría y Funcionamiento
---

***token:*** es una serie de caracteres en una base o cifrado especifico, que permite asociarlo a un usuario y agregarle cierto información, poder permitir el acceso o negarlo, estos token tienen un ciclo de vida y se puede definir en minutos, horas, dias. 

Es un caracter aleatorio.

> Ejemplo: lkgfhjsjhgfsrfju545814

***JWT:*** es la evolución del token y significa JSON WEB TOKEN, es un estandar abierto publicado en el RFC 7519 que define una forma de encapsular y compartir **CLAIMS**.

Tienen una firma digital, que pueden generarse utilizando claves simetricas o claves asimetricas.

También se pueden encontrar datos cifrados, que en gran parte contienen datos sensibles, **NO** es recomendable contraseñas.

***CLAIMS:*** caracteristicas que tienen los jwt y sirven para tratar una petición (REQUEST) que viene de un dispositivo que sera recibido por el backend.

> https://jwt.io/

### JWT Para django: Simple JWT

> **Simple JWT:** https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

> **Simple JWT Github:** https://github.com/SimpleJWT/django-rest-framework-simplejwt


### Django Rest Framework: Authentication

> **Django Rest Framework:** Authentication: https://www.django-rest-framework.org/api-guide/authentication/

> **Django Rest Framework Authentication Github:** https://github.com/encode/django-rest-framework/blob/e32ebc41998ffd7f22f6e691badb86a709c89ba7/rest_framework/authentication.py#L33


<div style="margin-bottom:50px;"></div> 

---
## LOGIN con TOKEN + SESIONES
---

Para utilizar el token que viene en django rest framework, se deben realizar los siguientes pasos:

1. En el archivo base.py en THIRD_APPS se agrega:
``` python
THIRD_APPS = [
    ...
    'rest_framework.authtoken',
    ...
]
``` 
2. Generar migraciones:
``` python
python3 manage.py makemigrations
``` 
``` python
python3 manage.py migrate
``` 

3. Dentro de la app user o donde se tenga el modelo usuarios, se agrega un archivo llamado views.py
``` python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.api.serializers import UserTokenSerializer

class Login(ObtainAuthToken):

    def post(self, request,*args,**kwargs):
        login_serializer = self.serializer_class(data=request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token':token.key,
                        'user': user_serializer.data,
                        'message': 'Successful login'
                    }, status = status.HTTP_201_CREATED)
                else:
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token':token.key,
                        'user': user_serializer.data,
                        'message': 'Successful login'
                    }, status = status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid session'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Incorrect username or password'}, status = status.HTTP_400_BAD_REQUEST)
``` 

4. Agregar la ruta en las urls del proyecto
```python
from django.contrib import admin
from django.urls import path, include

from apps.users.views import Login

urlpatterns = [
    ...
    path('', Login.as_view(), name='login'),
    ...
]
``` 
5. Para verificar estas rutas se utilizará POSTMAN

> https://www.postman.com/

6. Crear un serializador para mostrar los datos desde postman que deseemos al crear un usuario
```python
class UserTokenSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')
``` 

7. Para permitir solo un logueo simultaneo de una misma cuenta, se manejaran las sesiones de django
```python

from datetime import datetime
from django.contrib.sessions.models import Session

class Login(ObtainAuthToken):

    def post(self, request,*args,**kwargs):
        ....
                if created:
                   ....
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) #__gte: mayor o igual
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    ....
``` 

8. Cuando te piden si ya inicio sesión no crear nuevo token ni borrar sesiones, sino de una vez evitar que inicie sesión se modifica de la siguiente manera
```python

from datetime import datetime
from django.contrib.sessions.models import Session

class Login(ObtainAuthToken):

    def post(self, request,*args,**kwargs):
        ....
                if created:
                   ....
                else:
                    token.delete()
                    return Response({'error': 'Invalid session'}, status = status.HTTP_409_CONFLICT)
``` 

<div style="margin-bottom:50px;"></div> 

---
## Logout + TOKEN + Sesiones
---
para crear un logout utilizamos rest_framework

1. En el archivo views.py de user o de la app creada para el logueo:
``` python
from django.contrib.sessions.models import Session
from rest_framework.views import APIView

class Logout(APIView):

    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user 
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()

                session_message = 'Deleted user sessions'            
                token_message = 'Token removed'
                return Response({'message_token':token_message, 'message_session': session_message},status = status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid session'},status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'token in request incorrect'},status = status.HTTP_409_CONFLICT)
``` 

> Esto es ejemplo siempre debe hacerse en POST

<div style="margin-bottom:50px;"></div> 

---
## TIEMPO de EXPIRACIÓN a Token
---
Para agregar tiempo de expiración crearemos una clase que herede de TokenAuthentication

> https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py

1. Creamos dentro de la aplicación user o la encargada del logueo, un archivo llamado authentication.py

2. En el archivo creamos el siguiente código:
``` python
from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed



class ExpiringTokenAuthentication(TokenAuthentication):

    '''
    Calculate the expiration time with a variable from the base of the settings
    '''
    def expires_in(self,token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    '''
    Validates if the token has expired
    '''
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    '''
    Creates a variable called is_expire which verifies by means of the is_token_expired function, the elapsed time.
    '''
    def token_expire_handler(self,token):
        is_expire = self.is_token_expired(token)
        if is_expire:
        return is_expire

    '''
    '''
    def authenticate_credentials(self,key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        is_expired = self.token_expire_handler(token)

        if is_expired:
            raise AuthenticationFailed('Your token has expired')

        return (token.user, token)
```
3. En el archivo base.py del settings creamos la variable de expiración
``` python
#Token expiration in seconds
TOKEN_EXPIRED_AFTER_SECONDS = 10
```

<div style="margin-bottom:50px;"></div> 

---
## AUTENTICACION General para todas las VISTAS
---
Para agregar una autenticación para todas las vistas

1. Creamos dentro de la aplicación user o la encargada del logueo, un archivo llamado authentication_mixins.py

2. En el archivo creamos el siguiente código:
``` python
from rest_framework.authentication import get_authorization_header
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response

from apps.users.authentication import ExpiringTokenAuthentication

class Authentication(object):

    user = None
    user_token_expired = False

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ExpiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token)
            if user is not None and token is not None:
                self.user = user
                return user
            return message 
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is not None:
            if type(user) == str:       
                response = Response({'error':user,'expired':self.user_token_expired}, status = status.HTTP_400_BAD_REQUEST)         
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response
            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)
        response = Response({'error': 'No credentials have been sent','expired':self.user_token_expired}, status = status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
```

3. En las rutas que necesitemos importamos el mixins. Utilizaremos como ejemplo productos (archivo product_viewset.py). Y lo mandamos como parametro.
``` python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.api.serializers.product_serializers import ProductSerializer
from apps.users.authentication_mixins import Authentication

class ProductViewSet(Authentication, ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state = True)

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(product_serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk= None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk= None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)

```

4. Para refrescar el token mediante el FRONTEND

    * Creamos en el archivo views de app user, una nueva clase para realizar esto
    ```python

    from rest_framework import status
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework.authtoken.models import Token

    from apps.users.api.serializers import UserTokenSerializer

    class UserToken(APIView):
        def get(self,request,*args,**kwargs):
            username = request.GET.get('username')
            try:
                #obteniendo el user al cual pertenece el nombre de usuario para traer el token
                user_token = Token.objects.get(
                    user = UserTokenSerializer().Meta.model.objects.filter(username=username).first()
                    )
                return Response({
                    'token': user_token.key
                })
            except:
                return Response({'error': 'credentials sent incorrectly'}, status = status.HTTP_400_BAD_REQUEST)
    ```
    * Lo asignamos a una url
    ```python
    from apps.users.views import UserToken
    urlpatterns = [
        ...
        path('refresh_token/', UserToken.as_view(), name='refresh_token'),
        ...
    ]
    
    ```


<div style="margin-bottom:50px;"></div>   

---
## Configurar CORS en la API
---
Cuando estamos comunicando una API con cualquier cliente FRONTEND, tenemos que configurar los CORS o CORS HEADERS

**CORS:** políticas que añaden configuraciones al header de la petición  

Para Django existe un paquete que se llama django-cors-headers

> **DJANGO-CORS-HEADERS:** https://github.com/adamchainz/django-...


1. Se instala la libreria
``` python
python -m pip install django-cors-headers
``` 

2. Añadir la aplicación a base.py 
``` python
THIRD_APPS = [
    ...,
    "corsheaders",
]
``` 

3. Añadir el middleware, deben ser colocados lo mas alto posible
```python
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
``` 

4. Agregar una configuración extra en base.py
```python
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]
```

5. Agregar otra variable con lo mismo, porque en ocasiones presenta error chrome y android
```python
CORS_ORIGIN_WHITELIST = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]
```