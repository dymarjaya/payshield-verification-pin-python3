from binascii import * 
    
def padding(var, pad_len, pad_char):
    length = len(var)
    var += pad_char*(pad_len-length)
    return var

def xor(b1, b2): 
    parts = []
    for b1, b2 in zip(b1, b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)
		
def padding(var, pad_len, pad_char):
    length = len(var)
    var += pad_char*(pad_len-length)
    return var

def genPINData(PIN):
    pinData = ("%02d%s" % (len(PIN), PIN))
    return padding(pinData, 16, 'F')
	
def genSerialData(AccountNumber):
    return ('0000' + AccountNumber)
	
def genPINBlock(PIN, AccountNumber):
    pinData = genPINData(PIN)
    serialData = genSerialData(AccountNumber)
    return xor(unhexlify(pinData), unhexlify(serialData))
