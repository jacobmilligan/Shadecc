#!/usr/bin/env python3

import argparse

from shadecc.build import build


def main():
    cli = argparse.ArgumentParser(prog='shadecc',
                                  description='Cross compile GLSL shaders to HLSL, GLSL, and MSL')
    cli.add_argument('-i', '--input', help='List of paths containing shader files',
                     required=True, nargs='*', type=str)
    cli.add_argument('-o', '--output', help='The directory to output all shader C++ source code',
                     required=True)
    cli.add_argument('-r', '--recursive', action='store_true',
                     help='Searches paths given in <input_path> recursively for GLSLfiles. '
                          'Enabled by default', default=True)
    cli.add_argument('-p', '--pattern', type=str,
                     help='File extension pattern to use when searching for GLSL files. *.glsl '
                          'by default', default='*.glsl')
    args = cli.parse_args()

    build(args.input, args.output, args.pattern, args.recursive)

