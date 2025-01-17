# Characters

Currently, the best definition of a character is a Unicode char. A string `str` in python 3 is composed of unicode chars, while a object of type `bytes` is composed of bytes (8-bit char).

A unicode char is represented by a code point, that is a number between 0 and 1114111 (base 10), given in hexadecimal format with 4 to 6 digits, prefixed by `U+`, from `U+0000` to `U+10FFFF`

While the bytes that represent a unicode char is dependent on the encoding. The encoding is an algorithm that converts code points in bytes and vice versa. The char `A` have the code point `U+0041` that is encoded as `\x41` in the `UTF-8` encoding, for example.

```python
s = 'café'
len(s) # 4, which means 4 unicode chars
b = s.encode('utf-8')
print(b) # b'caf\xc3\xa9'
len(b) # 5, which means 5 bytes, because 'é' uses 2 bytes
```

# Concerning bytes

There are two embed byte sequence (aka byte string) in python:
  - `bytes` that is immutable. It was introduced in python 3
  - `bytearray` that is mutable. It was introduced in python 2.6

Every item in a `bytes` or `bytearray` is a integer between 0 and 255

```python
cafe = bytes('café', encoding='utf_8')
cafe_arr = bytearray(cafe)
cafe_arr[-1:] # bytearray(b'\xa9)
```

The representation to the user follow these rules:
  - If the byte is between 32 and 126, it is represented by the ASCII symbol
  - If the byte is a tab, a carriage return, a linebreak or a `\`, then they are represented by `\t`, `\r`, `\n` and `\\` respectivally.
  - String delimeters are use `\'` when applicable
  - Any other value use the hexadecimal notation. For example, `\00` is a null byte

Both types accept most of the methods available for strings `str` and for the `re` method for regular expressions.

## Creation

You can use one of the following to create a `bytes` or a `bytearray`:
  - a `str` and a `encoding`;
  - a iterable with items with values between 0 and 255;
  - A object that implements the buffer protocol. For example: an `array.array`
  - Using the `.fromhex('31 4B CE A9')` syntax.

# Encoders and decoders

Python have more than 100 codecs available.

Every codec have a name, but it can be also called by a nickname. For example, the codec `utf_8`, can be also called as `utf8`, `utf-8` and `U8`.


# Encoding and decoding problems

## `UnicodeEncodeError`

This could happen when converting a `str` to a `bytes` object, because the codec provided does not have the symbol available.

```python
city = 'São Paulo'
city.encode('cp437') # UnicodeEncodeError
city.encode('cp437', errors='ignore') # 'So Paulo'
city.encode('cp437', errors='replace') # 'S?o Paulo'
city.encode('cp437', errors='xmlcharreference') # 'S&#227;o Paulo'
```

As seen above, you can use the kwarg `errors` of `.encode()` for dealing with this exception, but this could led to loss of information. You can also implement a function to deal with this using the `codecs.register_error` function.

Since ASCII characters are common in most of the codecs, you can use the function `str.isascii()` to verify if you string is 100% ASCII. If it is, you can encode the string in most (if not all of them) without worring about a `UnicodeEncodeError`.

## `UnicodeDecodeError`

It happens when trying to convert a `bytes` into a `str`. Most of the time, this happens when you are using the wrong codec. 

What is even worse is that sometimes this exception is not trown and wrong characters are placed into your `str`

```python
octets = b'Montr\xe9al' # encoded using latin1
octets.decode('latin1') # Correct answer: 'Montréal'
octets.decode('cp1252') # Correct answer: 'Montréal', becuase cp1252 (used mostly in windows) is a supersect of latin1
octets.decode('koi8_r') # Wrong character: 'MontrИal'
octets.decode('utf-8') # UnicodeDecodeError
octets.decode('utf-8', errors='replace') # 'Montr�al'
```

A unnespected character is known as a gremlin or a 文字化け (mojibake)

## `SystaxError` when loading modules with unnexpected codec

This happens because Python 3 modules are expected to be saved in `utf-8` codec and sometimes windows can save a file using the `cp1252` codec. To solve this emplace a `# coding: cp1252` on the top of the file or convert it to `utf-8`

## Trying to guess the codec

