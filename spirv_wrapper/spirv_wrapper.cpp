//
//  Compiler.cpp
//  spirv_wrapper
//
//  --------------------------------------------------------------
//
//  Created by
//  Jacob Milligan on 8/04/2018
//  Copyright (c) 2016 Jacob Milligan. All rights reserved.
//

#include "spirv_wrapper.hpp"

#include <spirv_glsl.hpp>

namespace sw {

std::vector<unsigned int> get_spirv(const char* path)
{
    auto file = fopen(path, "rb");
    if (file == nullptr) {
        fprintf(stderr, "spirv_wrapper: unable to open SPIR-V file at location: %s\n", path);
        return {};
    }

    fseek(file, 0, SEEK_END);
    auto size = static_cast<size_t>(ftell(file) / sizeof(unsigned int));
    fseek(file, 0, SEEK_SET);

    std::vector<unsigned int> bits(size);
    auto result = fread(bits.data(), sizeof(unsigned int), size, file);
    if (result != size) {
        fprintf(stderr, "spirv_wrapper: invalid SPIR-V size: %lu\n", size);
        return {};
    }

    fclose(file);
    return std::move(bits);
}

bool write_glsl(const std::string& src, const char* output_dir)
{
    printf("%s\n", output_dir);
    auto file = fopen(output_dir, "w+");
    if (file == nullptr) {
        return false;
    }
    fprintf(file, "%s\n", src.c_str());
    fclose(file);

    return true;
}

void fix_uniforms(spirv_cross::Compiler* compiler)
{
    // Remove locations for samplers
    for (auto& res : compiler->get_shader_resources().sampled_images) {
        compiler->unset_decoration(res.id, spv::DecorationLocation);
    }
}


}

int compile(const char* spv_input, const char* output_path, const uint32_t glslversion,
            const bool is_es)
{
    printf("\n");
    auto spirv = sw::get_spirv(spv_input);

    if (spirv.empty()) {
        return -1;
    }
    
    spirv_cross::CompilerGLSL glsl(spirv);
    auto opts = glsl.get_common_options();
    opts.version = glslversion;
    opts.es = is_es;
    glsl.set_common_options(opts);

    sw::fix_uniforms(&glsl);
    for (auto& res : glsl.get_shader_resources().uniform_buffers) {
        glsl.flatten_buffer_block(res.id);
    }

    auto src = glsl.compile();

    auto result = sw::write_glsl(src, output_path);
    if (!result) {
        fprintf(stderr, "spirv_wrapper: unable to write GLSL file to location: %s\n", output_path);
        return -1;
    }

    return 0;
}