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
    int compile(const char* spv_input, const char* output_path, uint32_t glslversion, bool is_es);
}