TLDR: it is impossible, but you can use the [chardet](https://pypi.org/project/chardet/) to try find out.


## BOM: a useful gremlin

The `b'\xff \xfe` are known as the BOM (byte-order mark) and they are used by the codec `utf-16`, `utf-32` and `utf-8-sig` (used on windows by notepad and excel). See the book for further explanation.

# Processing text files

It's useful to deal with `bytes` only when reading/writing the contents of a file, and do all the processing of the information using the `str`. This is helped by using the `open()` function.

```python
fp = open('cafe.txt', 'w', encoding='utf_8')
fp.write('café') # writes the file and output 4, even tough 5 bytes were written, because this method returns the number of unicode chars written
fp.close()
import os
os.stat('cafe.txt').st_size # 5

fp2 = open('cafe.txt') # without the encoding argument, it can produce missbehave because on windows the default enconding is `cp1252`
fp2.read() # 'cafÃ©'

fp4 = open('cafe.txt', 'rb')
fp4.read() # returns a bytes object, so the output would be b'caf\xc3\xa9'
```

The default enconding is given by `locale.getpreferredencoding()` method of the `locale` builtin package. For a iterative python section, the stdin/stdout/stderr on windows is utf-8 but for a file, they are `cp1252.`. On unix based systems, it's everything utf8.

Therefore, the best advice is to avoid trusting the default encondings and always use the `enconding=` kwarg on the `open()` function.

# Unicode normalization

Because unicode chars can be composed of more than one byte, and some symbols can be expressed in more than just one way, the comparission of strings can be trick.  The solution is to use `unicodedata.normalize()`

```python
s1 = 'café'
s2 = 'cafe\N{COMBINING ACUTE ACCENT}'
print(s1, s2) # café café
len(s1), len(s2) # 4, 5
s1 == s2 # False

from unicodedata import normalize
len(normalize('NFC', s1)), len(normalize('NFC', s2)) # 4, 4
len(normalize('NFD', s1)), len(normalize('NFD', s2)) # 5, 5
```
- NFC: combines unicode points to produce the shortest string
- NFD: expand composed chars in base chars and separete them
- NFKC: same as NFC but with compatibility substitution (beware for info lost)
- NFKD: same as NFD but with compatibility substitution (beware for info lost)

```python
from unicodedata import normalize
ohm = '\u2126'
name(ohm) # 'OHM SIGN'
ohm_c = normalize('NFC', ohm)
name(ohm_c) # 'GREEK CAPITAL LETTER OMEGA'
ohm == ohm_c # False
normalize('NFC', ohm) == normalize('NFC', ohm_c) # True

half = '\N{VULGAR FRACTION ONE HALF}'
print(half) # ½
normalize('NFKC', half) # '1/2'
four_squared = '4²'
normalize('NFKC', four_squared) # '42', note how it lost its meaning
```

## Case folding

Essentially `str.casefold()` do the same as `str.lower()` but convert some of the chars to different unicode points

Use `normalize('NFC', something)` for most of applications and `str.casefold()` when does not matter if the char is capital.

## Removing all diacritcs marks

Sometimes when dealing with input from the user, it is better to remove all the accents (diacritics marks)


```python
import string
import unicodedata

def shave_marks(txt):
  norm_txt = unicodedata.normalize('NFD', txt):
  shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
  return unicodedata.normalize('NFC', shaved)

Greek = 'Ζέφυρος, Zéfiro'
shave_marks(Greek) # 'Ζεφυρος, Zefiro'
order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
shave_marks(order) # '“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
```

Notice that "έ" quando "é" were substituted in the Greek example. To remove accents only from latin letters, use the following:

```python
def shave_marks_latin(txt):
  norm_txt = unicodedata.normalize('NFD', txt)
  latin_base = False
  preserve = []
  for c in norm_txt:
    if unicodedata.combining(c) and latin_base:
      continue
    preserve.append(c)
    if not unicode.combining(c):
      latin_base = c in string.ascii_letters
  shaved = ''.join(preserve)
  return unicodedata.normalize('NFC', shaved)
```

# Unicode ordering

Unicode basic ordering compares code points. However, this could cause undesired behaviour

```python
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted(fruits) # ['acerola', 'atemoia', 'açaí', 'caju', 'cajá']
```

The correct way should be `['açaí', 'acerola', 'atemoia', 'cajá', 'caju']`. To enforce this, we should use the `locale.strxfm` method:

```python
import locale
my_locale = locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=locale.strxfrm)
```

There is the `pyuca` lib that do this without considering the `locale` and using the Unicode Collation Algorithm.

# Unicode database

The module `unicodedata` is the unicode database, you use it to search for unicode chars.  See the `find_char.py` to see a application. 

# Double API for `str` and `bytes`

Some functions in python accept both `str` and `bytes`, but have a different behaviour depending on which one of them.

## Regular expressions

If you use `bytes`, re such as `\d` and `\w` will match only for ASCII characters, but if you use `str` it will match with Unicode and ASCII chars. See the example on the book to understand it.

## `os` module

The GNU/Linux kernel does not know about Unicode, so you can find some filenames that will not suit any codec and should be treated as normal as regular filenames. Because of this, the `os` module also accepts the `bytes` objects anywhere a filename is expected.

Two usefull  functions to deal with this are:
  - `os.fsencode()`
  - `os.fsdecode()`