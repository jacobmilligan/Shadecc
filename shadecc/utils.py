import os
import platform
import subprocess
import inspect
import ctypes

from tqdm import tqdm


def get_bin_path(tool):
    bin_path = os.path.join(os.path.dirname(__file__), 'bin')
    os_path = os.path.join(bin_path, platform.system())
    tool_path = os.path.join(os_path, tool)
    assert os.path.exists(tool_path), 'Tool {0} is found at path {1}'.format(tool, tool_path)
    return tool_path


def spirv_wrapper_compile(input, output):
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    lib_path = os.path.join(lib_path, platform.system())
    for f in os.listdir(lib_path):
        if 'spirv_wrapper' in f:
            lib_path = os.path.join(lib_path, f)
    lib = ctypes.cdll.LoadLibrary(lib_path)
    success = lib.compile(ctypes.c_char_p(input.encode('utf-8')),
                          ctypes.c_char_p(output.encode('utf-8')),
                          330, False)
    if success != 0:
        raise RuntimeError('Unable to compile GLSL')


def call(cmd, working_dir):
    try:
        out = subprocess.check_output(cmd, cwd=working_dir)
        tqdm.write(bytes.decode(out).strip())
    except subprocess.CalledProcessError as err:
        output = bytes.decode(err.output).strip()
        caller = inspect.getouterframes(inspect.currentframe(), 2)
        raise RuntimeError('Command: `{0}` failed with exit code {2}.\nCalled from: `{1}`.'
                           '\n{3}'.format(' '.join(err.cmd), caller[1][3], err.returncode, output))
