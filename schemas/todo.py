""" 
en schemas iran las tablas que estaran en la base de datos, los modelos seran como el traductor entre el
codigo pyrhon y la base de datos, se importan librerias para poder hacer la coneccion 
"""

# sirven para poder declara valores en las tablas de datos que se crearan para la base de datos
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
# sirve para declara una base de datos
from sqlalchemy.orm import declarative_base
# para poder crear relacion en las tablas fimarias y secundarias
from sqlalchemy.orm import relationship
# se importa la coneccion de la bsae de datos 'el motor de coneecion que se creo'
from db import engine

Base = declarative_base()

# tabla modelo 'Usuarios'
class Usuarios(Base):
    __tablename__ = "usuarios"
    # al crearse un usuario, el id se autoincrementa solo
    id = Column(Integer, primary_key=True, autoincrement=True)
    # maximo de caracteres 50 permitidos
    nombre = Column(String(length=50))
    # este parametro no puede ir vacio 
    presupuesto = Column(Integer, nullable=False)
    # Relación entre Usuarios y Frutas
    frutas = relationship("Frutas", back_populates="propietario")
    celulares = relationship("Celulares", back_populates="propietario")


# tabla modelo 'Frutas'
class Frutas(Base):
    __tablename__ = "frutas"
    id = Column(Integer, primary_key=True)
    nombre_fruta = Column(String(length=20),nullable=False) # no puede tener valores nulos
    cantidad_azucar = Column(Integer) 
    # columna foránea con relación bidireccional de la tabla 'usuarios' referencia a la columna 'id'
    propietario_id = Column(Integer, ForeignKey("usuarios.id"))
    # Esto permite acceder a las frutas asociadas a un usuario y viceversa.
    propietario = relationship("Usuarios", back_populates="frutas")


class Celulares(Base):
    __tablename__ = "celulares"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    nombre_celular = Column(String(length=20),nullable=False) # no puede tener valores nulos
    cantidad_ram = Column(Integer)
    cantidad_rom = Column(Integer)
    marca = Column(String(length=20))
    propietario_id = Column(Integer, ForeignKey("usuarios.id"))
    propietario = relationship("Usuarios", back_populates="celulares")

# código de creación de tablas debe estar en el mismo archivo o módulo donde defines tus esquemas.
# se pasa el motor que se importo de db con un bloque de control de exception para saber si se creo o no
try:
    Base.metadata.create_all(engine)
    print("Tabla creada exitosamente")
except Exception as e:
    print("Error al crear la tabla:", e)
