### video : "https://www.youtube.com/watch?v=wcbxMRgu9bE&t=204s "  ###

" al ejecutarse los endpoints, los datos se quedara guardados en la base de datos local creada "

# se importa fastAPI, http para control de exceptions
from fastapi import FastAPI, HTTPException,Depends
# se importan de modelo/schema (file todo.py) las tablas
from schemas.todo import Usuarios,Frutas, Celulares
# se importa del modelo (file db.py)  "session" para poder conectarse a la base de datos
from db import get_db
## imports para seguridad en la base de datos
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# intancia de fastapi
app = FastAPI()

# todas las funciones deben ser asyncronas 'async' (responderan cuando le sea disponible) 

""" 
************************************
* endpoints de la tabla 'usuarios' * 
************************************
"""

" enpoint .get para ver todos los users de la tabla 'usuarios' "
@app.get ("/users/")
async def ver_todos_los_usuarios(
    db: Session = Depends(get_db)
):
    # Se obtienen todos los registros de la tabla Frutas
    usuarios= db.query(Usuarios).all()
    # Se verifica si hay al menos un registro en la tabla 'frutas'
    if not usuarios:
        raise HTTPException(status_code= 404, detail="ninguna fruta encontrada")
    # si si hay value, retorna 'frutas'
    return usuarios

" enpoint .get para ver los datos de un {id} en especifico de la tabla 'usuarios' "
@app.get ("/users/{id}")
async def ver_usuairo_por_id(id:int, db: Session = Depends(get_db)):
    # Se busca el usuario por el id proporcionado
    user_query = db.query(Usuarios).filter(Usuarios.id == id)
    # Se obtiene el primer objeto que cumple con la condición
    user = user_query.first()
    # Se verifica si se encontró la fruta, si no se retorna una exception personalizada
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Se retorna la fruta encontrada
    return user
   

" enpoint .post para crear datos en la tabla 'usuarios' "
@app.post("/users/")
async def crear_usuario(nombre:str, presupuesto:int, db: Session = Depends(get_db)): # los parametros deben ser los mismos de la tabla de la class "Todo"
    user = Usuarios(nombre=nombre, presupuesto=presupuesto)
    db.add(user)    # se le dice a la db 'db' que agregue 'todo 'con todas sus instancias'
    db.commit()     # commit es para que se ejecute la transaccion
    return {"usuario agregado" : user.nombre}


" end point .put para actualizar datos de 'usuarios' "
@app.put("/users/{id}")
async def actualizar_usuario(id: int, nombre: str, presupuesto: int, db: Session = Depends(get_db)):
    # Se busca el usuario por el id proporcionado
    usuario_query = db.query(Usuarios).filter(Usuarios.id == id)
    #  recibir el primer objeto que este en la tabla
    usuario = usuario_query.first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # se actualizan los valores
    usuario.nombre = nombre
    usuario.presupuesto = presupuesto
    # Se confirman los cambios en la base de datos
    db.add(usuario)
    db.commit()
    
    return {"mensaje": "Usuario actualizado correctamente"}


" endpoint .delete para eliminar un valor/datos de 'usuarios'"
@app.delete("/users/{id}")
async def eliminar_usuario(id:int, db: Session = Depends(get_db)):
    # 
    usuario_query = db.query(Usuarios).filter(Usuarios.id == id)
    # recibir el primer objeto que este en la tabla
    usuario = usuario_query.first()
    # Se confirman los cambios en la base de datos
    db.delete(usuario)    # se agregara todo 'con todas sus instancias'
    db.commit()        # commit es para que se ejecute la transaccion
    return {"usuario eliminado": id}


""" 
**********************************
* endpoints de la tabla 'frutas' * 
**********************************
"""

" enpoint .get para ver todas las frutas de la tabla 'frutas' "
@app.get ("/frutas/")
async def ver_todas_las_frutas(db: Session = Depends(get_db)):
    # Se obtienen todos los registros de la tabla Frutas
    frutas= db.query(Frutas).all()
    # Se verifica si hay al menos un registro en la tabla 'frutas'
    if not frutas:
        raise HTTPException(status_code= 404, detail="ninguna fruta encontrada")
    # si si hay value, retorna 'frutas'
    return frutas

" endpoint .get para ver una fruta en especifico por 'id' "
@app.get("/frutas/{id}")
async def ver_fruta_por_id(id: int, db: Session = Depends(get_db)):
    # Se busca la fruta por el id proporcionado
    fruta_query = db.query(Frutas).filter(Frutas.id == id)
    # recibir el primer objeto que este en la tabla
    fruta = fruta_query.first()
    # Se verifica si se encontró la fruta, si no se retorna una exception personalizada
    if fruta is None:
        raise HTTPException(status_code=404, detail="Fruta no encontrada")
    # Se retorna la fruta encontrada
    return fruta


