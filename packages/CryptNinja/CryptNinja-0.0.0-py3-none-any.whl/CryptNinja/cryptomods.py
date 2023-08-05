#!/usr/bin/env python3


# Warning: This is a “Hazardous Materials” module. You should ONLY use it if you’re 100% absolutely sure that
# you know what you’re doing because this module is full of land mines, dragons, and dinosaurs with laser guns.

from argon2.low_level import hash_secret
from getpass import getpass
import uuid
from base64 import b64encode,b64decode
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.keywrap import aes_key_wrap
from cryptography.hazmat.primitives.keywrap import aes_key_unwrap
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.keywrap import InvalidUnwrap
from argon2.low_level import Type
import json, os, sys
import hashlib
import hmac
from hmac import compare_digest
from .purge import purge_data
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
class file_integrity:
    """This class is responsible for file integrity. generate_integrity function generate the hash for data file"""
    def __init__(self, key=None, filepath=None):
        if not key:
            raise ValueError('Key value required')
        else:
            self.key = key

        if filepath:
            self.filepath = filepath

    def generate_integrity(self):
        logging.info('integrity check begins')
        keypath = os.path.join(self.filepath, 'keys.file')
        with open(keypath, 'rb+') as key_file:
            data = json.loads(key_file.read())
            data = bytes(json.dumps(data), 'utf-8')
            hash_attr = hmac.new(self.key,data, hashlib.sha512)
            hexdigest = hash_attr.hexdigest()
            data = json.loads(data)
            data['version_hash'] = hexdigest
            newfile = os.path.join(self.filepath, 'new_key_file')
            f = open(newfile,'w')
            print(json.dumps(data, indent=4),file=f)
            f.close()
        key_file.close()
        pur = purge_data(keypath)
        pur.shred()
        os.unlink(keypath)
        metafile = os.path.join(self.filepath, 'metadata.json')
        os.rename(newfile,metafile)
        logging.info('generated the hash and saved succesfully')
        




class argon_hash:
    """ This class generates the data file and argon hash for keys. """
    def __init__(self, cleartext, KEK= None, data_json = {},filepath=None):

        self.cleartext = cleartext
        if KEK:
            raise ValueError
        else:
            self.KEK = KEK
            self.data_json = {
                            "time_cost": None,
                            "memory_cost": None,
                            "parallelism": None,
                            "salt": None,
                            "hash_len": None,
                            "MAC_key": None,
                            "Master_key": None,
                            "version_hash": None
            }

        if filepath:
            self.filepath = filepath



    def hashvalue(self):
        logging.info('generating the argon hash')
        self.data_json['time_cost'] = 16
        self.data_json['hash_len'] = 24
        self.data_json['memory_cost'] = 128
        self.data_json['parallelism'] = 16
        self.cleartext = bytes(self.cleartext, 'utf-8')
        self.data_json['salt'] = get_random_bytes(64)
        hash_val = hash_secret(self.cleartext,self.data_json['salt'],memory_cost = self.data_json['memory_cost'],time_cost=self.data_json['time_cost'], hash_len=self.data_json['hash_len'],parallelism=self.data_json['parallelism'], type=Type.ID)
        self.data_json['salt'] = b64encode(self.data_json['salt'])
        self.data_json['salt'] = self.data_json['salt'].decode('utf-8')
        tmpkey = os.path.join(self.filepath, 'tmp_keys.file')
        f = open(tmpkey, 'w')
        f.write(json.dumps(self.data_json,indent=4))
        f.close()
        self.KEK = hash_val.decode('utf-8').split('$')[-1]
        logging.info('succesfully generated the argon hash')


class gen_master_key:
    """ Generates the master key responsible for the encryption of the content. """
    def __init__(self, master_key=None):
        if master_key:
            raise ValueError('Not allowed to initialize Master key')
        else:
            self.master_key = master_key

    def master_key_val(self):
        logging.info('calling the function for random master key')
        self.master_key = get_random_bytes(16)
        #self.master_key =  b64encode(self.master_key)



class gen_MAC_key:
        """ Responsible for generating the MAC key responsible for other important features. """
        def __init__(self, MAC_master=None):
            if MAC_master:
                raise ValueError('Not allowed to intialize MAC master key')
            else:
                self.MAC_master = MAC_master


        def MAC_master_val(self):
            logging.info('calling the function for random mac key')
            self.MAC_master = get_random_bytes(16)
            #self.MAC_master = b64encode(self.MAC_master)

