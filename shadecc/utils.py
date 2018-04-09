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


def get_dll_path(lib):
    dll = 'lib' + lib
    system = platform.system()
    if system == 'Darwin':
        dll += '.dylib'
    elif system == 'Windows':
        dll += '.dll'
    else:
        dll += '.so'
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    platform_path = os.path.join(lib_path, system)
    dll_path = os.path.join(platform_path, dll)
    if not os.path.exists(dll_path):
        raise FileNotFoundError('Couldn\'t find a DLL for {0} at expected location: '
                                '{1}'.format(lib, dll_path))
    return dll_path


def call(cmd, working_dir):
    try:
        out = subprocess.check_output(cmd, cwd=working_dir)
        tqdm.write(bytes.decode(out).strip())
    except subprocess.CalledProcessError as err:
        output = bytes.decode(err.output).strip()
        caller = inspect.getouterframes(inspect.currentframe(), 2)
        raise RuntimeError('Command: `{0}` failed with exit code {2}.\nCalled from: `{1}`.'
                           '\n{3}'.format(' '.join(err.cmd), caller[1][3], err.returncode, output))
