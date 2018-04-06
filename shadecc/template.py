import os


def generate_cpp(output_dir, shader):
    template_location = os.path.join(os.path.dirname(__file__), 'templates')
    with open(os.path.join(template_location, 'header.hpp')) as file:
        header_tmpl = file.read()
    with open(os.path.join(template_location, 'source.cpp')) as file:
        src_tmpl = file.read()

    data = {}
    for key, value in vars(shader).items():
        if type(value) == list:
            data[key] = ', '.join(hex(elem) for elem in value)
        else:
            data[key] = '{}'.format(value)

    header_out = header_tmpl.format(**data)
    src_out = src_tmpl.format(**data)

    with open(os.path.join(output_dir, shader.name + '.hpp'), 'w') as file:
        file.write(header_out)
    with open(os.path.join(output_dir, shader.name + '.cpp'), 'w') as file:
        file.write(src_out)
