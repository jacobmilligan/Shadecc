//
//  Compiler.hpp
//  spirv_wrapper
//
//  --------------------------------------------------------------
//
//  Created by
//  Jacob Milligan on 8/04/2018
//  Copyright (c) 2016 Jacob Milligan. All rights reserved.
//

#pragma once

#include <stdint.h>

extern "C"
{
    typedef struct uniform_block {
        char* name;
        uint32_t member_count;
        char** member_names;
    } uniform_block_t;

    int compile(const char* spv_input, const char* output_path, uint32_t glslversion, bool is_es);
    int get_uniform_blocks(const char* spv_file, uniform_block_t** buffer, uint32_t* block_count);
}
