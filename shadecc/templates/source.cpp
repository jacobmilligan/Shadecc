//
//  {name}.hpp
//
//  --------------------------------------------------------------
//
//  This file was generated by the Shadecc tool.
//
//  This code will be overwritten if re-generated and could break things badly if
//  edited manually.
//

#include "{name}.hpp"

#include <cstdint>

namespace {name} {{


////////////////////////////////
/// Byte code definitions
////////////////////////////////


static constexpr uint8_t msl_bytes[] = {{
    {msl_bytes}
}};

static constexpr uint8_t hlsl_bytes[] = {{
    {hlsl_bytes}
}};

////////////////////////////////
/// Uniform Block definitions
////////////////////////////////

{uniform_block_members}

static constexpr shadecc::UniformBlock ub_list[] = {{
    {uniform_blocks}
}};


////////////////////////////////
/// Source definitions
////////////////////////////////

shadecc::ShaderSource source = {{
    "{name}",
    R"({glsl_src})",
    R"({msl_src})",
    R"({hlsl_src})",
    msl_bytes,
    hlsl_bytes,
    {uniform_block_count},
    ub_list,
    {is_instanced}
}};


}} // namespace {name}