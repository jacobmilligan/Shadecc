#pragma shadecc_stage frag
#pragma shadecc_name "BasicTextureFS"

#version 330 core

uniform sampler2D tex;

in vec4 frag_color;
in vec2 frag_tex;

out vec4 color_out;

void main() {
    vec4 tex_sample = texture(tex, frag_tex);
    color_out = tex_sample;
}
