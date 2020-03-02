import subprocess
import sys
import time

DEBUG = 1

compressed = "last_flag"

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"


def tipo(compressed):
    print("Got type!")
    if DEBUG:
        time.sleep(1)
    return subprocess.Popen(["file", compressed], stdout=subprocess.PIPE).stdout.read().decode()

def position_new_flag(content):
    if DEBUG:
        print(f"CONTENT: {content}")
        print("Positioning new flag")
        time.sleep(1)

    if "flag.txt" in content:
        if DEBUG:
            print("From flag.txt to last_flag")
        subprocess.call(["mv","flag.txt","last_flag"])

    elif "last_flag" in content:
        if DEBUG:
            print("From last_flag to last_flag")
        subprocess.call(["mv","last_flag","last_flag"])

    elif "flag" in content:
        if DEBUG:
            print("From flag to last_flag")
        subprocess.call(["mv","flag","last_flag"])
    else:
        for _file in content:
            if ".out" in _file:
                if DEBUG:
                    print("From flag.out to last_flag")
                subprocess.call(["mv", "-v", "flag.out", "last_flag"])
                break

        print("ERROR: DID NOT FIND THE FLAG FILE\nPlease rename the compressed data to one of the following names:\nflag.txt\nlast_flag\nflag\nflag.out")

def redefine_type_and_extract(tipo):
    flag = "last_flag"
    global it

    if _posix_tar in tipo:
        flag += ".tar"
        subprocess.call(["mv", "-v", "last_flag", flag])
        subprocess.call(["tar", "-xvf", flag])
        subprocess.call(["rm", flag])
        if DEBUG:
            print("POSIX")
            time.sleep(1)
    elif _bzip2 in tipo:
        flag += ".bz2"
        subprocess.call(["mv", "-v", "last_flag", flag])
        subprocess.call(["bzip2", "-dvk", flag])
        subprocess.call(["rm", flag])
        if DEBUG:
            print("bzip2")
            time.sleep(1)
    elif _zip in tipo:
        flag += ".zip"
        subprocess.call(["mv", "-v", "last_flag", flag])
        subprocess.call(["unzip", flag])
        subprocess.call(["rm", flag])
        if DEBUG:
            print("ZIP")
            time.sleep(1)

    elif _gzip in tipo:
        flag += ".gz"
        subprocess.call(["mv", "-v", "last_flag", flag])
        subprocess.call(["gzip", "-dv", flag])
        #gunzip does not preserve file, not looked after options
        #subprocess.call(["rm", flag])
        if DEBUG:
            print("GZIP")
            time.sleep(1)

    elif _xz in tipo:
        flag += ".xz"
        subprocess.call(["mv", "-v", "last_flag", flag])
        subprocess.call(["tar", "-xvf", flag])
        subprocess.call(["rm", flag])
        if DEBUG:
            print("XZ")
            time.sleep(1)

    else:
        print("unknown format... exiting")
        print("Take a look")
        print(f"{tipo}")
        time.sleep(1)
        if "ASCII" in tipo:
            print("It looks like the flag :)")
            subprocess.call(["cat", "last_flag"])
        print(f"nº it -> {it}")
        sys.exit()



_content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")

it = 0
while True:
    position_new_flag(_content)
    _type = tipo( "last_flag" )
    #print(f"Tipo obtido: {_type}")
    redefine_type_and_extract(_type)
    #time.sleep(3)
    _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
    it += 1

