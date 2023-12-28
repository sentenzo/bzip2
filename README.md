# bzip2

This project is my implementation of **bzip2** 
([wiki](https://en.wikipedia.org/wiki/Bzip2)) — is a popular and efficient 
data compression algorithm.

![preview](./preview.png)

## Disclaimer
Though the code presented is fully functional, passes all the tests and has 
notable compression efficiency, the following should be taken into account:
- it's a pet project — it was **never meant to be used in production**
- the file binary structure is incompatible with the original bzip2 format 
(= can't be opened with an archive manager app)
- optimization leaves much to be desired due to a variety of factors:
  - it's written on pure Python
  - algorithm parameters are not fine-tuned enough

## Project overview

The project files can be roughly groupt into three cathegories:
1. The implementation itself
2. Infrostructure (`Makefile`, `main.py`, settings, tests)
3. Extended documentation (all the `README.md` files)

## Algorithm specification

bzip2 algorithm can be described as a chain of reversible transformations:

1. Splitting into blocks
2. **RLE**
3. **BWT**
4. **MTF**
5. **RLE**
6. **HFC**
7. Merging the blocks

where:
| term    | wiki                                                                    | description               | specification                                   |
| ------- | ----------------------------------------------------------------------- | ------------------------- | ----------------------------------------------- |
| **RLE** | [link](https://en.wikipedia.org/wiki/Run-length_encoding)               | run-length encoding       | [RLE-README](app/transformations/rle/README.md) |
| **BWT** | [link](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform) | Burrows-Wheeler transform | [BWT-README](app/transformations/bwt/README.md) |
| **MTF** | [link](https://en.wikipedia.org/wiki/Move-to-front_transform)           | move-to-front transform   | [MTF-README](app/transformations/mtf/README.md) |
| **HFC** | [link](https://en.wikipedia.org/wiki/Huffman_coding)                    | Huffman coding            | [HFC-README](app/transformations/hfc/README.md) |

