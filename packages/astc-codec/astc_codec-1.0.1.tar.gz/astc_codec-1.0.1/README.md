# ASTC_Codec
An ASTC decoder for PIL.

The decoder uses [Google/astc-codec](https://github.com/google/astc-codec) to decompress the data.


## Installation
- Cython required
### PIP
```
pip install astc_codec
```
### Manual
```cmd
python setup.py install
```


## Usage
### valid block_sizes

|block size | footprint | footprint id |
|---|---|---|
| (4, 4) | k4x4 | 0 |
| (5, 4) | k5x4 | 1 |
| (5, 5) | k5x5 | 2 |
| (6, 5) | k6x5 | 3 |
| (6, 6) | k6x6 | 4 |
| (8, 5) | k8x5 | 5 |
| (8, 6) | k8x6 | 6 |
| (10, 5) | k10x5 | 7 |
| (10, 6) | k10x6 | 8 |
| (8, 8) | k8x8 | 9 |
| (10, 8) | k10x8 | 10 |
| (10, 10) | k10x10 | 11 |
| (12, 10) | k12x10 | 12 |
| (12, 12) | k12x12 | 13 |

### PIL.Image decoder
```python
from PIL import Image
import astc_codec 
#needs to be imported once in the active code, so that the codec can register itself

raw_astc_image_data : bytes
block_size = (int, int) # see valid block_sizes
img = Image.frombytes('RGBA', size, raw_astc_image_data, 'astc', block_size)
```

### raw decoder
```python
from astc_codec import decompress_astc, ASTCDecompressToRGBA

# ASTC to RGBA
rgba_data = decompress_astc(astc_data : bytes, block_size : (int, int), width : int, height : int)

# ASTC to RGBA, direct mapping to the C++ function
# footprint = footprint id from valid block_sizes
rgba_data = ASTCDecompressToRGBA(astc_data : bytes, astc_data_size : int,
    width : int, height : int, footprint : int, out_buffer_size : int,
    out_buffer_stride : int)
```