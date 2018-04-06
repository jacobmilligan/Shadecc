//
//  Shadecc.hpp
//  Shadecc
//
//  --------------------------------------------------------------
//
//  Created by
//  Jacob Milligan on 15/02/2018
//  Copyright (c) 2016 Jacob Milligan. All rights reserved.
//

#include <cstdint>

namespace shadecc {


/// Contains the translated source and bytecode for a given shader.
struct ShaderSource {
    const char* name;
    /// String containing the shader source translated to GLSL
    const char* glsl_src;
    /// String containing the shader source translated to MSL
    const char* msl_src;
    /// String containing the shader source translated to HLSL
    const char* hlsl_src;
    /// Array containing the bytecode of the shader source translated to MSL
    const uint8_t* msl_bytecode;
    /// Array containing the bytecode of the shader source translated to HLSL
    const uint8_t* hlsl_bytecode;
};


} // namespace shadecc