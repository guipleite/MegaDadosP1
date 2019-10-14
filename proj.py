import pymysql

def adiciona_usuarios(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela usuarios')

def acha_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Nome,Email,Cidade from usuarios WHERE nome="Joao" ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def adiciona_post(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");')
            cursor.execute('INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor"),1,1;')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

def acha_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Titulo Post WHERE Usuarios_idUsuarios=1 ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_post(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");')
            cursor.execute('''INSERT INTO Passaros (Nome, Especie) VALUES ("cacatua, caracatua") ''')
            cursor.execute('INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor"),1,1;')
            cursor.execute('''INSERT INTO Tag (Post_idPost, Passaros_idPassaros, Ativar) VALUES (1, 1,1)''')
            cursor.execute('''INSERT INTO Mencionar (Usuarios_idUsuarios, Post_idPost, Ativar) VALUES (1, 1,1)''')

            cursor.execute('''UPDATE Posts SET ativo=0 WHERE Usuarios_idUsuarios=1''')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel remover da tabela Post')

def menciona_passaro(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");')
            cursor.execute('''INSERT INTO Passaros (Nome, Especie) VALUES ("cacatua, caracatua") ''')
            cursor.execute('INSERT INTO Post (Titulo, Texto, URL,Atividade,Usuarios_idUsuarios) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor"),1,1;')
            cursor.execute('''INSERT INTO Tag (Post_idPost, Passaros_idPassaros, Ativar) VALUES (1, 1,1)''')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel ')

def acha_menciona_passaro(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Post_idPost, Passaros_idPassaros, ativo from Tag WHERE Passaros_idPassaros=1 AND Post_idPost=1 AND Ativar=1 ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def menciona_usuario(conn):
    with conn.cursor() as cursor:
        try:

            cursor.execute('INSERT INTO Post (Titulo, Texto, URL) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor");')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

def acha_menciona_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Nome,Email,Cidade from usuarios WHERE nome="Joao" ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def adiciona_view(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Post (Titulo, Texto, URL) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor");')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

def acha_view(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Nome,Email,Cidade from usuarios WHERE nome="Joao" ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def adiciona_pref(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (Nome, Email, Cidade) VALUES ("Joao", "dasd@ads.com", "Sorocaba");')
            cursor.execute('INSERT INTO Post (Titulo, Texto, URL) VALUES ("Title", "lore ipsuum lfkmaknfklansf", "http://reddit.com/r/ProgrammerHumor");')
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel inserir na tabela Post')

def acha_pref(conn):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT Nome,Email,Cidade from usuarios WHERE nome="Joao" ''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
