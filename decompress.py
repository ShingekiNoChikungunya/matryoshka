import subprocess
import sys
import time

it = 0

compressed = "last_flag"

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"


def tipo(compressed):
    return subprocess.Popen(["file", compressed], stdout=subprocess.PIPE).stdout.read().decode()

def position_new_flag(content):
    found = 0

    for _file in content:
        if "flag" in _file:
            found = 1
            if _file != "last_flag":
                subprocess.call(["mv", _file, "last_flag"])
            break

    if not found:
        print("ERROR: DID NOT FIND THE FLAG FILE\nPlease rename the compressed data to one of the following names:\nflag.txt\nlast_flag\nflag\nflag.out")

def redefine_type_and_extract(tipo):
    flag = "last_flag"
    global it

    if _posix_tar in tipo:
        flag += ".tar"

        subprocess.call(["mv",  "last_flag", flag])
        subprocess.call(["tar", "-xf", flag])

        subprocess.call(["rm", flag])

    elif _bzip2 in tipo:
        flag += ".bz2"
        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["bzip2", "-dk", flag])
        subprocess.call(["rm", flag])

    elif _zip in tipo:
        flag += ".zip"
        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["unzip", "-qq", flag])
        subprocess.call(["rm", flag])

    elif _gzip in tipo:
        flag += ".gz"
        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["gzip", "-d", flag])
        #gunzip does not preserve file, not looked after options
        #subprocess.call(["rm", flag])

    elif _xz in tipo:
        flag += ".xz"
        subprocess.call(["mv", "last_flag", flag])
        subprocess.call(["tar", "-xf", flag])
        subprocess.call(["rm", flag])

    else:
        print("unknown format... exiting")
        print("Take a look")
        print(f"{tipo}")
        time.sleep(3)
        if "ASCII" in tipo:
            print("It looks like the flag :)")
            subprocess.call(["cat", "last_flag"])
        print(f"\nnº it -> {it}")
        sys.exit()



def main():
    _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
    global it

    while True:
        position_new_flag(_content)
        _type = tipo( "last_flag" )

        redefine_type_and_extract(_type)
        _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE).stdout.read().decode().split("\n")
        it += 1

if __name__ == '__main__':
    main()
