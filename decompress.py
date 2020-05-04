import subprocess
import sys
import os
import time

it = 0

_compressed = "last_flag"

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"


def tipo(compressed):
    type_str = subprocess.Popen(["file", compressed], stdout=subprocess.PIPE).stdout.read().decode()

    if _posix_tar in type_str:
        return 0
    elif _bzip2 in type_str:
        return 1
    elif _zip in type_str:
        return 2
    elif _gzip in type_str:
        return 3
    elif _xz in type_str:
        return 4
    else:
        return 5

def position_first_flag(name):
    subprocess.call(['mv', name, _compressed])

def position_new_flag(content, _content):
    found = 0

    for _file in content:
        if  _file not in _content:
            found = 1
            if _file != "last_flag":
                subprocess.call(["mv", _file, "last_flag"])
            break

    if not found:
        print("ERROR: DID NOT FIND THE FLAG FILE\nPlease rename the compressed data to one of the following names:\nflag.txt\nlast_flag\nflag\nflag.out")

def check_for_password( some_compressed_data ):


def redefine_type_and_extract( type_ ):
    flag = _compressed
    global it

    if type_ == 0:
        flag += ".tar"

        subprocess.call(["mv",  "last_flag", flag])
        subprocess.call(["tar", "-xf", flag])
        subprocess.call(["rm", flag])

    elif type_ == 1:
        flag += ".bz2"

        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["bzip2", "-dk", flag])
        subprocess.call(["rm", flag])

    elif type_ == 2:
        flag += ".zip"

        subprocess.call(["mv", "last_flag", flag])
        subprocess.Popen("zip2john last_flag.zip > hash 2>/dev/null", shell=True)
        subprocess.call(["john","hash"])
        # os.system("john hash --wordlist=pwd.txt 2>&1 1>/dev/null")
        passwd = subprocess.Popen(["john", "hash", "--show"], stdout=subprocess.PIPE).stdout.read().decode()
        try:
            passwd = passwd.split("\n")[0].split(':')[1]
        except:
            print('[~~~]ERROR',passwd,sep='')
        subprocess.call(["unzip", "-o", "-P", passwd , "-qq", flag])
        subprocess.call(["rm", flag, "hash"])

    elif type_ == 3:
        flag += ".gz"

        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["gzip", "-d", flag])
        #gunzip does not preserve file, not looked after options
        #subprocess.call(["rm", flag])

    elif type_ == 4:
        flag += ".xz"

        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["tar", "-xf", flag])
        subprocess.call(["rm", flag])

    elif type_ == 5:
        print("unknown format... exiting")
        print("Take a look")
        print(f"{type_}")
        if "ASCII" in type_:
            print("It looks like the flag :)")
            time.sleep(3)
            print("<=========================>")
            subprocess.call(["cat", "last_flag"])
            if "no line terminator" in type_:
                print()
            print("<=========================>")
        else:
            print("No ASCII text :(")
        print(f"nº iterations needed: {it}")
        sys.exit()



def main():
    global it

    _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
    position_first_flag(sys.argv[1])
    content = _content

    while True:
        position_new_flag(content, _content)
        compressed_type = tipo( _compressed )

        redefine_type_and_extract(compressed_type)
        content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
        it += 1

if __name__ == '__main__':
    main()
