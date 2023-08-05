#!/usr/bin/env python3


import sqlite3
from sqlite3 import Error
import traceback
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .customerror import custom_error
import time
from tabulate import tabulate
from .cryptomods import AES_decryption
from base64 import b64decode
import logging


class db_ops:
    """ This class is solely responsible for sql queries. It is also responsible for creating the 
        database initially creat and create_table functions. It performs insert, delete, update and create
        operations using the below defined functions."""
    def __init__(self,filepath=None,username=None,password=None, struct = None,id=None,flag=None, comments = None, conn = None):
        self.id = id
        self.flag = flag
        self.struct = struct
        self.conn = conn
        if filepath:
            self.filepath = filepath

        if username:
            self.username = username

        if password:
            self.password = password		

        if comments:
            self.comments = comments
        else:
            self.comments = 'NA'


    def create(self):
        if self.struct == None:
            try:
                logging.info('creating the inmemory database')
                conn = sqlite3.connect(":memory:")
                cursor = conn.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS credentials (
                            id integer PRIMARY KEY,
                            username text NOT NULL,
                            password text NOT NULL,
                            comments text NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            );
                        """)
                dumpsqlpath = os.path.join(self.filepath, 'dump.sql')
                with open(dumpsqlpath,'w') as f:
                    for line in conn.iterdump():
                        f.write('%s\n'%line)
                f.close()
                print('Database created')
            except Error as e:
                logging.error(e)
                print(e)
                
            finally:
                logging.info('closing the sqlite3 connection')
                conn.close()

        else:
            self.load()

    def load(self):
        if self.struct != None:
            try:
                logging.info('Loading the inmemory database')
                conn = sqlite3.connect(":memory:")
                cursor = conn.cursor()
                cursor.executescript(self.struct)
                conn.commit()
                logging.info('returning the sqlite3 connection')
                return conn
            except Error as e:
                logging.error(e)
                print(e)
                
        else:
            logging.error('Struct value is missing')
            raise ValueError('Structure value missing')


    def insert(self):
        try:
            logging.info('executing the insert query --insert')
            cursor = self.conn.cursor()
            cursor.execute(""" INSERT INTO credentials (username,password,comments) VALUES("{0}","{1}","{2}"); """.format(self.username,self.password,self.comments))
            logging.info('performing the commit')
            self.conn.commit()
        except Error as e:
            logging.error(e)
            print(e)



    def delete_val(self):
        if not self.id:
            logging.error('id value for the data is missing')
            raise custom_error('missing')
            
        else:
            try:
                logging.info('connecting to sqlite3 database --delete values')
                cursor = self.conn.cursor()
                logging.info('selecting data to validate')
                cursor.execute("SELECT * FROM credentials WHERE id= %i;"%(self.id))
                if len(cursor.fetchall()) == 0:
                    logging.error("id doesn't exists")
                    print('Invalid id number\nNothing is deleted')
                else:
                    logging.info('executing the delete command')
                    cursor.execute("DELETE FROM credentials WHERE id = %i;"%(self.id))
                    self.conn.commit()
                    logging.info('committed the database')
                    print('Successfully Deleted')
            except Error as e:
                logging.error(e)
                print(e)
                
            
        time.sleep(2)
	
    def update_val(self):
        if not self.id:
            logging.error('missing id')
            raise custom_error('missing')
        else:
            try:
                logging.info('connecting to sqlite3 database --update values')
                cursor = self.conn.cursor()
                logging.info('selecting data to validate')
                cursor.execute("SELECT * FROM credentials WHERE id= %i;"%(self.id))
                if len(cursor.fetchall()) == 0:
                    logging.error("id doesn't exists")
                    print('Invalid id number\nCannot be updated')
                else:
                    if self.flag == 1:
                        logging.info('updating username')
                        cursor.execute("UPDATE credentials SET username='%s' WHERE id = %i;"%(self.username,self.id))
                        logging.info('performing commit to table')
                        self.conn.commit()
                        print('Successfully Updated Username')
                        
                        
                    elif self.flag == 2:
                        logging.info('updating username')
                        cursor.execute("UPDATE credentials SET password='%s' WHERE id = %i;"%(self.password,self.id))
                        logging.info('performing commit to table')
                        self.conn.commit()
                        print('Successfully Updated Password')
                        
                        
                    elif self.flag == 3:
                        logging.info('updating username and password')
                        cursor.execute("UPDATE credentials SET username='%s',password='%s' WHERE id = %i;"%(self.username,self.password,self.id))
                        self.conn.commit()
                        logging.info('performing commit to table')
                        print('Successfully Updated Credentials')
                        
                        
            except Error as e:
                logging.error(e)
                print(e)
                
                
            
            time.sleep(2)

    def dumps(self):
        dumpsqlpath = os.path.join(self.filepath, 'dump.sql')
        logging.info('Dumping database to the file for future use')
        with open(dumpsqlpath, 'w') as fsql:
            for line in self.conn.iterdump():
                fsql.write('%s\n'%line)
        fsql.close()
        logging.info('dump complete, file will be encrypted')

class show_data:
    """ This class has two important functions. First one is show_db which display the passwords in the
        encrypted form. Second one is dec_show_db function which decrypts the passwords stored in databases.
        Decrypted passwords are not stored anywhere except for in the memory.
        """
    def __init__(self, conn=None, passphrase=None,filepath=None):
        self.conn = conn

        if passphrase:
            self.passphrase = passphrase

        if filepath:
            self.filepath = filepath

    def show_db(self):
        try:
            logging.info('connecting to sqlite3 database --not decrypted')
            cursor = self.conn.cursor()
            logging.info('getting all the data from table')
            cursor.execute("SELECT * FROM credentials;")
            count = cursor.fetchall()
            table_val =[]
            logging.info('creating headers for tabular form')
            headers = ['ID','Username','Password','Comments','Timestamp']

            if len(count) != 0:
                logging.info('fetching values to print')
                for row in count:
                    tmp=[]
                    tmp.append(row[0])
                    tmp.append(row[1])
                    tmp.append(row[2])
                    tmp.append(row[3])
                    tmp.append(row[4])
                    table_val.append(tmp)
                logging.info('printing the encrypted password values')
                print(tabulate(table_val, headers, tablefmt="grid", colalign=("center",)))
                time.sleep(2)
            else:
                logging.info('empty table')
                print('No values found. Insert Some values')
                time.sleep(2)
        except Error as e:
            logging.error(e)
            print(e)
            


    def dec_show_db(self):
        try:
            logging.info('connecting to sqlite3 database --decrypted')
            cursor = self.conn.cursor()
            logging.info('getting all the data from table')
            cursor.execute("SELECT * FROM credentials;")
            count = cursor.fetchall()
            table_val =[]
            logging.info('creating headers for tabular form')
            headers = ['ID','Username','Password','Comments','Timestamp']
            if len(count) != 0:
                for row in count:
                    tmp=[]
                    tmp.append(row[0])
                    tmp.append(row[1])
                    logging.info('readying the decryption function')
                    dec_obj = AES_decryption(self.passphrase, db_data=row[2], filepath=self.filepath)
                    logging.info('decrypting for viewing')
                    tmp.append(dec_obj.decrypt_data())
                    tmp.append(row[3])
                    tmp.append(row[4])
                    table_val.append(tmp)
                logging.info('printing the decrypted password values')
                print(tabulate(table_val, headers, tablefmt="grid", colalign=("center",)))
                time.sleep(2)
            else:
                logging.info('empty table')
                print('No values found. Insert Some values')
                time.sleep(2)
        except Error as e:
            logging.error(e)
            print(e)

