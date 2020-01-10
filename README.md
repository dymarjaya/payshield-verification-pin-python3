# verification-pin-thales-payment-hsm

## Verifikasi PIN dengan Thales payment HSM 
Program ini mendemonstrasikan secara sederhana bagaimana melakukan verifikasi PIN menggunakan Thales payment HSM. Program ini support untuk Thales payment HSM dengan tipe RG 7000, HSM 8000, payShield 9000 dan payShield 10K.

### Alur Kerja
Berikut topologi sederhana pada program ini:

```
+------------------+        +------+       +-----+
| TERMINAL(ATM/EDC)|  <---> | HOST | <---> | HSM |
+------------------+        +------+       +-----+
```

Capture data kartu dan input PIN dilakukan di terminal (misalnya pada ATM/EDC). Kemudian data tersebut dikalkulasi menjadi PIN Block dan dienkrip menggunakan terminal PIN key (TPK) yang ada di terminal. Data yang sudah aman ini kemudian dikirim ke host. Host terhubung dengan HSM untuk melakukan proses kriptografi yang diperintahkan (misalnya membuat PIN offset, menganti PIN offset ataupun verifikasi PIN).

### Catatan
Beberapa catatan mengenai demo program ini:
1. Program ini dibuat untuk tujuan edukasi dan dibangun dengan python 3
2. LMK yang digunakan adalah LMK Test
3. Semua working key yang digunakan sudah di-generate sebelumnya
4. Tempat penyimpanan data PIN offset pada sisi host menggunakan text file

### Penggunaan
> Pastikan anda telah melakukan konfigurasi IP address dan port HSM pada kode sebelum menjalankan program ini. 
Sebagai contoh, IP address yang digunakan dalam kode ini adalah 192.168.1.100 dan port 1500. 
Anda dapat menggantinya sesuai setting yang anda gunakan.

Konfigurasi IP address dan port HSM dapat anda temukan dalam kode pada baris berikut:
```python
#HSM connection configuration
TCP_IP = '192.168.1.101'
TCP_PORT = 1500
```

Berikut beberapa tahapan sebelum melakukan verifikasi PIN:
1. Generate PIN Offset
2. Change PIN Offset (jika ingin melakukan perubahan PIN)
3. Verification PIN

Berikut cara menjalankan programnya:

1. Generate PIN Offset: Inputkan Nomor Kartu dan PIN nya.
```
> python genpinoffset.py 4579230000004312 111111
###################
GENERATE PIN OFFSET
###################

TERMINAL SIDE
-------------
[+]AccountNumber: 4579230000004312
[+]PIN: 111111
[+]PINBlock: 06118321FFFFFBCE
[+]e(PINBlock)TPK: 51D392627E88EB18

HOST SIDE
---------
>>>Send host command to HSM...
00000000: 00 86 31 32 33 34 42 4B  30 30 32 54 45 46 46 32  ..1234BK002TEFF2
00000010: 37 30 43 33 33 30 31 30  31 43 32 44 36 42 32 33  70C330101C2D6B23
00000020: 44 46 37 32 45 41 38 46  46 45 42 44 30 45 34 39  DF72EA8FFEBD0E49
00000030: 31 44 36 32 45 32 45 33  44 31 35 31 39 42 33 39  1D62E2E3D1519B39
00000040: 35 46 42 39 46 45 35 46  30 37 44 41 35 31 44 33  5FB9FE5F07DA51D3
00000050: 39 32 36 32 37 45 38 38  45 42 31 38 30 31 30 36  92627E88EB180106
00000060: 39 32 33 30 30 30 30 30  30 34 33 31 33 34 35 36  9230000004313456
00000070: 37 38 39 30 31 32 33 34  35 36 37 38 39 32 33 30  7890123456789230
00000080: 30 30 30 4E 30 34 33 31                           000N0431

<<<Receive response command from HSM...
00000000: 00 14 31 32 33 34 42 4C  30 30 33 32 38 30 36 34  ..1234BL00328064
00000010: 46 46 46 46 46 46                                 FFFFFF

[!]Generate PIN Offset Success
[+]Error Code = 00
[+]PIN Offset: 328064
```

