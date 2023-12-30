> Source:
> - https://en.wikipedia.org/wiki/Huffman_coding

<h1>Huffman coding</h1> 

- [Abstract](#abstract)
- [Algorithm description](#algorithm-description)
  - [Encoding](#encoding)
  - [Decoding](#decoding)
    - [Side notes](#side-notes)
- [Huffman tree](#huffman-tree)
- [Canonical Huffman code](#canonical-huffman-code)
- [Implementation](#implementation)
- [Specification](#specification)


## Abstract

Huffman coding (**HFC**) — a very popular lossless data compression algorithm. 

It's a type of a prefix code, which implies each element of initial dictionary can be encoded with arbitrary amount of bits. 

## Algorithm description

To understand Huffman coding, you should see it in action.

### Encoding

We have a string we want to encode:
```python
init_data = "voodoobanana" # len(init_data)
init_data_len = len(init_data) # 12
init_data_len_bits = init_data_len * 8 # 96
```

**HFC** allows us to built a special data-structure called **Huffman tree**. There's a [[#Huffman tree|detailed section on how to build it]] below, but for now let's assume we know how to do it. 

A Huffman tree for a string `"voodoobanana"` looks like this:
```python
      ┌─0────────────"o" # 00
 ┌─0──┴─1────────────"a" # 01
*┴─1──┬─0────────────"n" # 10
      └─1──┬─0───────"b" # 110
           └─1──┬─0──"d" # 1110
                └─1──"v" # 1111
```

It's a binary tree (each node has no more than two children). Each branch is marked with a digit either `0` or `1`. The leaf nodes store symbols from `init_data`. There's only six distinct symbols present: `"o"`, `"a"`, `"n"`, `"b"`, `"d"` and `"v"`.

The bit sequence after the `#` sign represents the encoding of each symbol. It derives from the path you should cross to get to the leaf. For example, to get to `"d"`, you need to go down (`1`), down (`1`), down (`1`), up (`0`), and this gives you `1110`.

Finally, to get the encoded data, we need to replace each symbol with its encoded bit sequance:
```python
encoder = {
  "o": [0,0],
  "a": [0,1],
  "n": [1,0],
  "b": [1,1,0],
  "d": [1,1,1,0],
  "v": [1,1,1,1],
}
encoded_data = []
for symbol in init_data: # "voodoobanana"
    encoded_data.extend(encoder[symbol])
# v    o  o  d    o  o  b   a  n  a  n  a
# 1111 00 00 1110 00 00 110 01 10 01 10 01

encoded_data_len_bits = len(encoded_data) # 29
```

`init_data_len_bits` was `96` bits long, and `encoded_data_len_bits` is `29` bits — **70% smaller**.

### Decoding

We are having:
- a Huffman tree:
  ```python
        ┌─0────────────"o"
   ┌─0──┴─1────────────"a"
  *┴─1──┬─0────────────"n"
        └─1──┬─0───────"b"
             └─1──┬─0──"d"
                  └─1──"v"
  ```
- an encoded sequence of bits: `11110000111000001100110011001`

This is how we work it out:
```python
decoded_data == []

# we put a pointer (*) to the root:

      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
*┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"
▼
11110000111000001100110011001 # the current bit is 1

# we choose branch 1 to move forward 
      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
─┴─1─*┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"
 ▼
11110000111000001100110011001 # the current bit is 1

# we choose branch 1 to move forward 
      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
─┴─1──┬─0────────────"n"
      └─1─*┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"
  ▼
11110000111000001100110011001 # the current bit is 1 (again)

# we choose branch 1 to move forward 
      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
─┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1─*┬─0──"d"
                └─1──"v"
   ▼
11110000111000001100110011001 # the current bit is 1

# we choose branch 1 to move forward 
      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
─┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1─*"v"
# we got to the leaf, which stores the symbol "v"
# we append the symbol to the decoded_data
decoded_data == ["v"]

# we put the pointer (*) to the root again:
      ┌─0────────────"o"
 ┌─0──┴─1────────────"a"
*┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"

    ▼
11110000111000001100110011001 # the current bit is 0

# we choose branch 0 to move forward 
      ┌─0────────────"o"
 ┌─0─*┴─1────────────"a"
─┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"

     ▼
11110000111000001100110011001 # the current bit is 0 (again)

# we choose branch 0 to move forward 
      ┌─0───────────*"o"
 ┌─0──┴─1────────────"a"
─┴─1──┬─0────────────"n"
      └─1──┬─0───────"b"
           └─1──┬─0──"d"
                └─1──"v"

# we append the symbol to the decoded_data
decoded_data == ["v", "o"]

...
```

And so it repeats till we restore the entire string.

#### Side notes
- Huffman code has a remarkable property called **prefix property**: none of its bit sequences is a prefix to the other sequence:
    - `a: 10, b: 111` — **can** be a part of some Huffman code
    - `a: 10, b: 101` — **can NOT** be a part of a Huffman code, because `101` starts with `10`
- **prefix property** is guarantied by Huffman tree properties:
    - going the same path always brings you to the same place (like in any graph)
    - nodes with symbols have no branches

## Huffman tree

```python
"voodoobanana"
{
 "o": 4,
 "a": 3,
 "n": 2,
 "b": 1,
 "v": 1, 
 "d": 1,
}

            ┌─0──────────────────(4)"o" # 00
    ┌─0──(7)┴─1──────────────────(3)"a" # 01
(12)┴─1──(5)┬─0──────────────────(2)"n" # 10
            └─1──(3)┬─0──────────(1)"b" # 110
                    └─1──(2)┬─0──(1)"v" # 1110
                            └─1──(1)"d" # 1111
```

## Canonical Huffman code



## Implementation


## Specification

```
 0               1               2               3
 0 1 2 3 4 5 6 7 8 9 A B C D E F 0 1 2 3 4 5 6 7 8 9 A B C D E F
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   lengths size (4 bytes)                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|            lengths - RLE-compressed (up to 4 GiB)             |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                                                               |
|                                                               |
|                        encoded data                           |
|                                                               |
|                                                               |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```