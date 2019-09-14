# math-learning-server

Servidor Django

El mismo se puede correr de dos maneras diferentes:

## Correr usando Docker compose

Correr el siguiente comando en una terminal estando posicionado en el mismo directorio que el docker-compose.yml:

Primera vez:

    $ docker-compose up --build
    
Luego no es necesario el --build

    $ docker-compose up


## Correr utilizando un virtualenv

correr el siguiente comando para activar el entorno virtual:

    $ source ./bin/activate

luego correr el siguiente comando para instalar las dependencias:

    $ pip3 install -r mathlearning/requirements.txt 

por ultimo para iniciar la aplicacion django correr:

    $ python mathlearning/manage.py runserver 0.0.0.0:5000
