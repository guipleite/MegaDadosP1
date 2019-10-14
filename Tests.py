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

    def test_adiciona_usuarios(self):
        conn = self.__class__.connection

        # Adiciona um usuario.
        adiciona_usuarios(conn)

        # Tenta adicionar o mesmo usuario duas vezes.
        try:
            adiciona_usuarios(conn)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_usuario(conn)
        self.assertIsNotNone(id)

    def test_adiciona_post(self):
        conn = self.__class__.connection

        # Adiciona comida não existente.
        adiciona_post(conn)

        # Checa se a o post existe.
        id = acha_post(conn)
        self.assertIsNotNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection

        remove_post(conn)

        with conn.cursor() as cursor:
            try:
                cursor.execute('''SELECT Ativar FROM Tag WHERE Passaros_idPassaros=1''')
                self.assertEqual(cursor.fetchone()[0],0)

                cursor.execute('''SELECT Ativar FROM Mencionar WHERE Usuarios_idUsuarios=1''')
                self.assertEqual(cursor.fetchone()[0],0)

                cursor.execute('''SELECT Ativo FROM Posts WHERE Usuarios_idUsuarios=1''')
                self.assertEqual(cursor.fetchone()[0],0)

            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não foi possivel :(')

    def test_menciona_passaro(self):
        conn = self.__class__.connection

        menciona_passaro(conn)
        id = acha_menciona_passaro(conn)
        self.assertIsNotNone(id)

    def test_menciona_usuario(self):
        conn = self.__class__.connection

        menciona_usuario(conn)
        id = acha_menciona_usuario(conn)
        self.assertIsNotNone(id)

    def test_adiciona_view(self):
        conn = self.__class__.connection

        adiciona_view(conn)
        id = acha_view(conn)
        self.assertIsNotNone(id)

    def test_adiciona_pref(self):
        conn = self.__class__.connection

        adiciona_pref(conn)
        id = acha_pref(conn)
        self.assertIsNotNone(id)

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
    filenames = [entry for entry in os.listdir()
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
