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
    - [See also:](#see-also)
    - [Side notes](#side-notes-3)
- [Implementation](#implementation)
  - [Bit-wise operations](#bit-wise-operations)
  - [Working with Huffman tree](#working-with-huffman-tree)
    - [Side notes](#side-notes-4)
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

**HFC** allows us to built a special data-structure called **Huffman tree**. There's a [detailed section on how to build it](#huffman-tree) below, but for now let's assume we know how to do it. 

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

Finally, to get the encoded data, we need to replace each symbol with its encoded bit sequence:
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
*┬─0─┬─0─┬─0─"b" # 000
 │   │   └─1─"v" # 001
 │   └─1─┬─0─"d" # 010
 │       └─1─"n" # 011
 └─1─────┬─0─"a" # 10
         └─1─"o" # 11

  v  o  o   d  o  o   b  a   n  a   n  a
001 11 11 010 11 11 000 10 011 10 011 10
```

#### Side notes
- we used the same `init_data`, but we got a different Huffman tree, than it was in [Algorithm description](#algorithm-description) segment
- for the same data input many different Huffman trees can be built
    - for example, if you swap all `0`s and `1`s on the branches, it will still be a Huffman tree
- to pick the first two smallest nodes, we should use a heap data structure 

## Canonical Huffman code
Having been able to build a Huffman tree, we still need to store it somehow. There's a variety of options here involving different kinds of tree-serialization. But in case of Huffman tree we can actually cheat a little. 

We don't need to serialize the entire tree. The whole tree structure is redundant. We only need to know the list of bit-sequance lengths for each symbol to restore a **canonical Huffman code** from it.

**Canonical Huffman code** is one of the possible Huffman code for the given data, which: 
- is unique
- always exists
- can be built out of any other Huffman code

Let's go back to the tree from [Huffman tree](#huffman-tree) section:
```python
init_data = "voodoobanana"

*┬─0─┬─0─┬─0─"b" # 000, length == 3
 │   │   └─1─"v" # 001, length == 3
 │   └─1─┬─0─"d" # 010, length == 3
 │       └─1─"n" # 011, length == 3
 └─1─────┬─0─"a" # 10,  length == 2
         └─1─"o" # 11,  length == 2
```

The only thing we need to build a canonical tree is the lengths of the encoding sequences:
```python
lengths.sort() # the sorting is mandatory!
lengths = [(2,"a"),(2,"o"),(3,"b"),(3,"d"),(3,"n"),(3, "v")]
```
Here's another recipe without explanation:
```python
# The 1st symbols is always all-zeroes
(2,"a"): "00" # "0"*2
# The next symbol is always +1 (in bynary form)
(2,"o"): "01" # 00 + 1 == 01
# The next symbol is always +1 (in bynary form)
# If the length is increased, zeros appends to the right
(3,"b"): "100" # 01 + 1 == 10, "10" + "0" == "100"
# The next symbol is always +1 (in bynary form)
(3,"d"): "101"
# The next symbol is always +1 (in bynary form)
(3,"n"): "110"
# The next symbol is always +1 (in bynary form)
(3,"v"): "111"
```

```python
 a  o   b   d   n   v
10 11 000 010 011 001 # what we had
00 01 100 101 110 111 # what we got (the canonical code)
```

Based on the code, we can restore the Huffman tree (using DFS or BFS).

#### See also: 
- [wiki article](https://en.wikipedia.org/wiki/Huffman_coding#Compression)
- [online visualization](https://cmps-people.ok.ubc.ca/ylucet/DS/Huffman.html)

#### Side notes
- the trees from [Algorithm description](#algorithm-description) and form [Huffman tree](#huffman-tree) differ in structure, despite being built on the same data
    - one tree has lengths `[2,2,3,3,3,3]`
    - the other one: `[2,2,2,3,4,4]`
    - despite that, the initial data encodes into `29` bits by **any of those trees**

## Implementation
### Bit-wise operations
You'll need some instruments for that (Python standard library doesn't have any). You need to:
- iterate through a binary data chunk by bits (used in decoding)
- construct new data chunks, appending arbitrary amounts of bits (used in encoding)
- align your data blocks if their bit-length is not divided by `8`

### Working with Huffman tree
It seems reasonable to have a separated class for these tasks. What should it do:
- build a **canonical Huffman tree** 
    - based on the frequencies of the initial data (used in encoding)
    - based on the code lengths (used in decoding)
- return the list of code **lengths** — the Huffman tree invariant
- build an **encoding table** from the Huffman tree (used in encoding)

#### Side notes
- in my implementation I used bytes as the initial symbols, but there's no restrictions in what these symbols can be
- a lot of optimizations can be applied to working with Huffman tree (see it [on wiki](https://en.wikipedia.org/wiki/Huffman_coding))

## Specification
`lengths` — is the list of code lengths in order to restore the tree. We assume the length is never bigger then `255`.

`lengths_rle_compressed == rle(lengths)`

`tail_length` — is a `1` byte segment to store the amount of aligning (non-significant) bits, which should be dropped from the end of the `encoded data` section.

```
 0               1               2               3
 0 1 2 3 4 5 6 7 8 9 A B C D E F 0 1 2 3 4 5 6 7 8 9 A B C D E F
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   lengths size (4 bytes)                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|              lengths_rle_compressed (up to 4 GiB)             |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                                                               |
|                                                               |
|                        encoded data                           |
|                                                               |
|                                               +-+-+-+-+-+-+-+-+
|                                               |  tail_length  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```