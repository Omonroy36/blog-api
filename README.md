Preparar entorno virtual
##### Solo si tienen mas de una version de python
```
$ pipenv --python="3.x" 
```
##### Crear el entorno virtual con la version por defecto de python
```
$ pipenv shell 
```
Instalar las librerias necesarias dentro del Pipfile
```
$ pipenv install
```
Comandos para la base de datos
### Ejecutar solo la primera vez si no tienen la carpeta migrations
```
$ python app.py db init 
```
### Ejecutar para crear las migraciones 
```
$ python app.py db migrate
```

### Ejecutar para enviar las migraciones hacia la base de datos
```
$ python app.py db upgrade
```

Iniciar el servidor
```
$ python app.py runserver
```
