import re


PRAGMA_LINE = '#pragma shadecc_'


class InVar(object):
    def __init__(self, raw_name, var_type, num_elems, line):
        self.raw_name = raw_name
        self.var_type = var_type
        self.num_elements = num_elems
        self.line = line


class Shader(object):
    def __init__(self):
        self.stage = ''
        self.name = ''
        self.glsl_src = ''
        self.instanced_vars = {}
        self.msl_src = ''
        self.hlsl_src = ''
        self.msl_bytes = []
        self.hlsl_bytes = []
        self.uniform_blocks = []


class PragmaProcessor(object):
    def process(self, line, shader, line_num):
        raise NotImplementedError


class StageProcessor(PragmaProcessor):
    def process(self, line, shader, line_num):
        """
        Preprocess `#pragma shadecc_stage`
        :param line:
        :type line:
        :param shader:
        :type shader:
        :param line_num:
        :type line_num:
        :return:
        :rtype:
        """
        shader.stage = line
        return ''


class NameProcessor(PragmaProcessor):
    def __init__(self):
        self.__regex = re.compile(r'"([^"]*)"')

    def process(self, line, shader, line_num):
        """
        Preprocess `#pragma shadecc_name`
        :param line:
        :type line:
        :param shader:
        :type shader:
        :param line_num:
        :type line_num:
        :return:
        :rtype:
        """
        shader.name = self.__regex.findall(line)[0]
        return ''


class InstancedProcessor(PragmaProcessor):
    ALLOWED_TYPES = ['vec1', 'vec2', 'vec3', 'vec4', 'mat4']
    INSTANCE_PREFIX = 'SHADECC_INSTANCED_'

    def __init__(self):
        self.loc_re = re.compile(r'layout \((location[\s]*=[\s]*([0-9]*))\)')

    def process(self, line, shader, line_num):
        """
        Preprocesses a `#pragma shadecc_instanced` declaration, unrolling instanced variables as
        required
        :param line:
        :type line:
        :param shader:
        :type shader:
        :param line_num:
        :type line_num:
        :return:
        :rtype:
        """
        parts = line.split()
        for t in self.ALLOWED_TYPES:
            type_index = parts.index(t) if t in parts else -1
            # Get index of the type and, if matrix, replace with vec type
            if type_index > -1 and t.startswith('mat'):
                mat_elem_count = parts[type_index].replace('mat', '')
                raw_name = parts[type_index + 1]
                inst_name = InstancedProcessor.INSTANCE_PREFIX + raw_name
                # Replace type name, and identifier (prefix with `SHADECC_INSTANCED_`)
                replacement = line.replace('mat', 'in vec').replace(raw_name, inst_name)
                # Add to dict for find/replace later in the code body
                shader.instanced_vars[inst_name] = InVar(raw_name, t, int(mat_elem_count), line_num)
                parts.clear()

                # Unroll the matrix into vec4 variables - for mat4 result will be
                # 4 vec4 elements named e.g. SHADECC_INSTANCED_model_0, SHADECC_INSTANCED_model_1...
                for elem in range(int(mat_elem_count)):
                    parts.append('{0}_{1}'.format(replacement, elem))
                    # gets `layout (location = n)` and replaces with n + 1
                    re_result = self.loc_re.search(parts[elem])
                    loc_str = re_result.group(1)
                    base_loc = re_result.group(2)
                    this_loc = int(base_loc) + elem
                    parts[elem] = parts[elem].replace(loc_str, 'location = ' + str(this_loc)) + ';'
                break
        return '\n'.join(parts)


class Preprocessor(object):
    __pragma_processors = {
        'stage': StageProcessor(),
        'name': NameProcessor(),
        'instanced': InstancedProcessor()
    }

    def process(self, file_contents):
        """
        Preprocesses a shader file and replaces all shadecc #pragma calls with standard GLSL
        :param file_contents:
        :type file_contents:
        :return:
        :rtype:
        """
        shader = Shader()
        lines = file_contents.split('\n')
        lines = [self.__process_pragma(l, shader, i) for i, l in enumerate(lines)]
        lines = '\n'.join(lines).split('\n')
        for name, var in shader.instanced_vars.items():
            lines = self.__replace_instanced_var(name, var, lines)
        shader.glsl_src = '\n'.join(lines).strip() + '\n'
        return shader

    def __replace_instanced_var(self, name, var, lines):
        """
        Replaces all usages of an instanced variable with its modified name and format. For example
        a mat4 instanced variable used like so:

        ```
        gl_Position = viewproj * model * position;
        ```

        Will be replaced with:

        ```
        gl_Position = viewproj * mat4(SHADECC_INSTANCED_model_0, SHADECC_INSTANCED_model_1, ...)
                      * position;
        ```

        :param name: The reformatted name to replace, i.e. SHADECC_INSTANCED_model
        :type name: str
        :param var: The in variable object
        :type var: InVar
        :param lines: List of the shaders source lines
        :type lines: list
        :return: The source lines modified to replace the variable
        :rtype: list
        """
        if var.var_type.startswith('mat'):
            args = ['{0}_{1}'.format(name, i) for i in range(var.num_elements)]
            replacement = '{0}({1})'.format(var.var_type, ', '.join(args))
            result = [l.replace(var.raw_name, replacement) if 'layout' not in l
                      else l
                      for l in lines]
            return result

    def __process_pragma(self, line, shader, line_num):
        """
        Processes a single shadecc #pragma declaration
        :param line:
        :type line:
        :param shader:
        :type shader:
        :param line_num:
        :type line_num:
        :return:
        :rtype:
        """
        if not line.startswith(PRAGMA_LINE):
            return line
        line_parts = line.split()
        directive_name = line_parts[1].replace('shadecc_', '')
        directive_contents = ' '.join(line_parts[2:])
        processor = self.__pragma_processors[directive_name]
        return processor.process(directive_contents, shader, line_num)

