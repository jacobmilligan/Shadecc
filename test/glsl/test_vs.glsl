#pragma shadecc_stage vert
#pragma shadecc_name "BasicVS"

#version 330 core

out vec4 frag_color;

void main() {
    frag_color = vec4(0.5, 0.5, 0.3, 1.0);
    gl_Position = vec4(0.0, 0.0, 0.0, 0.0);
}