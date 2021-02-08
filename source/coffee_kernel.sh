#!/bin/bash

print_hello() {
    echo "== == == == == == == == == == == == == == == =="
    echo "== Woof!!!                                   =="
    echo "== It is a script for building coffee kernel =="
    echo "==             Supported devices : Nokia 7.1 =="
    echo "==                                           =="
    echo "==    This script was made by KonstantIMP    =="
    echo "== == == == == == == == == == == == == == == =="
    echo ""
}

get_kernel_source() {
    echo "Getting kernel source code..."
    if [ -d "nokia_7_1_stock_kernel" ]; then
        echo "Kernel folder exists. Updating source..."
        cd nokia_7_1_stock_kernel
        
        git checkout origin/coffee_kernal_cappuccino
        git pull

        cd ..
    else
        echo "Kernel folder doesn't exist. Cloning..."
        if [ $1 == "KonstantIMP" ]; then
            echo "Good morning, I"
            git clone git@gitlab.com:KonstantIMP/nokia_7_1_stock_kernel.git -b coffee_kernel_cappuccino
        else
            git clone https://gitlab.com/KonstantIMP/nokia_7_1_stock_kernel.git -b coffee_kernel_cappuccino
        fi
    fi
    echo "Done!"
    echo ""
}

get_gcc_toolchain() {
    echo "Getting GCC toolchain (prebuilt by Google)..."
    if [ -d "aarch64-linux-android-4.9" ]; then
        echo "GCC folder exists. Updating binaries..."
        cd aarch64-linux-android-4.9
        git pull
        cd ..
    else
        echo "GCC folder doesn't exist. Cloning..."
        git clone https://github.com/RaghuVarma331/aarch64-linux-android-4.9.git -b master --depth=1 aarch64-linux-android-4.9
    fi
    echo "Done!"
    echo ""
}

set_gcc_var() {
    OUT="O=out"
    ARCH="ARCH=arm64"
    SUBARCH="SUBARCH=arm64"
    CROSS_COMPILE="$(pwd)/aarch64-linux-android-4.9/bin/aarch64-linux-android-"
}

print_hello;

get_kernel_source $1;
get_gcc_toolchain;

set_gcc_var;
