from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
import json
from Pparser import post_parser
app = FastAPI()

def setUp():
	with open('config_tests.json', 'r') as f:
		config = json.load(f)
		conn = pymysql.connect(
			#host=config['HOST'],
			user=config['USER'],
			password=config['PASS'],
			database='mydb'
		)
	return conn

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/add/usr")
def adiciona_usuario(name,email,location):
	conn = setUp()

	with conn.cursor() as cursor:
		try:
			cursor.execute('''INSERT INTO usuarios (Nome, Email, Cidade) VALUES (%s,%s,%s);''',(name,email,location))
			cursor.execute('''COMMIT''')

		except pymysql.err.IntegrityError as e:
			conn.close()
			raise ValueError(f'Não foi possivel inserir na tabela usuarios')

	conn.close()

@app.put("/add/bird")
def adiciona_passaro(name,species):

	conn = setUp()

	with conn.cursor() as cursor:
		try:
			cursor.execute('''INSERT INTO Passaros (Nome, Especie) VALUES (%s,%s);''',(name,species))
			cursor.execute('''COMMIT''')

		except pymysql.err.IntegrityError as e:
			conn.close()
			raise ValueError(f'Não foi possivel inserir na tabela Passaros')

	conn.close()

@app.put("/add/post")
def adiciona_post(title,text,url,usr_id,status=1):#Pegar o id dos nomes dos passaros e usrs

    conn = setUp()

    tags,shouts = post_parser(text)

    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES (%s,%s,%s,%s,%s);''',(title,text,url,status,usr_id))
            cursor.execute('''COMMIT''')

            post_id=1
            tagged_id =3 ###
            shouted_id = 3 #######

            for shout in shouts:
                cursor.execute('''INSERT INTO Mencionar (Usuarios_idUsuarios, Post_idPost, Ativar) VALUES (%s,%s,%s);''',(shouted_id,post_id,status))
                cursor.execute('''COMMIT''')

            for tag in tags:
                cursor.execute('''INSERT INTO Tag (Post_idPost, Passaros_idPassaros, Ativar) VALUES (%s,%s,%s);''',(post_id,tagged_id,status))
                cursor.execute('''COMMIT''')



        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

    conn.close()

@app.put("/add/view")
def adiciona_view(post_id,usr_id,browser,ip,device,date):
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO Visualizado (Post_idPost, Usuarios_idUsuarios, IP,Browser,Aparelho,Data) VALUES (%s,%s,%s,%s,%s,%s);''',(post_id,usr_id,ip,browser,device,date))
            cursor.execute('''COMMIT''')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir ')
    conn.close()


@app.put("/add/pref")
def adiciona_pref(usr_id,bird_id):
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO Usuarios_Passaros(Usuarios_idUsuarios,Passaros_idPassaros) VALUES (%s,%s);''',(usr_id,bird_id))
            cursor.execute('''COMMIT''')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')

    conn.close()


@app.post("/remove/post")##########################
def remove_post(conn):

    conn = setUp()

    with conn.cursor() as cursor:
        try:
            cursor.execute('''UPDATE Post SET Atividade=0 WHERE Usuarios_idUsuarios=1''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel remover da tabela Post')
    conn.close()



# def upvote_post():

# def downvote_post():


# def usuario_posts():

# def usuario_popular():

# def usuario_ref():

# def views_tipo():

# def passaros_img():