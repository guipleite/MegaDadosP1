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
def adiciona_post(title,text,url,usr_id,status=1):

    conn = setUp()

    tags,shouts = post_parser(text)

    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES (%s,%s,%s,%s,%s);''',(title,text,url,status,usr_id))
            cursor.execute('''COMMIT''')

            cursor.execute('''SELECT LAST_INSERT_ID()''')
            post_id = cursor.fetchone()[0]
            for shout in shouts:
                cursor.execute('''SELECT idUsuarios FROM Usuarios WHERE Nome = %s''',(shout))
                shouted_id = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO Mencionar (Usuarios_idUsuarios, Post_idPost, Ativar) VALUES (%s,%s,%s);''',(shouted_id,post_id,status))
                cursor.execute('''COMMIT''')

            for tag in tags:
                cursor.execute('''SELECT idPassaros FROM Passaros WHERE Nome = %s''',(tag))
                tagged_id = cursor.fetchone()[0]
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

@app.delete("/remove/post")
def remove_post(post_id):

    conn = setUp()

    with conn.cursor() as cursor:
        try:
            cursor.execute('''UPDATE Post SET Atividade=0 WHERE idPost=%s;''',(post_id))
            cursor.execute('''UPDATE Post SET Atividade=0 WHERE idPost=%s;''',(post_id))
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel remover da tabela Post')
    conn.close()

@app.put("/post/updownvote")
def updownvote(usr_id,post_id,vote): 
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO Joinha (Usuarios_idUsuarios, Post_idPost, Joi) VALUES (%s, %s, %s);''',(usr_id,post_id,vote))
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()

@app.put("/post/updatevote")
def updatevote(usr_id,post_id,vote): 
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''UPDATE Joinha SET Joi = %s  WHERE Usuarios_idUsuarios = %s AND Post_idPost=%s ''',(vote,usr_id,post_id))
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()

@app.get("/list/usr_posts")
def usuario_posts(usr_id):
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''SELECT * FROM Post INNER JOIN Usuarios ON Post.Usuarios_idUsuarios = Usuarios.idUsuarios WHERE idUsuarios = %s ORDER BY idPost DESC;''',(usr_id))
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()

@app.get("/list/usr_pop")
def usuario_popular():
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''DROP VIEW IF EXISTS RankingPoPu;''')
            cursor.execute('''CREATE VIEW RankingPoPu AS SELECT Cidade, idUsuarios, Nome FROM Usuarios 
            				  INNER JOIN Mencionar ON Usuarios.idUsuarios = Mencionar.Usuarios_idUsuarios 
    						  GROUP BY Usuarios_idUsuarios ORDER BY COUNT(Post_idPost) DESC;''')
            cursor.execute('''SELECT * FROM RankingPoPu GROUP BY Cidade;''')
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()

@app.get("/list/usr_ref")
def usuario_ref(usr_id):
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''SELECT Nome FROM Usuarios WHERE idUsuarios in 
				 (SELECT Post.Usuarios_idUsuarios FROM Mencionar INNER JOIN Usuarios ON Usuarios.idUsuarios = Mencionar.Usuarios_idUsuarios 
		          INNER JOIN Post ON Mencionar.Post_idPost = Post.idPost WHERE idUsuarios = %s GROUP BY Post.Usuarios_idUsuarios);''',(usr_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')

@app.get("/list/views_type")
def views_tipo():
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''SELECT Browser, Aparelho, COUNT(IP) FROM Visualizado GROUP BY Browser, Aparelho;''')
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()

@app.get("/list/bird_img")
def passaros_img():
    conn = setUp()
    with conn.cursor() as cursor:
        try:
            cursor.execute('''SELECT URL, Passaros_idPassaros FROM Post INNER JOIN Tag ON Post.idPost = Tag.Post_idPost GROUP BY Passaros_idPassaros, URL;''')
            cursor.execute('''COMMIT''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel')
    conn.close()