> Source:
> - https://en.wikipedia.org/wiki/Run-length_encoding
> - https://michaeldipperstein.github.io/rle.html

<h1>Run-length encoding</h1> 

- [Abstract](#abstract)
- [Naive implementation](#naive-implementation)
- [Encoded/Not-Encoded Flag](#encodednot-encoded-flag)
  - [Byte extension](#byte-extension)
    - [Side notes](#side-notes)
  - [Byte shrinking](#byte-shrinking)
    - [Side notes](#side-notes-1)
  - [A byte of flags](#a-byte-of-flags)
    - [Side notes:](#side-notes-2)
- [Escape code](#escape-code)
  - [A fixed escape byte](#a-fixed-escape-byte)
  - [A parametrizable escape byte](#a-parametrizable-escape-byte)
- [Double bytes](#double-bytes)
    - [Side notes:](#side-notes-3)
- [The PackBits algorithm](#the-packbits-algorithm)
    - [Side notes:](#side-notes-4)
  - [Specification](#specification)

There will be a very detailed article here about the different approaches to RLE.

[Click HERE to get straight to the **practical part**](#the-packbits-algorithm).

## Abstract

A popular and (relatively) easy to implement lossless data compression algorithm.

## Naive implementation
To simplify the task, let's assume the input data is always a string (a text): 
```python
# encoding
"ABBBCC" => "AB3C2"
# decoding
"AB3C2" => "A" + "B"*3 + "C"*2 => "ABBBCC"
```
In this case the RLE implementation becomes trivial. Here's one from LeetCode: [443. String Compression](https://leetcode.com/problems/string-compression/editorial/)

However, any practical implementation should work with arbitrary byte sequences. So the expression above will look like this:

```python
# encoding
[0x65, 0x66, 0x66, 0x66, 0x67, 0x67] => [0x65, 0x66, 0x51, 0x67, 0x50]
# A     B     B     B     C     C         A     B     3     C     2

# decoding
[0x65, 0x66, 0x51, 0x67, 0x50] => ... # ?
# A     B     3     C     2
```

The result of the decoding in this case is actually undetermined. The ambiguity comes from our inability to tell if the number is a **symbol** or a **counter** for some symbol, which goes before it.

Imagine you get a string `"h32"` it can be decoded into:
- `"h32"`
- `"hhh2"` (`"h"*3 + "2"`)
- `"h33"` (`"h" + "3"*2`)
- `"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"` (`"h"*32`)

So, we've got an ambiguity, which makes it impossible to decode the data. How can we fix this issue?

## Encoded/Not-Encoded Flag

To distinguish **symbols** from **counters**, we can flag them with a special additional bit. And we can do it in more than one way.

The **counters** are usually limited with **1 byte length**, which caps our compression efficiency with `x256`, but makes it easier to implement and more efficient in practical cases.

### Byte extension
We can add one additional bit to each byte, like this:
```c
# bytes without extension:
  01100101 01100110 00000011 01100111 00000010
# \------| \------| \------| \------| \-----|
#        A        B        3        C       2
# bytes with extension:
# v         v         v         v         v
  00110010 10011001 10100000 01100110 01111000 00010xxx
#  \-------| \-------| \-------| \-------| \-------|
#          A         B         3         C         2
```

#### Side notes
- it creates a **loose (unaligned) byte at the end**, and aligning it can be a tricky task
- it **violates the initial byte alignment** (supposedly, it leads to a less efficient calculation on CPU)

### Byte shrinking
We can regroup the original bits into segments 7 bits each + 1 bit reserved for a flag. Then you can encode this sequence.

```c
# original bytes:
11010110 01101000 11010100 10110011
#      Ö        h        Ô        ³

# bytes regrouped:
_1101011 _0011010 _0011010 _1001011 _0011xxx

# bytes encoded:
01101011 00011010 10000010 01001011 00011xxx
#                 ^-------
#                        2
```

```c
01100101 01100110 00000011 01100111 00000010
00101xxx 01100101 01100110 00000011 01100111 00000010
```

#### Side notes
- it creates a **loose (unaligned) byte at the end**, and aligning it can be a tricky task
- it changes the data pattern in bytes (`"ÖhÔ³"` — has a better compression potential, than `"aaaaaaa"`)

### A byte of flags
In each group of 8 bytes we add an additional byte to store the flags.

```c
01100101 01100110 00000011 01100111 00000010
# 00101 => 0        0        1        0        1
  00101xxx 01100101 01100110 00000011 01100111 00000010
# \------| \------| \------| \------| \------| \-----|
#    flags        A        B        3        C       2
```

#### Side notes:
- there can be a loose flags-byte in the end of the sequence, but the significant bits are determined by the size of the encoded block

## Escape code
To mark the **counter** bytes we can use a special symbol (or a sequence).

### A fixed escape byte
We may pick some arbitrary byte for this role. Like `0b01011100 == "\"` and make it an escape byte for our algorithm.

```python
"abbbcc" => r"ab\3\c\2\"
# counter:       -   -
#  symbol:    --   -   
```

The tricky part is how to deal with the escape symbol itself (if it is present in the initial data block). The easiest to implement approach is to double it.

```python
# 
r"\\3\c\\\" => r"\\\2\3\\c\\\3\"
#    counter:       -        -
#     symbol:     --   -------   
# single "\":     --    --  --
```

### A parametrizable escape byte
The same as a fixed escape byte, but we pick the rarest byte in the data block for and claim it as an escape byte for the current block.

## Double bytes

Any repetitive sequence of bytes is replaced with two bytes and is followed by a byte, which should be converted to `unsigned int` and interpreted as the length of the sequence.

```python
"abbbbbbccdddd" => "abb6cc2dd4"
```

#### Side notes:
- performes badly on size 2 repetitions: `"abbcddeefgg" => "abb2cdd2ee2fgg2"`

## The PackBits algorithm

You split your initial data into packages:
```python
"inqktqigfffffhmkvosynozpgggggggggpcrelizif"
["inqktqig", ("f", 5), "hmkvvosynozp", ("g", 9), "pcrelizzif"]
[8, "inqktqig", -5, "f", 12, "hmkvvosynozp", -9, "g", 10, "pcrelizzif"]
```
The stream of bytes always starts with a **counter byte** `n`. Its value can be between `-128` and `127`. It describes the package of the size, determined by the `n` value.
- if  `1 <= n <= 127` — the next `n` symbols are not modified
- if `-128 <= n <= -1` — the following byte should be repeated `-n` times

This one will actually be the algorithm of my choice to implement.

#### Side notes:
- we won't encode size 2 repetitions — it gives us no benifit in compression

### Specification

- the encoded binary block consists of the **initial sequence bytes**, separated with 
singular **counter bytes**
- the block always starts whith a counter byte
- if the value of a **counter byte** is positive and equals to `c`:
  - the next `c` bytes are the **initial sequence bytes** with no repetitions
  - the next **counter byte** is the next one after the sequence (`cur_pos += c + 1`)
- if the value of a **counter byte** is negative and equal to `-c`:
  - the next byte after is to be repeated `c` times
  - the next **counter byte** is located two steps ahead (`cur_pos += 2`)


```
 0               1               2               3
 0 1 2 3 4 5 6 7 8 9 A B C D E F 0 1 2 3 4 5 6 7 8 9 A B C D E F
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    +counter   |                                               |
+-+-+-+-+-+-+-+-+                                               |
|                       A sequence of bytes with no             |
|                      repetitions (up to 127 bytes)            |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   -counter    |    1 byte     |   -counter    |    1 byte     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   -counter    |    1 byte     |   +counter    |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+               |
|                                                               |
|   A sequence of bytes with no repetitions (up to 127 bytes)   |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                             ...                               |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```