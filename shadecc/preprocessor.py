import re


PRAGMA_LINE = '#pragma shadecc_'


class InVar(object):
    def __init__(self, var_type, num_elems, line):
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
        shader.stage = line
        return ''


class NameProcessor(PragmaProcessor):
    def __init__(self):
        self.__regex = re.compile(r'"([^"]*)"')

    def process(self, line, shader, line_num):
        shader.name = self.__regex.findall(line)[0]
        return ''


class InstancedProcessor(PragmaProcessor):
    ALLOWED_TYPES = ['vec1', 'vec2', 'vec3', 'vec4', 'mat4']

    def __init__(self):
        self.loc_re = re.compile(r'layout \((location[\s]*=[\s]*([0-9]*))\)')

    def process(self, line, shader, line_num):
        parts = line.split()
        for t in self.ALLOWED_TYPES:
            index = parts.index(t) if t in parts else -1
            if index > -1 and t.startswith('mat'):
                num_elems = parts[index].replace('mat', '')
                name = parts[index + 1]
                replacement = line.replace('mat', 'in vec')
                shader.instanced_vars[name] = InVar(t, int(num_elems), line_num)

                parts.clear()
                for elem in range(int(num_elems)):
                    parts.append('{0}_{1}'.format(replacement, elem))
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
        shader = Shader()
        lines = file_contents.split('\n')
        lines = [self.__process_pragma(l, shader, i) for i, l in enumerate(lines)]
        lines = '\n'.join(lines).split('\n')
        for name, var in shader.instanced_vars.items():
            lines = self.__replace_instanced_var(name, var, lines)
        shader.glsl_src = '\n'.join(lines).strip() + '\n'
        return shader

    def __replace_instanced_var(self, name, var, lines):
        if var.var_type.startswith('mat'):
            args = ['{0}_{1}'.format(name, i) for i in range(var.num_elements)]
            replacement = '{0}({1})'.format(var.var_type, ', '.join(args))
            return [l.replace(name, replacement) if 'layout' not in l else l for l in lines]

    def __process_pragma(self, line, shader, line_num):
        if not line.startswith(PRAGMA_LINE):
            return line
        line_parts = line.split()
        directive_name = line_parts[1].replace('shadecc_', '')
        directive_contents = ' '.join(line_parts[2:])
        processor = self.__pragma_processors[directive_name]
        return processor.process(directive_contents, shader, line_num)