""" Functions and classes below are responsible for wrapping the keys, validation & integrity of data, 
    unwrapping of the keys, decryption & encryption of db files, content  and password. Section below is
    dangerous and contains landmines and dinosaurs with guns and lasers. Moreover i am very poor with document
    so, i leave it you guys and your intelligent brains to go through the below code and understand it.

"""

class validation_check:
    def __init__(self,key=None, filepath=None):
        if not key:
            raise ValueError('Key value required')
        else:
            self.key = bytes(key, 'utf-8')

        if filepath:
            self.filepath = filepath



    def kek_gen(self):
        metafile = os.path.join(self.filepath, 'metadata.json')
        f = open(metafile,'r')
        data_json = json.loads(f.read())
        hash_val = hash_secret(self.key,b64decode(data_json['salt']),memory_cost = data_json['memory_cost'],time_cost=data_json['time_cost'], hash_len=data_json['hash_len'],parallelism=data_json['parallelism'], type=Type.ID)
        f.close()
        return (hash_val.decode('utf-8').split('$')[-1], data_json['MAC_key'])
        

    def unwrapper(self):       
        backend = default_backend()
        res = self.kek_gen()
        kek = bytes(res[0], 'utf-8')
        MAC_key = b64decode(res[1])
        try:
            unwrapped_key = aes_key_unwrap(kek,MAC_key,backend)
            return unwrapped_key
        except InvalidUnwrap as e:
            logging.error('Invalid Password')
            sys.exit('Unauthorized access')

    def validate(self):
        metafile = os.path.join(self.filepath, 'metadata.json')
        with open(metafile,'rb') as json_key_file:
            data = json.loads(json_key_file.read())
            org_hex = data['version_hash']
            data['version_hash'] = None
            tmp = bytes(json.dumps(data), 'utf-8')
            new_key = self.unwrapper()
            hash_attr = hmac.new(new_key,tmp, hashlib.sha512)
            hexdigest = hash_attr.hexdigest()
            json_key_file.close()
            return compare_digest(hexdigest,org_hex)

class key_wrap:
    def __init__(self, mkey, mackey, wrapping_key, filepath=None):
        self.mkey = mkey
        self.mackey = mackey
        self.wrapping_key = bytes(wrapping_key, 'utf-8')
        self.filepath = filepath

    def aes_key_wrap_func(self):
        backend = default_backend()
        wrapped_mackey = aes_key_wrap(self.wrapping_key, self.mackey, backend) # wrapping mackey
        wrapped_mkey = aes_key_wrap(self.wrapping_key, self.mkey, backend)
        keyfile = os.path.join(self.filepath, 'keys.file')
        tmpkeyfile = os.path.join(self.filepath, 'tmp_keys.file')
        f = open(keyfile,'w+')
        with open(tmpkeyfile,'r+') as json_file:
            data = json.loads(json_file.read())
            data['MAC_key'] = b64encode(wrapped_mackey).decode('utf-8')
            data['Master_key'] = b64encode(wrapped_mkey).decode('utf-8')
            print(json.dumps(data,indent=4),file=f)
        json_file.close()
        f.close()

        pur = purge_data(tmpkeyfile)
        pur.shred()
        os.unlink(tmpkeyfile)
        
#Encryption and Decryption area                        

