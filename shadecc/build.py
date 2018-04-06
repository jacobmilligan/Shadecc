import glob
import os
import subprocess

import shadecc.metal as metal
import shadecc.bin as bin

from tqdm import tqdm

from shadecc.preprocessor import Preprocessor
from shadecc.template import generate_cpp


def get_src_name(shader):
    return shader.name + '.' + shader.stage + '.glsl'


def compile_spirv(dir, shader):
    spv_name = get_src_name(shader).replace('glsl', 'spv')
    src_name = get_src_name(shader)
    tool = bin.get_path('glslangValidator')
    cmd = [tool, '--aml', '-S', shader.stage, '-G', '-o', spv_name, src_name]
    out = subprocess.check_output(cmd, cwd=dir)
    tqdm.write(bytes.decode(out).strip())
    return spv_name


def dump_src(dir, shader):
    path = os.path.join(dir, get_src_name(shader))
    with open(path, 'w') as src:
        src.write(shader.glsl_src)


def build(input_paths, output_dir, pattern, recurse):
    preprocessor = Preprocessor()
    for in_path in input_paths:
        glob_pattern = os.path.join(in_path, '**') if recurse else in_path
        glob_pattern = os.path.join(glob_pattern, pattern)
        shaders = glob.glob(glob_pattern, recursive=True)
        bar = tqdm(shaders)
        for shader_src in bar:
            location = os.path.dirname(shader_src.replace(in_path, ''))
            location = os.path.sep.join(location.split(os.path.sep)[1:])
            filename = os.path.basename(shader_src)
            bar.postfix = filename

            bar.desc = 'Preprocessing GLSL'
            with open(shader_src, 'r') as file:
                shader_obj = preprocessor.process(file.read())
            path = os.path.join(output_dir, location)
            if not os.path.exists(path):
                os.mkdir(path)
            dump_src(path, shader_obj)

            bar.desc = 'Compiling SPIR-V'
            spv = compile_spirv(path, shader_obj)
            bar.desc = 'Compiling MSL'
            metal.compile(path, spv, shader_obj)
            bar.desc = 'Writing C++ files'
            generate_cpp(output_dir, shader_obj)
            bar.desc = 'Done'

