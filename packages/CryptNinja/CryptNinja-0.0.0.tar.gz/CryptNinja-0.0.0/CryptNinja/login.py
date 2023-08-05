#!/usr/bin/env python3

#####For internal use only######

from getpass import getpass
import re
from .customerror import custom_error
import string, random
import os
from .sqllib import db_ops
from .sqllib import show_data
import sys
import time
from .purge import purge_data
from .cryptomods import argon_hash
from .cryptomods import gen_master_key
from .cryptomods import gen_MAC_key
from .cryptomods import key_wrap
from .cryptomods import file_integrity
from .cryptomods import validation_check
from .cryptomods import AES_encryption
from .cryptomods import AES_decryption
import logging
from datetime import datetime
from base64 import b64encode,b64decode
from .customlogger import logger
from .getfilename import getfile




#calling logger function
filevalue = getfile()
pathdir = filevalue.getpath()
log = logger(filepath=pathdir)
log.move()
logdir = os.path.join(pathdir,'debug.log')
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename=logdir,level=logging.DEBUG)

#Function to clear old files
def clear_old_encrypted_file():
	logging.info('clearing old encrypted data files')
	for i in os.listdir(pathdir):
		if '.' not in i and 'pycache' not in i and 'logs' not in i:
			encfile = os.path.join(pathdir, i)
			logging.info('initiating the purge')
			pur = purge_data(encfile)
			pur.shred()
			os.unlink(encfile)
	logging.info('purged')



class authentication:
	""" This class is responsible for authentication of user. Login function defined here 
		helps to authenticate the user."""
	def __init__(self,password):
		self.password = password
		
	def login(self):
		logging.info('creating the validation check class')
		obj = validation_check(key=self.password,filepath=pathdir)
		if obj.validate():
			logging.info('correct user password')
			return True
		else:
			logging.info('incorrect password')
			return False


				
				
				
	def print_pass(self):
		"""Purpose of this test function is to view the password in cleartext. This class will be removed
		in the future versions of the software. """
		logging.error('this is dangerous and taken as a error, displaying password in cleartext may compromise the security')
		print('this is the password user entered %s'%((self.password)))


class Password:
	""" This class is responsible for creating using user generating password or providing the random password
	if user is willing to use."""
	def __init__(self, user_password=None):
		if user_password:
			logging.error('password initialized')
			raise ValueError('Password not required')
		else:
			self.user_password = user_password

	def create_password(self):
			
			print("""In short, the new NIST guidance recommends the following for passwords:
					 An eight character minimum and 64 character maximum length
					 The ability to use all special characters but no special requirement to use them
					 Restrict sequential and repetitive characters (e.g. 12345 or aaaaaa)
					 Restrict context specific passwords (e.g. the name of the site, etc.)
					 Restrict commonly used passwords (e.g. p@ssw0rd, etc.)"""
					 )
			
			randpwd = random_password(None)
			logging.info("suggesting random passowrd")
			print("\n\nRecommended password: %s\n"%(randpwd.generate_password()))
			logging.info("taking user's password input")
			self.user_password = input('Create Password: ')
			retry_password = input('Re-type password: ')
			logging.info('comparing the password')
			if self.compare(self.user_password, retry_password):
				logging.info('passwords match')
				return self.user_password
			else:
				logging.error("passwords don't match. Closing the program")
				raise ValueError("Passwords don't match. Try again. ")

	def compare(self,p1,p2):
		logging.info('actual logging function called (compare function)')
		if p1 == p2:
			return True
		else:
			return False
		


