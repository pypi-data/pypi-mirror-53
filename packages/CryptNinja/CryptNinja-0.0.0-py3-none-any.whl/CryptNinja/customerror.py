#!/usr/bin/env python3

class custom_error(Exception):
	def __init__(self,type):
		self.type = type		
		
	def __str__(self):
		if self.type == 'lengtherror':
			return 'Length of password should be at least 8 characters.'
		elif self.type == 'specialchar':
			return 'At least one special character is required in password.'
		elif self.type == 'uppercase':
			return 'Uppercase characters are required.'
			
		elif self.type == 'numbererror':
			return 'At least one numeric character is required.'
			
		elif self.type == "fileobject":
			return 'file object required'
			
		elif self.type == "missing":
			return 'Missing id number'
			
		elif self.type == "miscred":
			return 'Username or Password Missing'
			
		elif self.type == 'wrongop':
			return 'Wrong option selected'
			
		elif self.type == 'intval':
			return 'Integer value allowed'
		elif self.type == 'oops':
			return 'Something went wrong'