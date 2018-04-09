import glob
import os

import shadecc.metal as metal
import shadecc.utils as utils

from tqdm import tqdm

from shadecc.preprocessor import Preprocessor
from shadecc.template import generate_cpp
from shadecc.spirv_wrapper import SpirvWrapper


def get_src_name(shader):
    """
    Gets a formatted filename for a shader object
    :param shader:
    :return:
    """
    return shader.name + '.' + shader.stage + '.glsl'


def compile_glsl(parent_dir, spv, shader_obj):
    """
    Compiles GLSL from SPIR-V code and flattens all uniform blocks
    :param parent_dir: The shaders parent build directory
    :param spv: SPIR-V file name
    :param shader_obj:
    """
    output_path = get_src_name(shader_obj)
    output_path = os.path.abspath(os.path.join(parent_dir, output_path))
    full_path = os.path.abspath(os.path.join(parent_dir, spv))
    wrapper = SpirvWrapper()
    wrapper.compile(full_path, output_path)
    shader_obj.uniform_blocks = wrapper.get_uniform_blocks(full_path)
    # cmd = [utils.get_bin_path('spirv-cross'), '--version', '330', spv, '--output', output_path,
    #        '--flatten-ubo']
    # utils.call(cmd, parent_dir)
    with open(os.path.join(parent_dir, output_path), 'r') as glsl_file:
        shader_obj.glsl_src = glsl_file.read()


def compile_spirv(output_dir, shader):
    """
    Compiles preprocessed GLSL code to SPIR-V
    :param output_dir: Location to output temp file and .spv
    :param shader:
    :return:
    """
    # write to temp file
    temp_path = os.path.join(output_dir, get_src_name(shader))
    with open(temp_path, 'w') as src:
        src.write(shader.glsl_src)

    spv_name = get_src_name(shader).replace('glsl', 'spv')
    src_name = get_src_name(shader)
    tool = utils.get_bin_path('glslangValidator')
    cmd = [tool, '-S', shader.stage, '-G', '--auto-map-locations', '-o', spv_name, src_name]
    utils.call(cmd, output_dir)

    os.remove(temp_path)
    return spv_name


def build(input_paths, output_dir, pattern, recurse):
    """
    Builds all shaders in the specified input paths, outputting the result into the specified
    output directory
    :param input_paths: list of paths to search for glsl source files
    :param output_dir: directory to output compiled shaders - maintains the corresponding input
    paths folder structure
    :param pattern: The file extension pattern used by all shaders (*.glsl by default)
    :param recurse: If true, will search recursively in all child directories of each input path
    :return:
    """
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

            bar.desc = 'Compiling SPIR-V'
            spv = compile_spirv(path, shader_obj)

            bar.desc = 'Compiling GLSL'
            compile_glsl(path, spv, shader_obj)

            bar.desc = 'Compiling MSL'
            metal.compile(path, spv, shader_obj)

            bar.desc = 'Writing C++ files'
            generate_cpp(output_dir, shader_obj)

            bar.desc = 'Done'

