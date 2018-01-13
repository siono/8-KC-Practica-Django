# Wordplease: Plataforma de Blogging



## Instalación
Para poner en marcha la plataforma se deberán seguir los siguientes pasos

### Instalar Django 3.5+

### Instalar dependencias
Ejecutar el comando que instalará las librerías necesarias en el entorno virtual

```
(env)$ pip install -r requirements.txt
```
### Crear BBDD y ejecutar migraciones

En la carpeta `src` del proyecto ejecutamos:

```
(env)$ python manage.py migrate
```

### Crear usuario de acceso a la administración de la aplicación

Para poder crear datos en las distintas entidades de la aplicación debe crearse primero un superusuario y proporcionar los datos necesarios

```
(env)$ python manage.py createsuperuser
```

### Arranque del servidor de desarrollo

```
(env)$ python manage.py runserver
```

### Acceso a interfaz de administración de la aplicación

http://127.0.0.1:8000/admin/login/

### Acceso al frontal de la aplicación

http://127.0.0.1:8000/
