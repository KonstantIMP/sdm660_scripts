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
    CROSS_COMPILE="CROSS_COMPILE=$(pwd)/aarch64-linux-android-4.9/bin/aarch64-linux-android-"
}

build_gcc() {
    cd nokia_7_1_stock_kernel

    sudo make "$OUT" "$ARCH" "$SUBARCH" "$CROSS_COMPILE" clean
    sudo make "$OUT" "$ARCH" "$SUBARCH" "$CROSS_COMPILE" mrproper
    sudo make "$OUT" "$ARCH" "$SUBARCH" "$CROSS_COMPILE" coffee-cappuccino_defconfig
    sudo make "$OUT" "$ARCH" "$SUBARCH" "$CROSS_COMPILE" "-j$(nproc --all)"

    cd ..
}

create_flashable() {
    git clone https://github.com/KonstantIMP/AnyKernel3_nokia_7_1.git -b boot_a
    cp nokia_7_1_stock_kernel/out/arch/arm64/boot/Image.gz-dtb AnyKernel3_nokia_7_1
    find nokia_7_1_stock_kernel/out -name "*.ko" -exec cp {} AnyKernel3_nokia_7_1/modules/system/lib/modules \;
    cd AnyKernel3_nokia_7_1 && zip -r "nokia_7_1_cappucino_$(date +"%d_%m_%H_%M")_a.zip" *
    cp *.zip ../ && cd ..
    rm -rf AnyKernel3_nokia_7_1
}

print_hello;

PS3="Choose compiler : "

select compiler in "1. GCC (prebuilt by Google)" "2. Proton Clang"
do
    #get_kernel_source $1;

    case "$compiler" in
        "1. GCC (prebuilt by Google)" )
            get_gcc_toolchain;
            set_gcc_var;

            build_gcc;
        ;;
        "2. Proton Clang" )
        echo "Build by clang"
        ;;
    esac
break
done

create_flashable;
