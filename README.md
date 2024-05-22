# ALS_Proyecto_Jorge_Alcalde_Pineiro
Apellidos, nombre: Alcalde Piñeiro Jorge 
NIF: 35600364k	
email: alcalde.ap95@gmail.com
Proyecto:  gym class and session management website. Users,Classes,Sessions,Registrations.
Repositorio: https://github.com/alcalde95/ALS_Proyecto_Jorge_Alcalde_Pineiro




# Base de datos

Entidades:
- User: usuario con email y contraseña
- Clase: clases que contendrán un uuid siendo este el identificador único, un nombre, la capacidad máxima de personas que se pueden inscribir a cada sesión,duración de cada sesión, una descripción y el creador de esta sesión.
- Session: sesión asociada a una clase que contendrá una fecha e un instructor que impartirá la clase, así como class_id, la clase de la que cuelga esta sesión
- Inscription : inscripción entre un usuario y una clase
- A nivel de funcionalidad habrá un usuario admin admin, que podrá borrar usuarios.
- Como usuario,podrás crear,editar y borrar tus propias clases. A su vez,podrás crear sesiones para cada clase y también borrarlas.
- Los usuarios también podrán inscribirse a las diferentes sesiones de las clases y a también desinscribirse.
- Los usuarios podrán iniciar sesión y registrarse

#Manual de usuario


Página de inicio desde donde se puede tanto iniciar sesión como registrarse.
Si está registrado podrá acceder a ver todas las clases

Una vez dentro podrá acceder a las clases pulsando Clases

Desde aquí podrá acceder a las clases creadas por el usuario, aquellas en las que está al menos inscrito a una sesión y a aquellas en las imparte por lo menos una sesión. Para poder acceder a la clase para ver sus sesiones se deberá pulsar enigma del nombre de la sesión

Esto se aplica tanto desde esta página, para poder ver las sesiones e inscribirse, como en la página de Mis clases, para acceder y ver las sesiones y poder tanto añadir nuevas sesiones como borrarlas. Si se accede desde clases gestionadas se mostrarán aquellas clases que gestiona el usuario, sin poder realizar ninguna modificación

# Rutas

- Página de inicio: /
- Inicio de sesión: /login
- Registro: /register
- Página del administrador: /admin
- Página de visualización de todas las clases: /classes
- Página de visualización y creación de tus propias clases: /myClasses
- Página edición de clase: /classes/edit/<id_clase>
- Página visualización para inscripción y desinscripción de sesiones:/classes/<id_clase>/clients
- Página visualización clases con al menos 1 inscripción: /inscribedClasses
- Página visualización clases con al menos 1 sesión gestionada: /managedClasses

# Instalación

Se debe tener instalado:
- Flask 3.0.3
- Flask-login 0.6.3
- Jinja2 3.1.3
- Redis 5.0.3
- Python 3.12.2


# Ejecución

Primero necesita tener un servidor Redis levantado y en ejecución

A continuación se deberá ejecutar setUp.py, que creará el usuario admin, dos usuarios: test@test.test y test2@test.test, ambos con la contraseña test1234, una clase para test@test.test,una sesión para esta clase y una inscripción de test2 a esta sesión.
```py
python setUp.py
```
Una vez listo, se ejecutará app.py,que levantará el servidor y nos indicará por la consola en qué puerto será levantado. Una vez levantado estaría todo listo