" enpoint .post para crear datos en la tabla 'frutas' "
@app.post("/frutas/{id}")
async def crear_fruta(id: int, nombre_fruta: str, cantidad_azucar: int, db: Session = Depends(get_db)):
    # Verificamos si ya existe una fruta con el mismo id
    existing_fruta = db.query(Frutas).filter(Frutas.id == id).first()
    if existing_fruta: # si ya existe una fruta con el mismo id, se programa un exception
        raise HTTPException(status_code=400, detail="Ya existe una fruta con este ID")
    # Creamos una nueva instancia de la clase Frutas
    nueva_fruta = Frutas(id=id, nombre_fruta=nombre_fruta, cantidad_azucar=cantidad_azucar)
    # Agregamos la nueva fruta a la sesión usando db importado de 'db'
    db.add(nueva_fruta)
    # Confirmamos los cambios en la base de datos
    db.commit()
    # Retornamos la nueva fruta creada
    return  {"fruta agregada" : nombre_fruta}


" end point .put para actualizar datos de 'frutas' "
@app.put("/frutas/{id}")
async def actualizar_fruta_por_id(id: int, nombre_fruta: str, cantidad_azucar: int, db: Session = Depends(get_db)):
    # Verificamos si ya existe una fruta con el mismo id
    fruta_query = db.query(Frutas).filter(Frutas.id == id)
    # recibir el primer objeto que este en la tabla
    fruta = fruta_query.first()
    # se verifica que haya un valor en fruta, si no hay se retorna una exception personalizada
    if fruta is None:
        raise HTTPException(status_code=404, detail="Fruta no encontrada")
    # se actualizan los valores
    fruta.nombre_fruta = nombre_fruta
    fruta.cantidad_azucar = cantidad_azucar
    # Se confirman los cambios en la base de datos
    db.add(fruta)
    db.commit()
    
    return {"mensaje": "Fruta actualizada correctamente"}

# Corregida session para no colgar la conexion a la base de datos
" end point .put para asignar un id de propietario a una fruta' "
@app.put("/frutas/asignar/{id}")
async def asignar_id_propietario(id: int, propietario_id: int, db: Session = Depends(get_db)):
    try:
        print("id: ", id)
        print("propietario_id: ", propietario_id)
        # Verificamos si ya existe una fruta con el mismo id
        fruta_query = db.query(Frutas).filter(Frutas.id == id)
        # recibir el primer objeto que este en la tabla
        fruta = fruta_query.first()
        # se verifica que haya un valor en fruta, si no hay se retorna una exception personalizada
        if fruta is None:
            raise HTTPException(status_code=404, detail="Fruta no encontrada")
        # se actualizan los valores
        propietario = db.query(Usuarios).filter(Usuarios.id == propietario_id).first()
        print("propietario: ", propietario)
        if propietario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        fruta.propietario_id = propietario_id
        # Se confirman los cambios en la base de datos
        db.add(fruta)
        db.commit()
    except SQLAlchemyError as e:
        print("Error: ", e)
        db.rollback()
        raise HTTPException(status_code=404, detail="Error paso algo feo")
    return {"mensaje": "Fruta asignada a usuario correctamente"}


" endpoint .delete para eliminar loa valores/datos de 'frutas'"
@app.delete("/frutas/{id}")
async def eliminar_frutas(id: int, db: Session = Depends(get_db)):
    # Verificamos si ya existe una fruta con el mismo id
    fruta_query = db.query(Frutas).filter(Frutas.id == id)
    # recibir el primer objeto que este en la tabla
    fruta = fruta_query.first()
    if fruta is None:
        raise HTTPException(status_code=404, detail="Fruta no encontrada")
    # Se confirman los cambios en la base de datos
    db.delete(fruta)
    db.commit()
    
    return {"mensaje": "Fruta eliminada correctamente"}




@app.post("/celulares/")
def crear_celular(
    nombre_celular: str, cantidad_ram: int, cantidad_rom: int, marca: str, propietario_id: int, db: Session = Depends(get_db)
):
    celular = Celulares(nombre_celular=nombre_celular, cantidad_ram=cantidad_ram, cantidad_rom=cantidad_rom, marca=marca, propietario_id=propietario_id)
    db.add(celular)
    db.commit()
    return {"celular agregado" : celular.nombre_celular}
# se debe estar en la ruta actual para poder levantar el servidor con uvicorn
# D:\programacion\Python_Backend\practicas apis\api_base_de_datos

# uvicorn main:app --reload
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs          - ver documentacion via web con todos los enpoint y probarlos