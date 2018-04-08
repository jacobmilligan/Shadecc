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


#include "spirv_wrapper.hpp"

int main(int argc, char** argv)
{
    compile(argv[1], argv[2], 330, false);
    return 0;
}