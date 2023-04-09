import sys
from optparse import OptionParser
from pathlib import Path
from Crypto.Util.Padding import unpad   
from Crypto.Cipher import DES3
from binascii import unhexlify 
from .firepwd import getKey, getLoginData

CKA_ID = unhexlify('f8000000000000000000000000000001')

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-v", "--verbose", type="int", dest="verbose", help="verbose level", default=0)
    parser.add_option("-p", "--password", type="string", dest="masterPassword", help="masterPassword", default='')
    parser.add_option("-d", "--dir", type="string", dest="directory", help="directory", default='')
    (options, args) = parser.parse_args()
    options.directory = Path(options.directory)

    key, algo = getKey(  options.masterPassword.encode(), options.directory, options.verbose )
    if key==None:
        sys.exit()
    #print(hexlify(key))
    logins = getLoginData(options.directory, options.verbose)
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
            print ( unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 ), end=',')
            iv = i[1][1]
            ciphertext = i[1][2] 
            print ( unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 ) )


if __name__ == '__main__':
    main()