class random_password:
	""" This class is responsible for generating random password using the function.
		It also keeps in mind the nist guidelines. It is strongly recommend to use a strong password.
		Following are the details of the function:
		random_length function is responsible for creating a random length for the password.
		generate_password function is responsible for actually generating a password.
		juggler is the reason for the randomness of the password. It basically juggles the password."""
	def __init__(self, random_password):
		self.random_password = random_password
		
	
	def random_length(self):
		logging.info('getting the random length of password')
		return int(random.randrange(4,8))
	
	def generate_password(self):
		special = string.punctuation
		p1 = ''.join(random.choices(string.ascii_letters, k=self.random_length()))
		p2 = ''.join(random.choices(special,k=4))
		p3 = ''.join(random.choices(string.digits,k=self.random_length()))
		p4 = ''.join(random.choices(string.ascii_letters, k=self.random_length()))
		p5 = ''.join(random.choices(string.digits,k=self.random_length()))
		logging.info('generated the random password')
		self.random_password =  p1 + p2 + p3 + p4 + p5
		logging.info('password will be juggled')
		return self.juggler()
		 
		
		
	def juggler(self):
		logging.info('actual juggling function called')
		tmp = []
		for i in self.random_password:
			tmp.append(i)
		random.shuffle(tmp)
		logging.info('juggled succesfully')
		return ''.join(tmp)

class valid_check:
	""" This class is responsible for the the sanity check of password. Class checks if 
		the user's input password follows the NIST guidelines. If password doesn't follow the guidelines
		a corresponding error is raised by the password_sanity function. """

	def __init__(self,user_password):
		self.user_password = user_password
			
	def password_sanity(self):
		if len(self.user_password) <= 8:
			logging.error('Failed because of length error.')
			raise custom_error('lengtherror')
	
		elif not re.search("([A-Z])",self.user_password):

			logging.error('Failed because of upper case error')
			raise custom_error('uppercase')
	
	
		elif not re.search("([0-9])",self.user_password):
			logging.error('Failed because of number error')
			raise custom_error('numbererror')
	
	
		elif re.match("^[a-zA-Z0-9_]*$", self.user_password):
			logging.error('Failed because of special case error')
			raise custom_error('specialchar')

			
		else:
			logging.info('password is sanity checked')
			return True





