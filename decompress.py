import utils
from utils import *
from utils import _compressed
from extractor import *



def main():
    has_wordlist()
    try:
        position_first_flag(compressed_file())
    except IndexError:
        print("usage: python decompress.py [file] [-w wordlist]")
        exit()

    _content = shell_cmd_output_lines("ls")
    content = _content

    while True:
        if content != _content:
            position_new_flag(content, _content)

        compressed_type = type(_compressed)

        redefine_type_and_extract(compressed_type)
        content = shell_cmd_output_lines("ls")
        utils._it += 1


if __name__ == '__main__':
    main()
