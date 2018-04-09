import os

from tqdm import tqdm


class TemplateEngine(object):
    def __init__(self):
        self.root = os.path.join(os.path.dirname(__file__), 'templates')
        self.templates = {}
        for tmpl in os.listdir(self.root):
            tmpl_path = os.path.join(self.root, tmpl)
            with open(tmpl_path) as file:
                without_ext = os.path.splitext(os.path.basename(tmpl_path))[0]
                self.templates[without_ext] = file.read()

    def render(self, template, data):
        tmpl_string = self.templates.get(template)
        if tmpl_string is None:
            tqdm.write('Shadecc: unable to find a template named {}'.format(template))
            return
        return tmpl_string.format(**data)



def generate_cpp(output_dir, shader):
    templates = TemplateEngine()
    data = {
        'uniform_block_members': ''
    }
    for key, value in vars(shader).items():
        if key == 'uniform_blocks':
            data['uniform_block_count'] = len(value)
            result = []
            for ub in value:
                members = templates.render('uniform_block_members', {
                    'block_name': ub.name,
                    'member_names': ', '.join('"{}"'.format(mem) for mem in ub.members)
                })
                data['uniform_block_members'] += members + '\n'

                ub = templates.render('uniform_block', {
                    'name': ub.name,
                    'member_count': ub.member_count,
                })
                result.append(ub)
            data[key] = ', '.join(result)
        elif type(value) == list:
            data[key] = ', '.join(hex(elem) for elem in value)
        else:
            data[key] = '{}'.format(value)

    header_out = templates.render('header', data)
    src_out = templates.render('source', data)

    with open(os.path.join(output_dir, shader.name + '.hpp'), 'w') as file:
        file.write(header_out)
    with open(os.path.join(output_dir, shader.name + '.cpp'), 'w') as file:
        file.write(src_out)