class AES_decryption: #file decryption class
    def __init__(self, password, db_data=None, filepath=None):
        if not password:
            raise ValueError('Missing password')
        else:
            self.password = bytes(password, 'utf-8')

        if db_data:
            self.db_data = b64decode(db_data)

        if filepath:
            self.filepath = filepath

    def getting_keys(self):
        metafile = os.path.join(self.filepath, 'metadata.json')
        f = open(metafile,'r')
        data_json = json.loads(f.read())
        hash_val = hash_secret(self.password,b64decode(data_json['salt']),memory_cost = data_json['memory_cost'],time_cost=data_json['time_cost'], hash_len=data_json['hash_len'],parallelism=data_json['parallelism'], type=Type.ID)
        f.close()
        return (hash_val.decode('utf-8').split('$')[-1], data_json['Master_key'], data_json['MAC_key'])


    def unwrapper_function(self):
        backend = default_backend()
        keys = self.getting_keys()
        kek = bytes(keys[0], 'utf-8')
        mkey_enc = b64decode(keys[1])
        mackey_enc = b64decode(keys[2])
        try:
            unwrapped_mackey = aes_key_unwrap(kek,mackey_enc,backend)
            unwrapped_mkey = aes_key_unwrap(kek,mkey_enc,backend)
            return (unwrapped_mackey,unwrapped_mkey)
        except InvalidUnwrap as e:
            logging.error('Invalid Password')
            raise ValueError('Unauthorized access')

    def generate_hmac(self, aad, nonce, key):
        data = aad + nonce #28 bytes
        hmac_val = hmac.new(key,data, hashlib.sha256)
        return hmac_val.digest() #32 bytes hash return

    def decrypt(self):
        dec_keys = self.unwrapper_function()
        mackey_unenc = dec_keys[0]
        mkey_unenc = dec_keys[1]
        for i in os.listdir(self.filepath):
            if '.' not in i and 'pycache' not in i and 'logs' not in i:
                filename = i

        if not filename:
            logging.error('File not found')
            sys.exit('File not found')
        else:
            dec_data = []
            uuidfile = os.path.join(self.filepath, filename)
            with open(uuidfile, 'rb') as fr:
                aad = uuid.UUID(filename)
                aad = aad.bytes
                while True:
                    data = fr.read(92)
                    if not data:
                        break
                    else:
                        hash = data[-32:]
                        act_data = data[12:-32:]
                        nonce = data[:12]
                        if compare_digest(hash, self.generate_hmac(aad, nonce, mackey_unenc)):
                            aesgcm = AESGCM(mkey_unenc)
                            dec = aesgcm.decrypt(nonce, act_data, aad)
                            dec_data.append(dec)
                        else:
                            raise ValueError('File has been tempered')
            fr.close()
            return b"".join(dec_data).decode('utf-8')


    def decrypt_data(self):
        dec_keys = self.unwrapper_function()
        mackey_unenc = dec_keys[0]
        mkey_unenc = dec_keys[1]
        aad = self.password
        nonce = self.db_data[:12]
        hash = self.db_data[-32:]
        act_data = self.db_data[12:-32:]
        if compare_digest(hash, self.generate_hmac(aad, nonce, mackey_unenc)):
            aesgcm = AESGCM(mkey_unenc)
            dec = aesgcm.decrypt(nonce, act_data, aad)
            return dec
        else:
            raise ValueError('Hash mismatch')

class AES_encryption(AES_decryption): #file encryption class
    def __init__(self, password, db_data=None, filepath=None):
        if password:
            self.password = bytes(password, 'utf-8')
        else:
            raise ValueError('Password requried')

        if db_data:
            self.db_data = bytes(db_data, 'utf-8')


        if filepath:
            self.filepath = filepath

    def encrypt(self):
        hold = []
        dec_keys = self.unwrapper_function()
        dumpsql = os.path.join(self.filepath, 'dump.sql')
        f = open(dumpsql,'rb')
        count = 0
        len_file = int(len(f.peek())/32)
        aad = uuid.uuid4()
        aad = aad.bytes #16 bytes
        mackey_unenc = dec_keys[0]
        mkey_unenc = dec_keys[1]
        while True:
            data = f.read(32)
            if not data:
                break
            else:
                if  count <= len_file:

                    nonce = get_random_bytes(12) #12
                    cipher = AESGCM(mkey_unenc)             
                    ct = cipher.encrypt(nonce, data, aad) #return 48 bytes
                    data = nonce + ct +  self.generate_hmac(aad, nonce, mackey_unenc) #12 + 48 + 32 

                    hold.append(data)

                    count += 1
                else:
                    break
    

        filename = uuid.UUID(bytes= aad)
        uuidfile = os.path.join(self.filepath, str(filename))    
        with open(uuidfile,'wb') as fq:
            fq.write(b"".join(hold))
        fq.close()
        f.close()
        pur = purge_data(dumpsql)
        pur.shred()
        os.unlink(dumpsql)
        del hold[:]

    def encrypt_data(self):
        dec_keys = self.unwrapper_function()
        mackey_unenc = dec_keys[0]
        mkey_unenc = dec_keys[1]
        nonce = get_random_bytes(12) #12
        aad = self.password #unknown bytes
        cipher = AESGCM(mkey_unenc)             
        ct = cipher.encrypt(nonce, self.db_data, aad)
        enc_db_data = nonce + ct + self.generate_hmac(aad, nonce, mackey_unenc) #12 +48 + 32
        return enc_db_data
