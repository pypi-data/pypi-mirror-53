from PIL import Image, ImageFile
import io

from astc_codec cimport *


# define decoder
class ASTCDecoder(ImageFile.PyDecoder):
    dstChannelBytes = 1
    dstChannels = 4

    def decode(self, buffer):
        if isinstance(buffer, (io.BufferedReader, io.BytesIO)):
            data = buffer.read()
        else:
            data = buffer
        self.set_as_raw(decompress_astc(data, (self.args[0], self.args[1]), self.state.xsize, self.state.ysize))
        return -1, 0


def decompress_astc(astc_data : bytes, block_format : tuple, width : int, height : int) -> bytes:
    """
    Decompresses ASTC LDR image data to a RGBA32 buffer.
    Supports formats defined in the KHR_texture_compression_astc_ldr spec and
    returns UNORM8 values.  sRGB is not supported, and should be implemented
    by the caller.
    :param astc_data: - Compressed ASTC image buffer, must be at least |astc_data_size|
        bytes long.
    :param block_format: - Format of the block (xdim, ydim).
    :param width: - Image width, in pixels.
    :param height: - Image height, in pixels.
    :returns: - Returns a buffer where the decompressed image will be
        stored, must be at least |out_buffer_size| bytes long if decompression succeeded,
        or b'' if it failed or if the astc_data_size was too small for the given width, height,
        and footprint, or if out_buffer_size is too small.
    """
    cdef size_t astc_data_size = len(astc_data)
    cdef size_t out_buffer_size = width * height * 4
    cdef size_t out_buffer_stride = width * 4
    out_buffer = bytes(out_buffer_size)
    if _ASTCDecompressToRGBA(<const uint8_t*> astc_data, astc_data_size,
                             <size_t> width, <size_t> height, <uint8_t> FOOTPRINT[block_format],
                             <uint8_t*> out_buffer, out_buffer_size,
                             out_buffer_stride):
        return out_buffer
    else:
        return b''

def ASTCDecompressToRGBA(astc_data : bytes, astc_data_size : int,
                         width : int, height : int, footprint : int, out_buffer_size : int,
                         out_buffer_stride : int):
    """
    Decompresses ASTC LDR image data to a RGBA32 buffer.
    Supports formats defined in the KHR_texture_compression_astc_ldr spec and
    returns UNORM8 values.  sRGB is not supported, and should be implemented
    by the caller.
    :param astc_data: - Compressed ASTC image buffer, must be at least |astc_data_size|
                bytes long.
    :param astc_data_size: - The size of |astc_data|, in bytes.
    :param width: - Image width, in pixels.
    :param height: - Image height, in pixels.
    :param footprint: - The ASTC footprint (block size) of the compressed image buffer.
    :param out_buffer_size: - The size of |out_buffer|, in bytes, at least
                height*out_buffer_stride. If this is too small, this
                function will return false and no data will be
                decompressed.
    :param out_buffer_stride: - The stride that should be used to store rows of the
                decoded image, must be at least 4*width bytes.
    :returns: - Returns a buffer where the decompressed image will be
                stored, must be at least |out_buffer_size| bytes long if decompression succeeded,
                or b'' if it failed or if the astc_data_size was too small for the given width, height,
                and footprint, or if out_buffer_size is too small.
    """
    out_buffer = bytes(out_buffer_size)
    if _ASTCDecompressToRGBA(<const uint8_t*> astc_data, <size_t> astc_data_size,
                             <size_t> width, <size_t> height, <uint8_t> footprint,
                             <uint8_t*> out_buffer, <size_t> out_buffer_size,
                             <size_t> out_buffer_stride):
        return out_buffer
    else:
        return b''

FOOTPRINT = {
    (4, 4): 0,
    (5, 4): 1,
    (5, 5): 2,
    (6, 5): 3,
    (6, 6): 4,
    (8, 5): 5,
    (8, 6): 6,
    (10, 5): 7,
    (10, 6): 8,
    (8, 8): 9,
    (10, 8): 10,
    (10, 10): 11,
    (12, 10): 12,
    (12, 12): 13,
}

# register decoder
if 'astc' not in Image.DECODERS:
    Image.register_decoder('astc', ASTCDecoder)
