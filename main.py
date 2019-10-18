from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
from Pparser import post_parser
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add/post")
def adiciona_post(conn):

	#post_parser(txt,post_id,conn)


    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");''')
            cursor.execute('''INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor",1,1);''')
            cursor.execute('''COMMIT''')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

@app.post("/add/view")
def adiciona_view(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");''')
            cursor.execute('''INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor",1,1);''')
            cursor.execute('''INSERT INTO Visualizado (Post_idPost, Usuarios_idUsuarios, IP,Browser,Aparelho,Data) VALUES (1, 1, "8.8.8.8","Chrome","Nokia Bolado",'2018-12-31 23:59:59');''')
            cursor.execute('''COMMIT''')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir ')

@app.post("/remove/post")
def remove_post(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''UPDATE Post SET Atividade=0 WHERE Usuarios_idUsuarios=1''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel remover da tabela Post')