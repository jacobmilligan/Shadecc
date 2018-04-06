import os
import platform


def get_path(tool):
    bin_path = os.path.join(os.path.dirname(__file__), 'bin')
    os_path = os.path.join(bin_path, platform.system())
    tool_path = os.path.join(os_path, tool)
    assert os.path.exists(tool_path), 'Tool {0} is found at path {1}'.format(tool, tool_path)
    return tool_path
