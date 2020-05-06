from utils import *
from utils import _compressed, _wl

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


def parse_password(raw_password):
    try:
        ''' file.zip:passwd:fileinside\nblabla '''
        password = raw_password.split("\n")[0].split(':')[1]
    except IndexError:
        print(f'[~~~]ERROR -> password = {raw_password}')

    return password


def extract_password_zip():
    shell_cmd_raw("zip2john last_flag.zip > hash 2>/dev/null")
    if _wl is not None:
        shell_cmd("john hash --wordlist=" + _wl)
    else:
        shell_cmd("john hash")

    raw_password = shell_cmd_output("john hash --show")

    return parse_password(raw_password)


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
