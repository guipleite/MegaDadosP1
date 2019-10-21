import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
from proj import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            #host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='mydb'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_request_add_user(self):
        conn = self.__class__.connection

        request_add_user(conn)
        
        with conn.cursor() as cursor:
            try:
                cursor.execute('''SELECT Nome , Email , Cidade from Usuarios WHERE Nome="test_add_usr" ''')
                self.assertEqual(cursor.fetchone(),(("test_add_usr", "email@email.com","Sao Paulo, SP")))
                cursor.execute('''COMMIT''') 

            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não foi possivel adicionar na tabela Usuarios' )   

    def test_request_add_passaro(self):
        conn = self.__class__.connection

        request_add_passaro(conn)
        
        with conn.cursor() as cursor:
            try:
                cursor.execute('''SELECT Nome , Especie from Passaros WHERE Nome="test_add_passaro" ''')
                self.assertEqual(cursor.fetchone(),(("test_add_passaro", "testus_addus_passarus")))
                cursor.execute('''COMMIT''') 

            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não foi possivel adicionar na tabela Usuarios' ) 

    def test_request_aa_add_post(self):
        conn = self.__class__.connection

        request_add_post(conn)
        
        with conn.cursor() as cursor:
            try:
                cursor.execute('''SELECT Titulo, Texto, URL,Atividade,Usuarios_idUsuarios from Post WHERE Titulo="test_add_post" ''')
                self.assertEqual(cursor.fetchone(),(("test_add_post", "test_add_post @test_add_post_u1 #test_add_post_b1","test_add_post_url",1,2)))
                cursor.execute('''COMMIT''')
                cursor.execute('''SELECT Ativar FROM Tag WHERE Post_idPost=1''')
                self.assertEqual(cursor.fetchone()[0],1)
                cursor.execute('''SELECT Ativar FROM Tag WHERE Post_idPost=1''')
                self.assertEqual(cursor.fetchone()[0],1)
            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não foi possivel adicionar na tabela Usuarios' )

    def test_request_aa_delete_post(self): ################
        conn = self.__class__.connection

        request_delete_post(conn)
        
        with conn.cursor() as cursor:
            try:
                cursor.execute('''SELECT Titulo, Texto, URL,Atividade,Usuarios_idUsuarios from Post WHERE Titulo="test_add_post" ''')
                self.assertEqual(cursor.fetchone(),(("test_add_post", "test_add_post @test_add_post_u1 #test_add_post_b1","test_add_post_url",0,2)))
                cursor.execute('''COMMIT''') 
                cursor.execute('''SELECT Ativar FROM Tag WHERE Post_idPost=1''')
                self.assertEqual(cursor.fetchone()[0],0)
                cursor.execute('''COMMIT''') 
                cursor.execute('''SELECT Ativar FROM Mencionar WHERE Post_idPost=1''')
                self.assertEqual(cursor.fetchone()[0],0)
                cursor.execute('''COMMIT''') 

            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não foi possivel adicionar na tabela Usuarios' ) 

    def test_request_pref(self):
        pass

    def test_request_views(self):
        pass

    def test_request_upvote(self):
        pass
        
    def test_request_z_remove_upvote(self):
        pass


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'],
                '-u', config['USER'],
                '-p' + config['PASS'],
                '-h', config['HOST']
            ],
            stdin=f
        )

def setUpModule():
    run_sql_script('P1script.sql')
    run_sql_script('P1script_Delta.sql')

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
