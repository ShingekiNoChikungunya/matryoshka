import subprocess
import sys
import os
import time

_it = 0
_compressed = "last_flag"

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"
_ascii = "ASCII"


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
    elif _ascii in type_str:
        return 5
    else:
        return 6


def check_for_password_zip():
    p = subprocess.Popen(["./has_pass_zip", _compressed + ".zip"],
                         stdout=subprocess.PIPE)

    if p.stdout is not None:
        return True
    return False


def check_for_password_rar():
    p = subprocess.Popen(["./has_pass_rar", _compressed + ".rar"],
                         stdout=subprocess.PIPE)

    if p.stdout is not None:
        return True
    return False

# future 7z implementation


def position_first_flag(name):
    subprocess.call(['mv', name, _compressed])


def position_new_flag(content, _content):
    # _content is the dir at the start of the script
    # content is the modified dir
    found = 0

    for _file in content:
        if _file not in _content:
            found = 1
            if _file != "last_flag":
                subprocess.call(["mv", _file, "last_flag"])
            break

    if not found:
        print("ERROR: DID NOT FIND THE FLAG FILE\n")


def extract_password_zip():
    subprocess.Popen("zip2john last_flag.zip > hash 2>/dev/null",
                     shell=True)
    subprocess.call(["john", "hash"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    # os.system("john hash --wordlist=pwd.txt 2>&1 1>/dev/null")
    passwd = subprocess.Popen(["john", "hash", "--show"],
                              stdout=subprocess.PIPE).stdout.read().decode()
    try:
        ''' file.zip:passwd:fileinside\nblabla '''
        passwd = passwd.split("\n")[0].split(':')[1]
    except:
        print(f'[~~~]ERROR -> password = {passwd}')

    return passwd


def redefine_type(new_type):
    subprocess.call(["mv", "last_flag", new_type])


def read_flag():
    return subprocess.Popen(["cat", "last_flag"],
                            stdout=subprocess.PIPE).stdout.read().decode()


def print_flag(flag):
    separator = '<' + '=' * (len(flag) - 2) + '>'
    print(separator)
    if "\n" in flag:
        print(flag, end="")
    else:
        print(flag)
    print(separator)


def print_ascii():
    print("It looks like the flag :)")
    flag = read_flag()
    time.sleep(3)
    print_flag(flag)
    print(f"nº iterations needed: {_it}")


def print_unknown_type(type_):
    print("unknown format... exiting")
    print("Take a look")
    print(f"{type_}")
    print("No ASCII text :(")


def extract_zip(passwd):
    flag = "last_flag.zip"
    if passwd is None:
        subprocess.call(["unzip", "-o", "-qq", flag])
        subprocess.call(["rm", flag])
    else:
        subprocess.call(["unzip", "-o", "-P", passwd, "-qq", flag])
        subprocess.call(["rm", flag, "hash"])


def redefine_type_and_extract(type_):
    flag = _compressed

    if type_ == 0:
        flag += ".tar"
        redefine_type(flag)

        subprocess.call(["tar", "-xf", flag])
        subprocess.call(["rm", flag])

    elif type_ == 1:
        flag += ".bz2"
        redefine_type(flag)

        subprocess.call(["bzip2", "-dk", flag])
        subprocess.call(["rm", flag])

    elif type_ == 2:
        flag += ".zip"
        redefine_type(flag)

        passwd = None
        if check_for_password_zip() is not None:
            passwd = extract_password_zip()
        extract_zip(passwd)

    elif type_ == 3:
        flag += ".gz"
        redefine_type(flag)

        subprocess.call(["gzip", "-d", flag])
        # gunzip does not preserve file, not looked after options
        # subprocess.call(["rm", flag])

    elif type_ == 4:
        flag += ".xz"
        redefine_type(flag)

        subprocess.call(["tar", "-xf", flag])
        subprocess.call(["rm", flag])

    elif type_ == 5:
        print_ascii()
        sys.exit()

    elif type_ == 6:
        print_unknown_type(type_)
        sys.exit()


def main():
    global _it

    position_first_flag(sys.argv[1])
    _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE)\
        .stdout.read().decode().split("\n")
    content = _content

    while True:
        if content != _content:
            position_new_flag(content, _content)

        compressed_type = tipo(_compressed)

        redefine_type_and_extract(compressed_type)
        content = subprocess.Popen(["ls"], stdout=subprocess.PIPE)\
            .stdout.read().decode().split("\n")
        _it += 1


if __name__ == '__main__':
    main()
