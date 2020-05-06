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


def shell_cmd(command):
    subprocess.call(command.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)


def shell_cmd_process(command):
    return subprocess.Popen(command.split(),
                            stdout=subprocess.PIPE)


def shell_cmd_output(command):
    return subprocess.Popen(command.split(),
                            stdout=subprocess.PIPE).stdout.read().decode()


def shell_cmd_output_lines(command):
    return subprocess.Popen(command.split(),
                            stdout=subprocess.PIPE).stdout\
        .read().decode().split('\n')


def shell_cmd_raw(command):
    subprocess.Popen(command, shell=True)


def type(compressed):
    type_str = shell_cmd_output("file " + compressed)

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
    p = shell_cmd_process("./has_pass_zip " + _compressed + ".zip")

    if p.stdout is not None:
        return True
    return False


def check_for_password_rar():
    p = shell_cmd_process("./has_pass_zip " + _compressed + ".rar")

    if p.stdout is not None:
        return True
    return False

# future 7z implementation


def position_first_flag(name):
    shell_cmd("mv " + name + " " + _compressed)


def parse_password(raw_password):
    try:
        ''' file.zip:passwd:fileinside\nblabla '''
        password = raw_password.split("\n")[0].split(':')[1]
    except IndexError:
        print(f'[~~~]ERROR -> password = {raw_password}')

    return password


def position_new_flag(content, _content):
    # _content is the dir at the start of the script
    # content is the modified dir
    found = 0

    for _file in content:
        if _file not in _content:
            found = 1
            if _file != "last_flag":
                shell_cmd("mv " + _file + " last_flag")
            break

    if not found:
        print("ERROR: DID NOT FIND THE FLAG FILE\n")


def extract_password_zip():
    shell_cmd_raw("zip2john last_flag.zip > hash 2>/dev/null")
    if _wl is not None:
        shell_cmd("john hash --wordlist=" + _wl)
    else:
        shell_cmd("john hash")

    raw_password = shell_cmd_output("john hash --show")

    return parse_password(raw_password)


def redefine_type(new_type):
    shell_cmd("mv last_flag " + new_type)


def read_flag():
    return shell_cmd_output("cat last_flag")

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
    type_str = shell_cmd_output("file unknown_file")
    print(f"{type_str[:-1]}")

    sys.exit()


def extract_zip():
    flag = "last_flag.zip"
    redefine_type(flag)

    passwd = None
    if check_for_password_zip() is not None:
        passwd = extract_password_zip()

    if passwd is None:
        shell_cmd("unzip -o -qq " + flag)
        shell_cmd("rm " + flag)
    else:
        shell_cmd("unzip -o -P " + passwd + " -qq " + flag)
        shell_cmd("rm " + flag + " hash")


def extract_tar():
    flag = "last_flag.tar"
    redefine_type(flag)

    shell_cmd("tar -xf " + flag)
    shell_cmd("rm " + flag)


def extract_bz2():
    flag = "last_flag.bz2"
    redefine_type(flag)

    shell_cmd("bzip2 -dk " + flag)
    shell_cmd("rm " + flag)


def extract_gunzip():
    flag = "last_flag.gz"
    redefine_type(flag)

    shell_cmd("gzip -d " + flag)
    # gunzip does not preserve file, not looked after options
    # subprocess.call(["rm", flag])


def extract_xz():
    flag = "last_flag.xz"
    redefine_type(flag)

    shell_cmd("tar -xf " + flag)
    shell_cmd("rm " + flag)


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

    _content = shell_cmd_output_lines("ls")
    content = _content

    while True:
        if content != _content:
            position_new_flag(content, _content)

        compressed_type = type(_compressed)

        redefine_type_and_extract(compressed_type)
        content = shell_cmd_output_lines("ls")
        _it += 1


if __name__ == '__main__':
    main()
