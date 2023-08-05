#!/usr/bin/env python3

class purge_data:
	def __init__(self,purge):
		self.purge = purge
		
	def shred(self):
		data = "01"
		count = 2
		f = open(self.purge,'rb+')
		f.read()
		count = f.tell()
		data = data*(int(count/2))
		data = data.encode('utf-8')

		f.seek(0)
		f.write(data)
		f.close()