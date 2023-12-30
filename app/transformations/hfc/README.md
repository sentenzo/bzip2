> Source:
> - https://en.wikipedia.org/wiki/Huffman_coding

<h1>Huffman coding</h1> 

- [Abstract](#abstract)
- [Algorithm description](#algorithm-description)
  - [Encoding](#encoding)
    - [Side notes](#side-notes)
  - [Decoding](#decoding)
    - [Side notes](#side-notes-1)
- [Huffman tree](#huffman-tree)
    - [Side notes](#side-notes-2)
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

#### Side notes
- `encoded_data` is not byte-aligned (the length is not divisible by `8`)
    - usually we want our data to be byte-aligned for the sake of convenience
- to make bit-wise operations efficiently, we need a special data structure
    - Python <=3.11 has no such data structures out-of-the-box

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
    - nodes with symbols have no branches (= all the nodes with symbols are leaves)
- we only can decode the data, if we have its Huffman tree
    - we'll have to store Huffman tree with the encoded data

## Huffman tree

Given `init_data` (the data to be encoded), how to build a Huffman tree?

Here I'll try to give a recipe in an imperative style, without bothering to explain the meaning of the actions we take (mostly due to lack of knowledge).

First, we should count the frequencies of the symbols and sort it in ascending order:
```python
init_data = "voodoobanana"
freqs = Counter(init_data)
#{
# "b": 1,
# "v": 1, 
# "d": 1,
# "o": 4,
# "a": 3,
# "n": 2,
#}
```

Now we start processing them:
```python
freqs = ["b": 1,"v": 1,"d": 1,"n": 2,"a": 3,"o": 4]

# 1st iteration
# we pick the first two and join them:
first = freqs.pop(0) # ("b": 1)
second = freqs.pop(0) # ("v": 1)

(1+1==2)"bv"┬─0─(1)"b"
            └─1─(1)"v"
joined = ("bv": 2)
# we put it back to the freqs list, preserving the order:
freqs = ["d": 1,"n": 2,"bv": 2,"a": 3,"o": 4]

# 2nd iteration
# we pick the first two and join them:
first = freqs.pop(0) # ("d": 1)
second = freqs.pop(0) # ("n": 2)

(3)"dn"┬─0─(1)"d"
       └─1─(2)"n"
joined = ("dn": 3)
# again, we put it back to the freqs list, preserving the order:
freqs = ["bv": 2,"dn": 3,"a": 3,"o": 4]

# 3rd iteration
first = freqs.pop(0) # ("bv": 2)
second = freqs.pop(0) # ("dn": 3)

(5)"bvdn"┬─0─(2)"bv"┬─0─(1)"b"
         │          └─1─(1)"v"
         └─1─(3)"dn"┬─0─(1)"d"
                    └─1─(2)"n"
joined = ("bvdn": 5)
freqs = ["a": 3,"o": 4,"bvdn": 5]

# 4th iteration
first = freqs.pop(0) # ("a": 3)
second = freqs.pop(0) # ("o": 4)

(7)"ao"┬─0─(3)"a"
       └─1─(4)"o"
joined = ("ao": 7)
freqs = ["bvdn": 5,"ao": 7]

# 5th iteration
first = freqs.pop(0) # ("bvdn": 5)
second = freqs.pop(0) # ("ao": 7)

"bvndao"(12)┬─0─(5)"bvdn"┬─0─(2)"bv"┬─0─(1)"b"
            │            │          └─1─(1)"v"
            │            └─1─(3)"dn"┬─0─(1)"d"
            │                       └─1─(2)"n"
            └─1──────────────(7)"ao"┬─0─(3)"a"
                                    └─1─(4)"o"
joined = ("bvndao": 12)
freqs = ["bvndao": 12]

# the Huffman tree is built!
*┬─0─┬─0─┬─0─"b"
 │   │   └─1─"v"
 │   └─1─┬─0─"d"
 │       └─1─"n"
 └─1─────┬─0─"a"
         └─1─"o"
```

#### Side notes
- we used the same `init_data`, but we got a different Huffman tree, than it was in [[#Algorithm description|Algorithm description]] segment
- for the same data input many different Huffman trees can be built
    - for example, if you swap all `0`s and `1`s on the branches, it will still be a Huffman tree
- to pick the first two smallest nodes, we should use a heap data structure 

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