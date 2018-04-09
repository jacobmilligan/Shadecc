import os
import ctypes
import platform

from utils import get_dll_path


class UniformBlock(object):
    def __init__(self, name, member_count, members):
        self.name = name
        self.member_count = member_count
        self.members = members


class SpirvWrapper(object):
    class CUniformBlock(ctypes.Structure):
        _fields_ = [('name', ctypes.c_char_p),
                    ('member_count', ctypes.c_uint32),
                    ("member_names", ctypes.POINTER(ctypes.c_char_p))]

    def __init__(self):
        self.dll = ctypes.cdll.LoadLibrary(get_dll_path('spirv_wrapper'))

    def compile(self, spv_path, glsl_output_path):
        cstring_input = ctypes.c_char_p(spv_path.encode('utf-8'))
        cstring_output = ctypes.c_char_p(glsl_output_path.encode('utf-8'))
        success = self.dll.compile(cstring_input, cstring_output, 330, False)
        if success != 0:
            raise RuntimeError('Unable to compile GLSL')

    def get_uniform_blocks(self, spv_path):
        locations = ctypes.POINTER(SpirvWrapper.CUniformBlock)()
        num_blocks = ctypes.c_uint32()
        spv_cstring = ctypes.c_char_p(spv_path.encode('utf-8'))
        success = self.dll.get_uniform_blocks(spv_cstring,
                                              ctypes.byref(locations),
                                              ctypes.byref(num_blocks))
        if success != 0:
            raise RuntimeError('Unable to compile GLSL')

        blocks = []
        for ub in range(num_blocks.value):
            ub_name = bytes.decode(locations[ub].name)
            member_count = locations[ub].member_count
            members = [bytes.decode(locations[ub].member_names[m]) for m in range(member_count)]
            blocks.append(UniformBlock(ub_name, member_count, members))
        return blocks
