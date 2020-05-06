import subprocess
import time
import sys

_compressed = "last_flag"
_wl = None
_it = 0

_posix_tar = "POSIX tar archive (GNU)"
_bzip2 = "bzip2 compressed data"
_zip = "Zip archive data"
_gzip = "gzip compressed data"
_xz = "XZ compressed data"
_ascii = "ASCII"


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


def position_first_flag(name):
    shell_cmd("mv " + name + " " + _compressed)


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


def has_wordlist():
    global _wl

    if "-w" in sys.argv:
        _wl = parse_wordlist_name()


def parse_wordlist_name():
    argc = len(sys.argv)

    w_index = sys.argv.index('-w')
    if w_index >= argc - 1:
        print("Did you provide a wordlist?")
        exit()
    return sys.argv[w_index + 1]


def compressed_file():
    return sys.argv[1]


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

    exit()


def print_unknown_type():
    print("unknown format... exiting")
    print("Take a look:")
    redefine_type("unknown_file")
    type_str = shell_cmd_output("file unknown_file")
    print(f"{type_str[:-1]}")

    exit()


def exit():
    sys.exit()
