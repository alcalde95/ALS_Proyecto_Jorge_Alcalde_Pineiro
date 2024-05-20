import uuid



class Clase:
    def __init__(self,nombre,descripcion,capacidadMaxima,duracion,creador):
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__capacidadMaxima = capacidadMaxima
        self.__duracion = duracion
        self.__creador = creador
        self.__id = str(uuid.uuid4())

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def capacidadMaxima(self):
        return self.__capacidadMaxima

    @capacidadMaxima.setter
    def capacidadMaxima(self, capacidadMaxima):
        self.__capacidadMaxima = capacidadMaxima

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, duracion):
        self.__duracion = duracion

    @property
    def creador(self):
        return self.__creador

    @property
    def id(self):
        return self.__id
