//
//  main.cpp
//  spirv_wrapper
//
//  --------------------------------------------------------------
//
//  Created by
//  Jacob Milligan on 8/04/2018
//  Copyright (c) 2016 Jacob Milligan. All rights reserved.
//


#include <cstdio>
#include "spirv_wrapper.hpp"

#include "../test/build/BasicTextureVS.hpp"

int main(int argc, char** argv)
{
//    compile(argv[1], argv[2], 330, false);
//    uniform_block* buf = nullptr;
//    uint32_t num_blocks;
//    auto success = get_uniform_blocks(argv[1], &buf, &num_blocks);

    auto blocks = BasicTextureVS::source.uniform_blocks;
    for (int i = 0; i < BasicTextureVS::source.num_uniform_blocks; ++i) {
        for (int j = 0; j < blocks[i].num_members; ++j) {
            printf("%s\n", blocks[i].members[j]);
        }
    }

    return 0;
}