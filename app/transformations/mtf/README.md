> Source:
> - https://en.wikipedia.org/wiki/Move-to-front_transform

<h1>Move-to-front transform</h1> 

- [Abstract](#abstract)
- [Implementation](#implementation)
  - [Encoding](#encoding)
  - [Decoding](#decoding)
- [Specification](#specification)


## Abstract
Move-to-front transform (**MTF**) is a data encoding method with no compression, but the resulting data appears to have more potential for compression.

It is used as an extra step in some compression algorithms.

## Implementation
The following examples will be related to strings. But the same line of reasoning stands for binary data.

### Encoding

It's easier to explain in practice.

Let's pick some string to tinker with. Let it be `"coconut"`.

Now let's pick the dictionary — one of the embedded parameters of **MTF** algorithm. Let it be the alphabet: `"abcde...xyz"`.

And here the encoding begins:

```python
      0 1 2 3 ... 23 24 25
> c | a b c d ...  x  y  z | => 2
  o |                      |
  c |                      |
  o |                      |
  n |                      |
  u |                      |
  t |                      |
```

On the first iteration we are encoding the letter `c`.  The result is `2`, because this is the position of `c` in the dictionary.

Then we modify the dictionary: we **move** `c` **to front**:

```python
      0 1 2 3 ... 23 24 25
  c | a b c d ...  x  y  z | => 2
> o | c a b d ...  x  y  z | => 14
  c |                      |
  o |                      |
  n |                      |
  u |                      |
  t |                      |
```

`o` is encoded as `14` — because `o` is the 15-th letter and its position wasn't shifted. Well, yet...

```python
      0 1 2 3 ... 23 24 25
  c | a b c d ...  x  y  z | => 2
  o | c a b d ...  x  y  z | => 14
> c | o c a b ...  x  y  z | => 1
  o |                      |
  n |                      |
  u |                      |
  t |                      |
```

Now `o` is moved to front, and we've finished the 3-d iteration. 

This is the final state:
```python
      0 1 2 3 ... 23 24 25
  c | a b c d ...  x  y  z | => 2
  o | c a b d ...  x  y  z | => 14
  c | o c a b ...  x  y  z | => 1
  o | c o a b ...  x  y  z | => 1
  n | o c a b ...  x  y  z | => 14
  u | n o c a ...  x  y  z | => 20
  t | u n o c ...  x  y  z | => 20
```

The encoded string is `[2,14,1,1,14,20,20]`.

### Decoding
We have:
- the initial dictionary state:
```
  0  1  2  3  4  5  6  7  8  9 10 11 12 
  a  b  c  d  e  f  g  h  i  j  k  l  m
 13 14 15 16 17 18 19 20 21 22 23 24 25
  n  o  p  q  r  s  t  u  v  w  x  y  z
```
- the encoded string: `[2,14,1,1,14,20,20]`

This is enough to recreate the hole encoding procedure.

1. **The 1st symbol** of the string is encoded with `2`. At the first iteration the dictionary had initial state. Hence, **the 1st symbol is `dict[2] == "c"`**.
    - we know exactly how the dictionary was modified: `"abcd...xyz" => "cabd...xyz"`
2. **The 1st symbol** of the string is encoded with `14`. So, it will be `dict[14] == "o"`
    - don't forget to modify
3. etc.


## Specification

The dictionary initial state is always considered to be `list(range(256))` — the list of all bytes from `0x00` to `0xff`.

There's no other parameters to transmit, except for the encoded data itself, so there's no specific binary markup for the block.