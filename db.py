## file para poder conectarse a la base de datos local 'postgres' creada desde el archivo docker-compose ##

# se importa la librearia de sqlachemy, se crea un motor para poder conectarse a la base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# URl representa y llevara los componentes para conectarse a la base de datos con los datos correspondientes
from sqlalchemy.engine import URL


url=URL(
    drivername = 'postgresql',
    username = 'daysuke',
    password = 'contraseña',
    host = 'localhost',
    database = 'postgres',
    port = '5432'
)

# se crea un motor para poder conectarse a la base de datos, usando la coneccion configurada 'url'
engine = create_engine(url)
# se trae a sessionmaker, y bind tendra lo de la variable engine 'el motor de la base de datos'
Session = sessionmaker(bind=engine)
# todo lo de las 2 variables anteriores se guardaran y tendran todo en la variable 'session'
session = Session()

