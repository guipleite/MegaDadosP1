import pymysql


txt = "SSSSSSSSSSSSSSSSAsdadada asd #123, asdawfe . @hugo #gostoso @monts!"

def post_parser(txt,post_id,conn):
	
	txts = txt.split(' ')

	for i in txts:
		if i[0] == "#":
			n=0
			for j in i[1:]:
				if j =='#'or j =='/'or j ==','or j ==';'or j =='?'or j ==':'or j =='!':
					break
				n+=1

			#adicionar tag
			print("tag:",i[1:n+1])
			with conn.cursor() as cursor:
				try:
					cursor.execute('''SELECT idPassaros FROM passaros WHERE nome = ''')
					cursor.execute('''INSERT INTO Tag (Post_idPost, Passaros_idPassaros, Ativar) VALUES (1, 1,1)''')
					cursor.execute('''COMMIT''')
				except pymysql.err.IntegrityError as e:
					raise ValueError(f'Não foi possivel ')

		elif i[0] == "@":
			n=0
			for j in i[1:]:
				if j =='#'or j =='/'or j ==','or j ==';'or j =='?'or j ==':'or j =='!':
					break
				n+=1

			#adicionar shout
			print("shout:",i[1:n+1])