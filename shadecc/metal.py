import os
import shadecc.utils as utils


def compile_msl_src(src_path, spv, output_path, shader):
    cmd = [utils.get_bin_path('spirv-cross'), '--output', output_path, spv, '--msl',
           '--msl-version', '2']
    utils.call(cmd, src_path)


def compile(src_path, spv, shader):
    msl_src_path = shader.name + '.metal'
    air_path = shader.name + '.air'
    lib_path = shader.name + '.metallib'

    compile_msl_src(src_path, spv, msl_src_path, shader)

    cmd = ['xcrun', '-sdk', 'macosx', 'metal', msl_src_path, '-o', air_path]
    utils.call(cmd, src_path)

    cmd = ['xcrun', '-sdk', 'macosx', 'metallib', air_path, '-o', lib_path]
    utils.call(cmd, src_path)

    with open(os.path.join(src_path, lib_path), 'rb') as lib_file:
        shader.msl_bytes = list(lib_file.read())

    with open(os.path.join(src_path, msl_src_path), 'r') as src_file:
        shader.msl_src = src_file.read()
    
    os.remove(os.path.join(src_path, air_path))
    os.remove(os.path.join(src_path, lib_path))

