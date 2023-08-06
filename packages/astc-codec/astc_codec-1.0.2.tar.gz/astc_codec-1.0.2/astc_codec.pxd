# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from libc.stdint cimport uint8_t
from libcpp cimport bool

cdef extern from "astc_codec.h" namespace "astc_codec":
    # Decompresses ASTC LDR image data to a RGBA32 buffer.
    #
    # Supports formats defined in the KHR_texture_compression_astc_ldr spec and
    # returns UNORM8 values.  sRGB is not supported, and should be implemented
    # by the caller.
    #
    # |astc_data| - Compressed ASTC image buffer, must be at least |astc_data_size|
    #               bytes long.
    # |astc_data_size| - The size of |astc_data|, in bytes.
    # |width| - Image width, in pixels.
    # |height| - Image height, in pixels.
    # |footprint| - The ASTC footprint (block size) of the compressed image buffer.
    # |out_buffer| - Pointer to a buffer where the decompressed image will be
    #                stored, must be at least |out_buffer_size| bytes long.
    # |out_buffer_size| - The size of |out_buffer|, in bytes, at least
    #                     height*out_buffer_stride. If this is too small, this
    #                     function will return false and no data will be
    #                     decompressed.
    # |out_buffer_stride| - The stride that should be used to store rows of the
    #                       decoded image, must be at least 4*width bytes.
    #
    # Returns true if the decompression succeeded, or false if decompression
    # failed, or if the astc_data_size was too small for the given width, height,
    # and footprint, or if out_buffer_size is too small.
    cdef bool _ASTCDecompressToRGBA(const uint8_t*astc_data, size_t astc_data_size,
                                   size_t width, size_t height, uint8_t footprint,
                                   uint8_t*out_buffer, size_t out_buffer_size,
                                   size_t out_buffer_stride);
