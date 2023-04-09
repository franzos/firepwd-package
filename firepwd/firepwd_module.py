import sys
from pathlib import Path
from typing import List
from Crypto.Util.Padding import unpad   
from Crypto.Cipher import DES3
from binascii import unhexlify
from dataclasses import dataclass
from .firepwd import getKey, getLoginData

@dataclass
class FirepwdResult:
    url: str
    login: str
    password: str

CKA_ID = unhexlify('f8000000000000000000000000000001')

def Firepwd(password: str, path: str, verbose: int = 0):
    results: List[FirepwdResult] = []

    encoded_password = password.encode()
    pure_path = Path(path)

    key, algo = getKey(encoded_password, pure_path, verbose)
    if key==None:
        sys.exit()
    #print(hexlify(key))
    logins = getLoginData(pure_path, verbose)
    if len(logins)==0:
        print ('no stored passwords')
    else:
        print ('decrypting login/password pairs' ) 
    if algo == '1.2.840.113549.1.12.5.1.3' or algo == '1.2.840.113549.1.5.13':  
        for i in logins:
            assert i[0][0] == CKA_ID
            print ('%20s:' % (i[2]),end='')  #site URL
            iv = i[0][1]
            ciphertext = i[0][2] 
            login = unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 )
            print ( login, end=',')
            iv = i[1][1]
            ciphertext = i[1][2]
            password = unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 )
            print ( password )

            results.append(FirepwdResult(
                url=i[2],
                login=login.decode(),
                password=password.decode()
            ))

    return results