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

int get_uniform_blocks(const char* spv_file, uniform_block_t** buffer, uint32_t* block_count)
{
    auto spirv = sw::get_spirv(spv_file);
    if (spirv.empty()) {
        return -1;
    }

    spirv_cross::CompilerGLSL compiler(spirv);
    auto resources = compiler.get_shader_resources();
    *block_count = static_cast<uint32_t>(resources.uniform_buffers.size());
    *buffer = static_cast<uniform_block*>(malloc(sizeof(uniform_block) * *block_count));

    uint32_t ub = 0;
    std::vector<const char*> names;
    for (auto& res : resources.uniform_buffers) {
        names.clear();
        auto cur_ub = &(*buffer)[ub];
        auto type = compiler.get_type(res.type_id);
        auto num_members = type.member_types.size();

        cur_ub->name = static_cast<char*>(malloc(res.name.length() * sizeof(char)));
        strcpy(cur_ub->name, res.name.c_str());
        cur_ub->member_count = static_cast<uint32_t>(num_members);

        for (uint32_t i = 0; i < num_members; ++i) {
            const auto& name = compiler.get_member_name(res.base_type_id, i);
            names.push_back(name.c_str());
        }

        auto size = names.size() * sizeof(char*);
        cur_ub->member_names = static_cast<char**>(malloc(size));
        for (int j = 0; j < names.size(); ++j) {
            cur_ub->member_names[j] = static_cast<char*>(malloc(strlen(names[j]) * sizeof(char*)));
            strcpy(cur_ub->member_names[j], names[j]);
        }
        ++ub;
    }

    return 0;
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