import subprocess
import os
import shadecc.bin as bin

from tqdm import tqdm


def compile_msl_src(src_path, spv, output_path, shader):
    cmd = [bin.get_path('spirv-cross'), '--output', output_path, spv, '--msl', '--msl-version',
           '2']
    output = subprocess.check_output(cmd, cwd=src_path)
    if len(output) > 0:
        tqdm.write(bytes.decode(output).strip())


def compile(src_path, spv, shader):
    msl_src_path = shader.name + '.metal'
    air_path = shader.name + '.air'
    lib_path = shader.name + '.metallib'

    compile_msl_src(src_path, spv, msl_src_path, shader)

    cmd = ['xcrun', '-sdk', 'macosx', 'metal', msl_src_path, '-o', air_path]
    output = subprocess.check_output(cmd, cwd=src_path)
    if len(output) > 0:
        tqdm.write(bytes.decode(output).strip())

    cmd = ['xcrun', '-sdk', 'macosx', 'metallib', air_path, '-o', lib_path]
    output = subprocess.check_output(cmd, cwd=src_path)
    if len(output) > 0:
        tqdm.write(bytes.decode(output).strip())

    with open(os.path.join(src_path, lib_path), 'rb') as lib_file:
        shader.msl_bytes = list(lib_file.read())

    with open(os.path.join(src_path, msl_src_path), 'r') as src_file:
        shader.msl_src = src_file.read()

    os.remove(os.path.join(src_path, air_path))
    os.remove(os.path.join(src_path, lib_path))

