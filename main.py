
#Python
#import pymysql
#from uuid import UUID

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Form, Path, Query

#Files
#from models import *

app = FastAPI(title='Backend Junior Python Digiworld')


@app.get('/')
def index():
    return 'Backend Junior Python Digiworld'