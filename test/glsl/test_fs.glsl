#pragma shadecc_stage frag
#pragma shadecc_name "BasicFS"

#version 330 core

in vec4 frag_color;

out vec4 color_out;

void main() {
    color_out = frag_color;
}