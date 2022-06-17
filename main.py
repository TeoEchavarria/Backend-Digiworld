#Python
import pymysql
from uuid import UUID

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Form, Path, Query

#Files
from models import *

app = FastAPI(title='Backend Junior Python Digiworld')

#Crear tarea
#Editar tarea
#Eliminar tarea
#Listar todas las tareas
#Listar una tarea

# ----------------------------------------
#                DataBase
#-----------------------------------------
myConexion = pymysql.connect( host='localhost', user= 'root', passwd= "root", db='backend_digiworld' )
cur = myConexion.cursor()

@app.get('/')
def index():
    return 'Backend Junior Python Digiworld'

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user : UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister

    Return a json with the basic user information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    """
    user_dict = user.dict()
    cur.execute(
        "INSERT INTO user VALUES (%s, %s, %s, %s, %s)",
        (str(user_dict["user_id"]),user_dict["email"],user_dict["password"],user_dict["first_name"],user_dict["last_name"]))
    myConexion.commit()
    return user

### Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login(email: EmailStr  = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    cur.execute(
        f"SELECT * FROM backend_digiworld.user WHERE email =  '{str(email)}' AND password = '{password}';"
    )
    row = cur.fetchone()
    myConexion.commit()
    if row is None:
        return LoginOut(email=email, message="Login Unsuccessfully!")
    else:
        return LoginOut(email=email)


## Tareas

## Show a tarea by his ID
@app.get(
    path="/tarea/{tarea_id}",
    status_code=status.HTTP_200_OK,
    summary="show a Tarea by ID",
    tags=["Tareas"]
)
def show_a_tarea_id(tarea_id : UUID = Path(
        None,
        title = "Tarea ID",
        example = "3fa85f64-5717-4562-b3fc-2c966f66afa6"
    )):
    """
    Show a Tarea by his id

    This path operation Show a Tarea in the app.

    Parameters:
    - Request path parameter
        - tarea_id: UUID

    Returns a json with the basic user information:
    - tarea_id: UUID
    - title: str
    - body_text: str
    - status: bool
    - message : str
    """
    cur.execute(
        f"SELECT * FROM backend_digiworld.tareas WHERE tarea_id =  '{str(tarea_id)}';"
    )
    i = cur.fetchall()
    if i == ():
        myConexion.commit()
        return None
    else:
        i = i[0]
        reply = { "tarea:id":list(i)[0], 
        "title": list(i)[1], 
        "body text": list(i)[2], 
        "status": list(i)[3],
        "message": list(i)[4]}
        myConexion.commit()
        return reply

### Show all tareas
@app.get(
    path="/tareas",
    status_code=status.HTTP_200_OK,
    summary="Show all tareas",
    tags=["Tareas"]
)
def show_all_tareas():
    """
    This path operation shows all tareas in the app

    Returns a json list with all tareas in the app:
    - tarea_id: UUID
    - title: str
    - body_text: str
    - status: bool
    - message : str
    """
    cur.execute(
        "SELECT * FROM backend_digiworld.tareas;"
    )
    reply = [show_a_tarea_id(list(i)[0])for i in cur.fetchall()]
    myConexion.commit()
    return reply

### Create Tarea
@app.post(
    path="/tareas/create",
    status_code=status.HTTP_201_CREATED,
    summary="Created a tarea",
    tags=["Tareas"]
)
def create_a_tarea(tarea : Tarea = Body(...)):
    """
    Create a Tarea

    This path operations create a tarea in the app

    Parameters:
    - Request body parameter
        - tarea: Tarea

    Return a json with the basic user information:
    - tarea_id: UUID
    - title: str
    - body_text: str
    - status: bool
    - message : str
    """
    tarea_dict = tarea.dict()
    cur.execute(
        "INSERT INTO tareas VALUES (%s, %s, %s, %s, %s)",
        (str(tarea_dict["tarea_id"]),tarea_dict["title"],tarea_dict["body_text"],tarea_dict["status"],'Successful Creation!!!'))
    myConexion.commit()
    return show_a_tarea_id(tarea_dict["tarea_id"])

### Update a tarea
@app.put(
    path="/tareas/update",
    status_code=status.HTTP_200_OK,
    summary="Update a tarea",
    tags=["Tareas"]
)
def update_a_tarea(tarea_update : Tarea = Body(...)):
    """
    Update tarea

    This path operation update a tarea information in the app and save in the database

    Parameters:
    - tarea_id: UUID
    
    Returns a json with deleted tarea data:
    - tarea_id: UUID
    - title: str
    - body_text: str
    - status: bool
    - message : str
    """
    tarea_dict = tarea_update.dict()
    base_reply = show_a_tarea_id(tarea_dict['tarea_id'])
    base = [ base_reply[key] if value == "" else value for (key,value) in tarea_dict.items() ]
    base_reply = [value for value in base_reply.values() ]
    cur.execute(
        f"UPDATE `backend_digiworld`.`tareas` SET `title` = '{base[1]}', `body_text` = '{base[2]}', `status` = '{base[3]}', `message` = 'Update Successfully' WHERE (`tarea_id` = '{str(base[0])}');"
    )
    myConexion.commit()
    return show_a_tarea_id(base[0])

### Delete a tarea
@app.delete(
    path="/tareas/{tarea_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a tarea",
    tags=["Tareas"]
)
def delete_a_tarea(tarea_id : UUID = Path(
        None,
        title = "Tareas ID",
        example = "3fa85f64-5717-4562-b3fc-2c966f66afa6"
    )):
    """
    Delete a tarea

    This path operation delete a tarea in the app

    Parameters:
        - tarea_id: UUID

    Returns a json with deleted tarea data:
    - tarea_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    answerd = show_a_tarea_id(tarea_id)
    cur.execute(
    f"DELETE FROM `backend_digiworld`.`tareas` WHERE (`tarea_id` = '{str(tarea_id)}');"
    )
    myConexion.commit()
    return answerd