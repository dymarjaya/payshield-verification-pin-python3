# !/usr/bin/python3
# Author    : Mudito Adi Pranowo, David Abdurrahman
# Porting by: Mudito Adi Pranowo
# Company   : PT Dymar Jaya Indonesia
# This code demonstrate verification PIN offset using Thales payment HSM
# Note: Require cryptography library -> pip install cryptography
# Note: Require hexdump library -> pip install hexdump
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import string, socket, sys
from struct import *
from pyUtil import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hexdump import hexdump

if len(sys.argv) != 3:
    print ('Usage: %s <Card Number> <PIN> ' % (sys.argv[0]))
    print ('Example: %s 4579230000004312 123456' % (sys.argv[0]))
    sys.exit()
       
TPK = '8A62CEFD4F3E296E31EFD38A680E6B7532BF0BAD1A898A51'
k = unhexlify(TPK)

PINBlock = genPINBlock((sys.argv[2]),(sys.argv[1])[3:15])
cipher = Cipher(algorithms.TripleDES(k), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()
ct = encryptor.update(PINBlock) + encryptor.finalize()
ePINBlock = hexlify(ct).decode('UTF-8').upper()
        
print ('################')
print ('PIN VERIFICATION')
print ('################')
print ('')
print ('TERMINAL SIDE')
print ('-------------')
print ('[+]TPK:', TPK)
print ('[+]AccountNumber:', (sys.argv[1]))
print ('[+]PIN:', (sys.argv[2]))
print ('[+]PINBlock:', hexlify(PINBlock).decode('UTF-8').upper())
print ('[+]e(PINBlock)TPK:', ePINBlock)

print ('')
print ('HOST SIDE')
print ('---------')

#HSM connection configuration
TCP_IP = '192.168.1.101'
TCP_PORT = 1500

#Construct HSM command for Verification PIN
MHL = '1234'
HSMCMD = 'DA'
TPKLMK = 'TEFF270C330101C2D6B23DF72EA8FFEBD0E491D62E2E3D151'
PVKLMK = '9B395FB9FE5F07DA'
MaxPINL = '12'
PINBlockFCode = '01'
CheckLength = '06'
PANN = (sys.argv[1])[3:15]
DecTab = '3456789012345678'
PVD = (sys.argv[1])[3:10] + 'N' + (sys.argv[1])[11:15]

f = open (sys.argv[1] + '.txt' , 'r')
PINOffset = (f.readline()) + 'FFFFFF'
f.close()

#Sending Command to HSM
COMMAND = MHL + HSMCMD  + TPKLMK + PVKLMK + MaxPINL + ePINBlock + PINBlockFCode + CheckLength + PANN + DecTab + PVD + PINOffset
SIZE = pack('>h',len(COMMAND))
MESSAGE = SIZE + bytearray(COMMAND, 'UTF-8')

print ('>>>Send host command to HSM...')
hexdump(MESSAGE)

hsmSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hsmSocket.connect((TCP_IP, TCP_PORT))
hsmSocket.send(MESSAGE)

BUFFER_SIZE = 1024
data = hsmSocket.recv(BUFFER_SIZE)

print ('')
print ('<<<Receive response command from HSM...')
hexdump(data)

hsmSocket.close()

RSPNCD = int(data[8:10])
RSPNCS = str(data[8:10].decode('UTF-8'))

print ('')

if RSPNCD < 00:
    print ('[!]Verification PIN Failed')
    print ('[+]Error Code = ' + RSPNCS )
elif RSPNCD < 1 :
    print ('[!]Verification PIN Success')
    print ('[+]Error Code = ' + RSPNCS)
else:
    print ('[!]Verification PIN Failed')
    print ('[+]Error Code = ' + RSPNCS)

print ('')