class option:
	def __init__(self,numb=None, passphrase =None, conn =None):
		if type(numb) == int:
			self.numb = numb
		
		else:
			raise custom_error('intval')
		

		self.passphrase = passphrase
		self.conn = conn

	
	def select_op(self):
		if self.numb == 1:
			uname = input('Username: ')
			passwd = input('Password: ')
			comment = input('Description: ')
			while True:
				if not uname:
					print('Username Cannot be empty. Press "q" to go back to the menu.')
					uname = input('Username: ')
				elif uname.lower() == "q": return False
				elif uname: break
				else:
					aesgcm = AES_encryption(passwd, filepath= pathdir)
					aesgcm.encrypt()
					raise ValueError('Wrong Input')


			while True:
				if not passwd:
					print('Password cannot be empty. Press "q" to go back to the menu.')
					passwd = input("Password: ")
				elif passwd.lower() == "q":  return False
				elif passwd: break
				else:
					aesgcm = AES_encryption(passwd,filepath= pathdir)
					aesgcm.encrypt()
					raise ValueError('Wrong Input')


			if comment.lower() == "q": return False

			aesgcm = AES_encryption(self.passphrase, db_data=passwd,filepath= pathdir)
			enc_data = b64encode(aesgcm.encrypt_data())
			insert_q = db_ops(username=uname,password=enc_data.decode('utf-8'), comments=comment, conn=self.conn)
			insert_q.insert()
			print('Successfully inserted')
			time.sleep(2)
			
			
		elif self.numb == 2:
			show = show_data(conn=self.conn)
			show.show_db()


		elif self.numb == 3:
			passwd = getpass('Please provide password: ')
			while True:
				if not passwd:
					print('Password cannot be empty. Press "q" to quit.')
					passwd = getpass('Please provide password: ')
				elif passwd.lower() == "q": return False
				else: break

			try:
				show = show_data(passphrase=passwd, conn=self.conn, filepath=pathdir)
				show.dec_show_db()
			except ValueError as e:
				print('Wrong password. Try Again.')
				return False

		elif self.numb == 4:
			id_input = input('Provide id number: ')
			while True:
				try:
					if int(id_input):
						break
					else:
						id_input = input('Wrong value. Please try again: ')
				except ValueError as e:
					id_input = input('Wrong value. Please try again: ')
			deleter = db_ops(id=int(id_input), conn=self.conn)
			deleter.delete_val()
			
			
		elif self.numb == 5:
			id_no = input('Provide ID number: ')
			while True:
				try:
					if int(id_no):
						break
					else:
						id_no = input('Wrong value. Please try again: ')
				except ValueError as e:
					id_no = input('Wrong value. Please try again: ')
			
			
			
			choice = input('\n\nSelect 1 to update username\nSelect 2 to update password\nSelect 3 to update both\n\nOption: ')
			while True:
				try:
					if int(choice) in range(1,4):
						break
					else:
						choice = input('Wrong value. Please try again: ')
				except ValueError as e:
					choice = input('Wrong value. Please try again: ')



			if int(choice) == 1:
				uname = input('Provide New username: ')
				while True:
					if uname: break
					else:
						uname = input('Username cannot be empty: ')
						
						
				dbops = db_ops(id=int(id_no),username=uname,flag=int(choice), conn=self.conn)
				dbops.update_val()
				
			elif int(choice) == 2:
				passwd = input('Provide New Password: ')
				while True:
					if passwd: break
					else:
						passwd = input('Password cannot be empty: ')
						
				aesgcm = AES_encryption(self.passphrase, db_data=passwd, filepath= pathdir)
				enc_data = b64encode(aesgcm.encrypt_data())
				dbops = db_ops(id=int(id_no),password=enc_data.decode('utf-8'),flag=int(choice), conn=self.conn)
				dbops.update_val()
			
			elif int(choice) == 3:
				uname = input('Provide New username: ')
				passwd = input('Provide New Password: ')
				while True:
					if uname and passwd: break
					
					else:
						if not uname and passwd:
							uname = input('Username cannot be empty: ')
						elif not passwd and uname:
							passwd = input('Password cannot be empty: ')
						
						elif not uname and not passwd:
							uname = input('Username cannot be empty: ')
							passwd = input('Password cannot be empty: ')
				
				
				aesgcm = AES_encryption(self.passphrase, db_data=passwd, filepath= pathdir)
				enc_data = b64encode(aesgcm.encrypt_data())			
				dbops = db_ops(id=int(id_no),username=uname,password=enc_data.decode('utf-8'),flag=int(choice), conn=self.conn)
				dbops.update_val()
			
		elif self.numb == 6:
			clear_old_encrypted_file()
			dbops = db_ops(filepath=pathdir,conn=self.conn)
			dbops.dumps()
			aesgcm = AES_encryption(self.passphrase, filepath= pathdir)
			aesgcm.encrypt()
			sys.exit('GoodBye!')
			
		elif self.numb == 7:
			inp = input('Data will not be recoverable. Do you wish to conitnue?(Y/N) or "q" to quit: ')
			while True:
				if inp.lower() in ('y','n','q'): break
				else:
					print('Not a valid input. Try again.')
					inp = input('Data will not be recoverable. Do you wish to conitnue?(Y/N) or "q" to quit: ')



			if inp.lower() == "q" or inp.lower() == "n": return False
			else:
				logging.warning('purge option selected by input, all data will be lost')
				self.conn = None

				clear_old_encrypted_file()
				metafile = os.path.join(pathdir, 'metadata.json')
				obj1 = purge_data(metafile)
				obj1.shred()
				os.unlink(metafile)
				print('Succesfully purged')
				sys.exit('Exiting...')


		else:
			clear_old_encrypted_file()
			dbops = db_ops(filepath=pathdir,conn=self.conn)
			dbops.dumps()
			aesgcm = AES_encryption(self.passphrase, filepath= pathdir)
			aesgcm.encrypt()
			raise custom_error('wrongop')


class display_op:
	def __init__(self,val=None):
		self.val = val
		
	def show_options(self):
		self.val = input("""\n\nSelect from below options: \n
1. To insert new username and password
2. To show current username and password (encrypted)
3. To show current username and password (unencrypted)
4. To Delete Specific value
5. To Update Specific value
6. Quit
7. Purge Files (Data will not be recoverable)\n
Option:	""")
		return self.validation_check()
		

	def validation_check(self):
		while True:
			try:
				if int(self.val) not in range(1,8):
					self.val = input('Not a valid option, Try Again: ')
				else:
					break
			except ValueError as e:
				#raise custom_error('intval')
				self.val = input('Not a valid option, Try Again: ')
			
		self.val = int(self.val)
		return self.val


