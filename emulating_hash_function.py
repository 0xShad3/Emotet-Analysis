import ctypes
import sys
import json
from optparse import OptionParser


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def DLLHashFunction(dllName):
    hashDLLName = ctypes.c_uint(0)
    for i in dllName:
        if ord(i) >= 0x41 and ord(i) <= 0x5a:
            i = chr(ord(i) + 32)
        hashDLLName.value = (hashDLLName.value << 16) + \
            (hashDLLName.value << 6) + ord(i) - hashDLLName.value
    return hashDLLName.value ^ 0x9623f0


def NameHashFunction(function):
    hashName = ctypes.c_uint(0)
    for i in range(len(function)):
        hashName.value = (hashName.value << 16) + \
            (hashName.value << 6) + ord(function[i]) - hashName.value
    return hashName.value ^ 0x26e731b1


def crackDLLHash(dllHash):
    f = open("CommonDLLNames.txt", "r")
    while True:
        dllName = f.readline().strip("\n")
        if len(dllName) == 0:
            print(
                colors.RED + "[-] DLL hash couldnt be cracked, hash used : 0x{:x}".format(dllHash) + colors.ENDC)
            return None
        dllName += ".dll"
        if DLLHashFunction(dllName) == dllHash:
            print(colors.GREEN + "[+] DLL name cracked [ {:s} ] hash used : 0x{:x}".format(
                dllName, dllHash) + colors.ENDC)
            return dllName


def crackFunctionHash(funcNameHash, dllName):
    f = open("./dllCrack/" +dllName[:-4] + "funcnames.txt", "r")
    while True:
        apimethod = f.readline()
        if len(apimethod) == 0:
            print(colors.RED + "[-] Function hash couldnt be cracked, hash used : 0x{:x}".format(funcNameHash) + colors.ENDC)
            break

        if NameHashFunction(apimethod.strip('\n')) == funcNameHash:
            print(colors.GREEN + "[+] Function name cracked [ {:s} ] hash used 0x{:x}".format(
                apimethod.strip('\n'),
                funcNameHash) + colors.ENDC
            )
            break
    f.close()

def write_json(data,filename):
    try:
        with open(filename,'w') as f:
            json.dump(data,f,indent=4)
    except IOError, e:
        print(colors.RED + str(e) + colors.ENDC)
        filename = input(color.WARNING + "[+] Enter filename to store the DB:"+ colors.ENDC)
        write_json(filename)

def read_json(filename):
    try:
        with open(filename,'r') as f:
            return json.read(data,f,indent=4)
    except IOError, e:
        print(colors.RED + str(e) + colors.ENDC)
        filename = input(color.WARNING + "[+] Enter filename to store the DB:"+ colors.ENDC)
        return return_json(filename)

def interactiveDecryption():

    while True:
        print("Commands supported")
def main():
    optionparser = OptionParser()
    optionparser.add_option("-l", "--library",
                            default=None,
                            type="int",
                            action="store",
                            dest="DLL",
                            help="Provide the hash of the function to search for."
                            "This is required!")
    optionparser.add_option("-f", "--function",
                            default=None,
                            type="int",
                            action="store",
                            dest="FUNC",
                            help="Provide the hash of the dll file name to search for."
                            "This is required!")
    optionparser.add_option("-i", "--shell",
                            default=None,
                            type="bool",
                            action="store",
                            dest="SHELL",
                            help="Set this option to True to enter interactive decryption mode."
                            )
    (options, args) = optionparser.parse_args()
    
    if options.SHELL:
        print(colors.OKBLUE + "[+] Entering interactive mode" + colors.ENDC)
        interactiveDecryption()

    if options.DLL == None or options.FUNC == None:
        print("Use --help to check for usage.")
        sys.exit()

    dllName = crackDLLHash(options.DLL)
    if dllName == None:
        print(
            colors.RED + "[-] Exiting!" + colors.ENDC)
        sys.exit()

    crackFunctionHash(options.FUNC, dllName)


if __name__ == "__main__":
    main()
