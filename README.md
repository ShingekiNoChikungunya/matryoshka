# What it is
Simple and very specific script to decompress data compressed several times.

The script supports only most commom tools and algorithms, like:

* bz2
* gz
* tar
* xz
* zip

## Usage
```
$ chmod 0755 has_pass_zip
$ python decompress.py zip_bomb.something
```
---

## How to add a new type

You can read the explanation for better understanding or just skip to the instructions.

### Brief Explanation
---
The script starts with the compressed name you passed to it.

On the first loop he will rename it to the generic name _last flag_, in the function, _position_first_flag_.

_last flag_ will continuely be used throughout the script. Second step, it will get the type of compressed file by the linux util _file_, in the function _type_. The function _type_ will use the static strings defined in _utils.py_.

After getting the file type, at _decompress.py_, the file generically named _last flag_ will be renamed to its appropiate extension, eg. _last flag.zip_ in the function _redefine_type_( _utils.py_), and then suitably extracted, this takes place in the _redefine_type_and_extract_ function at _extractor.py_.

Bonus: Some file types are password protected, so we check it and deal with it in each extraction function. Ideally the function _redefine_type_and_extract_ doesn't need to know it.

This finishes an iteraction. We now rename the newly generated file to the generic name _last flag_, in _position_new_flag_ at _decompress.py_. And go on again. 

### Instructions
---

1. Get a portion of the compressed file type description string with _file_ util.
2. Open _utils.py_ and paste it inside a variable.
3. In _utils.py_, inside the function _type_, add an elif statement before the ascii one.
4. You can return any number, just remember it as we will need it later.
5. Close _utils.py_ and open _extractor.py_ up.
6. Now create a function to extract your new type. There are some wrappers to shell commands defined in _utils.py_ that can be helpful and you can take one of the already defined functions as examples. Remembering that we first use the function _redefine_type_ to rename the previously generic name _last_flag_ to the appropriate name, with the extension.
7. Now at the main function, add an _elif_ statement before the unknown type in the function _redefine_type_and_extract_, compare if type_ equals your type code. And if so, call your extract function defined in step 6.
8. That's it.