def main():
	"""This main class checks if the metadata already exists. It performs the actions according to
	the availability of the metadaa file. You don't have to worry about this main function """
	try:
		newfilepath = os.path.join(pathdir,'metadata.json')
		if not os.path.exists(newfilepath):
			logging.info('###### Running the program for the first time #######')
			logging.info('Started')
			new_passwd = Password() #Generating password for user according to the nist parameters
			passwd = new_passwd.create_password() #only first time
			logging.info('validity of password will be checked')
			foo = valid_check(passwd)
			logging.info('calling password sanity check function')
			if foo.password_sanity():
				logging.info('Initializing Database')
				db = db_ops(filepath=pathdir)
				db.create()
				logging.info('Creating table')
				#db.create_table()
				logging.info('Generating Key encryption key')
				KEK_gen = argon_hash(passwd,filepath=pathdir)
				KEK_gen.hashvalue()
				logging.info('Generating key1')
				master_k = gen_master_key()
				master_k.master_key_val()
				logging.info('Generating key2')
				MAC_key = gen_MAC_key()
				MAC_key.MAC_master_val()
				logging.info('wrapping keys')

				wrapped_data = key_wrap(master_k.master_key, MAC_key.MAC_master, KEK_gen.KEK,filepath=pathdir)
				wrapped_data.aes_key_wrap_func()
				logging.info('storing intergrity')
				integrity = file_integrity(key=MAC_key.MAC_master,filepath=pathdir)
				integrity.generate_integrity()
				logging.info('Reseting keys')
				aesgcm = AES_encryption(passwd, filepath= pathdir)
				aesgcm.encrypt()
				master_k.master_key = None
				MAC_key.MAC_master = None
				print('Database initialized. Login again')
		
		else:
			logging.info('Started after inititalization')
			logging.info('Will prompt for password')
			passwd = getpass('Enter Password: ')
			logging.info('calling the authencation class')
			auth = authentication(passwd)
			logging.info('Authenticating')
			if auth.login():
				logging.info('authentication succesful')
				try:
					logging.info('locating metadata')
					if not os.path.isfile('dump.sql'):
						logging.info('found the required metadata file')
						logging.info('Decryption database file')
						dec_obj = AES_decryption(passwd,filepath=pathdir)
						logging.info('returning the db structure')
						struct_data = dec_obj.decrypt()
						logging.info('loading the db and getting the sqlite3 connection')
						load_db = db_ops(filepath=pathdir,struct=struct_data)
						dbcon = load_db.load()
						logging.info('succesfully got the sqlite3 connection')
						logging.info('clearing structure from memory')
						struct_data = None
						logging.info('structure cleared')
						logging.info('Decrypted database file')
						logging.info('Generating KEK.')
						logging.info('displaying the options')
						foo = display_op()
						while True:
							option_val = foo.show_options()
							select_option = option(option_val, passwd, conn = dbcon)
							select_option.select_op()
					else:
						logging.error("Previously program has been killed by the user and system wasn't able to perform cleanup.")
						aesgcm = AES_encryption(passwd, filepath= pathdir)
						aesgcm.encrypt()
						sys.exit('Cleanup done. Login again. Check log file for further details.')

				except (KeyboardInterrupt, EOFError) as p:
					logging.error('signal detected after login')
					clear_old_encrypted_file()
					dbops = db_ops(filepath=pathdir,conn=dbcon)
					dbops.dumps()
					aesgcm = AES_encryption(passwd, filepath= pathdir)
					aesgcm.encrypt()
					print('exiting..')
			else:
				logging.error('Authentication failed. Wrong password or file integrity changed')
			
		
	except custom_error as e:
		logging.error('custom error')
		print(e)
	
	except UnboundLocalError as p:
		logging.error('Filename doesnt exist error')
		print("File doesn't exist")
	
	except (KeyboardInterrupt, EOFError) as q:
		logging.error('Signal detected')
		print('exiting..')
	
	
	
	
if __name__ == "__main__":
	main()