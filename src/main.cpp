// Copyright (C) 2018-2019 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include <string>
#include <iostream>

#ifdef UNICODE
#include <tchar.h>
#endif

#ifndef UNICODE
#define tcout std::cout
#define _T(STR) STR
#else
#define tcout std::wcout
#endif

#define EXIT_FAILURE 1
#define EXIT_SUCCESS 0

#ifndef UNICODE
int main(int argc, char *argv[]) {
#else
int wmain(int argc, wchar_t *argv[]) {
#endif

    try {

        // ------------------------------ Parsing and validation of input args ---------------------------------
        if (argc != 2) {
            tcout << _T("Usage : ./hello_world <your_name>") << std::endl;
            return EXIT_FAILURE;
        }
        tcout << "Hello " << argv[1] << "!" << std::endl;



    } catch (const std::exception & ex) {
        std::cerr << ex.what() << std::endl;
        return EXIT_FAILURE;
    }
    std::cout << "This sample demonstrates scone compiled C++ binary running in TEE environment" << std::endl;
    return EXIT_SUCCESS;
}