2. Change PIN: Inputkan Nomor kartu, PIN lama, dan PIN yang baru.
```
> python changepin.py 4579230000004312 111111 123456
##########
CHANGE PIN
##########

TERMINAL SIDE
-------------
[+]TPK: 8A62CEFD4F3E296E31EFD38A680E6B7532BF0BAD1A898A51
[+]AccountNumber: 4579230000004312
[+]Old PIN: 111111
[+]Old PINBlock: 06118321FFFFFBCE
[+]e(Old PINBlock)TPK: 51D392627E88EB18
[+]New PIN: 123456
[+]New PINBlock: 0612A666FFFFFBCE
[+]e(New PINBlock)TPK: EEC12744E8F13E16

HOST SIDE
---------
>>>Send host command to HSM...
00000000: 00 A2 31 32 33 34 44 55  30 30 32 54 45 46 46 32  ..1234DU002TEFF2
00000010: 37 30 43 33 33 30 31 30  31 43 32 44 36 42 32 33  70C330101C2D6B23
00000020: 44 46 37 32 45 41 38 46  46 45 42 44 30 45 34 39  DF72EA8FFEBD0E49
00000030: 31 44 36 32 45 32 45 33  44 31 35 31 39 42 33 39  1D62E2E3D1519B39
00000040: 35 46 42 39 46 45 35 46  30 37 44 41 35 31 44 33  5FB9FE5F07DA51D3
00000050: 39 32 36 32 37 45 38 38  45 42 31 38 30 31 30 36  92627E88EB180106
00000060: 39 32 33 30 30 30 30 30  30 34 33 31 33 34 35 36  9230000004313456
00000070: 37 38 39 30 31 32 33 34  35 36 37 38 39 32 33 30  7890123456789230
00000080: 30 30 30 4E 30 34 33 31  33 32 38 30 36 34 46 46  000N0431328064FF
00000090: 46 46 46 46 45 45 43 31  32 37 34 34 45 38 46 31  FFFFEEC12744E8F1
000000A0: 33 45 31 36                                       3E16

<<<Receive response command from HSM...
00000000: 00 14 31 32 33 34 44 56  30 30 33 33 30 33 30 39  ..1234DV00330309
00000010: 46 46 46 46 46 46                                 FFFFFF

[!]Change PIN Success
[+]Error Code = 00
[+]New PIN Offset: 330309
```

3. Verification PIN: Inputkan Nomor kartu dan PIN yang valid.
```
> python verpin.py 4579230000004312 123456
################
PIN VERIFICATION
################

TERMINAL SIDE
-------------
[+]TPK: 8A62CEFD4F3E296E31EFD38A680E6B7532BF0BAD1A898A51
[+]AccountNumber: 4579230000004312
[+]PIN: 123456
[+]PINBlock: 0612A666FFFFFBCE
[+]e(PINBlock)TPK: EEC12744E8F13E16

HOST SIDE
---------
>>>Send host command to HSM...
00000000: 00 91 31 32 33 34 44 41  54 45 46 46 32 37 30 43  ..1234DATEFF270C
00000010: 33 33 30 31 30 31 43 32  44 36 42 32 33 44 46 37  330101C2D6B23DF7
00000020: 32 45 41 38 46 46 45 42  44 30 45 34 39 31 44 36  2EA8FFEBD0E491D6
00000030: 32 45 32 45 33 44 31 35  31 39 42 33 39 35 46 42  2E2E3D1519B395FB
00000040: 39 46 45 35 46 30 37 44  41 31 32 45 45 43 31 32  9FE5F07DA12EEC12
00000050: 37 34 34 45 38 46 31 33  45 31 36 30 31 30 36 39  744E8F13E1601069
00000060: 32 33 30 30 30 30 30 30  34 33 31 33 34 35 36 37  2300000043134567
00000070: 38 39 30 31 32 33 34 35  36 37 38 39 32 33 30 30  8901234567892300
00000080: 30 30 4E 30 34 33 31 33  33 30 33 30 39 46 46 46  00N0431330309FFF
00000090: 46 46 46                                          FFF

<<<Receive response command from HSM...
00000000: 00 08 31 32 33 34 44 42  30 30                    ..1234DB00

[!]Verification PIN Success
[+]Error Code = 00
```
