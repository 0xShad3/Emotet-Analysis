'''
	@author: Angelos T. Kalaitzidis
	IDAPython script to extract the 2 out of the 3 encrypted tables in decrypted form
	
'''

decrypt_function_name = 'decryptLibraryXOR'

def get_password(address):
	membytes = get_bytes(address,4) # assuming unsigned integer
	password = ''
	for i in range(len(membytes)):
		password += membytes[::-1][i]
	return password

def get_encrypted_little_endian(address):
	offset = address
	offset += 2 * 4 # 2 * sizeof(int)
	encrypted = get_bytes(offset,4)
	return encrypted[::-1]

def get_limit_counter(address):
	deobf1 = get_bytes(address,4)
	deobf2 = get_bytes(address + 4,4)
	limit_s1 = 0
	for i in range(len(deobf1)):
		limit_s1 += (ord(deobf1[i]) ^ ord(deobf2[i])) * 16 **i
	
	return limit_s1


def get_ciphertext(ptr):
	if print_insn_mnem(ptr) == 'mov' and 'ecx' in print_operand(ptr,0):
		return get_operand_value(ptr,1)

def decrypt(address):
	limit = get_limit_counter(address)
	password = get_password(address)
	decrypted_mem = ""
	decrypted_block = ""
	cnt = 0

	while True:
		
		if cnt >= 0x100:	
			return decrypted_mem[:limit]
		
		#if '0' in decrypted_block:
		#		return decrypted_mem
		encrypted = get_encrypted_little_endian(address)		
		for i in range(len(password)):
			decrypted_block += chr(ord(password[i]) ^ ord(encrypted[i]))
		
		decrypted_mem += decrypted_block[::-1]
		
		encrypted = ""
		decrypted_block = ""
		address += 4
		cnt += 1	

print "[+] Decryption phase 1"
ea_start_1 = 0x40d000
ea_end_1 = 0x40d35f

for ea in range(ea_start_1,ea_end_1):
	for xref in XrefsTo(ea,flags=0):
		print ("0x{:x} => {:s}".format(ea, decrypt(ea)))

print "[+] Decryption phase 2"

ea_start_2 = 0x40d7e0
ea_end_2 = 0x40db2f

for ea in range(ea_start_2,ea_end_2):
	for xref in XrefsTo(ea,flags=0):
		print ("0x{:x} => {:s}".format(ea, decrypt(ea)))
		break
"""def isCodeXREF(address):
	if CodeRefsTo(address,0)[0]:
		return hex(address)
	else:
		return 0"""