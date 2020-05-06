import subprocess
import sys
import time

_it = 0
_compressed = "last_flag"
_wl = None

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"
_ascii = "ASCII"


def has_wordlist():
    global _wl

    if "-w" in sys.argv:
        _wl = parse_wordlist_name()


def parse_wordlist_name():
    argc = len(sys.argv)

    w_index = sys.argv.index('-w')
    if w_index >= argc - 1:
        print("Did you provide a wordlist?")
        sys.exit(1)
    return sys.argv[w_index + 1]


def type(compressed):
    type_str = subprocess.Popen(["file", compressed],
                                stdout=subprocess.PIPE).stdout.read().decode()

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
    if _wl is not None:
        subprocess.call(["john", "hash", "--wordlist=" + _wl],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    else:
        subprocess.call(["john", "hash"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    passwd = subprocess.Popen(["john", "hash", "--show"],
                              stdout=subprocess.PIPE).stdout.read().decode()
    try:
        ''' file.zip:passwd:fileinside\nblabla '''
        passwd = passwd.split("\n")[0].split(':')[1]
    except IndexError:
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

    sys.exit()


def print_unknown_type():
    print("unknown format... exiting")
    print("Take a look:")
    redefine_type("unknown_file")
    type_str = subprocess.Popen(["file", "unknown_file"],
                                stdout=subprocess.PIPE).stdout.read().decode()
    print(f"{type_str[:-1]}")

    sys.exit()


def extract_zip():
    flag = "last_flag.zip"
    redefine_type(flag)

    passwd = None
    if check_for_password_zip() is not None:
        passwd = extract_password_zip()

    if passwd is None:
        subprocess.call(["unzip", "-o", "-qq", flag])
        subprocess.call(["rm", flag])
    else:
        subprocess.call(["unzip", "-o", "-P", passwd, "-qq", flag])
        subprocess.call(["rm", flag, "hash"])


def extract_tar():
    flag = "last_flag.tar"
    redefine_type(flag)

    subprocess.call(["tar", "-xf", flag])
    subprocess.call(["rm", flag])


def extract_bz2():
    flag = "last_flag.bz2"
    redefine_type(flag)

    subprocess.call(["bzip2", "-dk", flag])
    subprocess.call(["rm", flag])


def extract_gunzip():
    flag = "last_flag.gz"
    redefine_type(flag)

    subprocess.call(["gzip", "-d", flag])
    # gunzip does not preserve file, not looked after options
    # subprocess.call(["rm", flag])


def extract_xz():
    flag = "last_flag.xz"
    redefine_type(flag)

    subprocess.call(["tar", "-xf", flag])
    subprocess.call(["rm", flag])


def redefine_type_and_extract(type_):
    if type_ == 0:
        extract_tar()

    elif type_ == 1:
        extract_bz2()

    elif type_ == 2:
        extract_zip()

    elif type_ == 3:
        extract_gunzip()

    elif type_ == 4:
        extract_xz()

    elif type_ == 5:
        print_ascii()

    elif type_ == 6:
        print_unknown_type()


def main():
    global _it
    has_wordlist()
    try:
        position_first_flag(sys.argv[1])
    except IndexError:
        print("usage: python decompress.py [file] [-w wordlist]")
        sys.exit()

    _content = subprocess.Popen(["ls"], stdout=subprocess.PIPE)\
        .stdout.read().decode().split("\n")
    content = _content

    while True:
        if content != _content:
            position_new_flag(content, _content)

        compressed_type = type(_compressed)

        redefine_type_and_extract(compressed_type)
        content = subprocess.Popen(["ls"], stdout=subprocess.PIPE)\
            .stdout.read().decode().split("\n")
        _it += 1


if __name__ == '__main__':
    main()
