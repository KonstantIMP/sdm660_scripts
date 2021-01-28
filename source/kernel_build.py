from os import system
import subprocess
import platform

def print_hello() :
    print("== == == == == == == == == == == == == == ==")
    print("== Woof!!!                                ==")
    print("== Kernel building for Nokia 7.1 started  ==")
    print("== Script made by : KonstantIMP           ==")
    print("== Take a cup of coffee and wait...       ==")
    print("== == == == == == == == == == == == == == ==")
    print("")

def os_check() :
    if platform.system() != "Linux" :
        print("Sorry! You have to use Linux based michine to run the script")
        print("")
        exit(-1)

def compiler_choose() :
    print("Choose compiler :")
    print("  1. GCC (prebuilt by Google)")
    print("  2. Clang (prebuilt by Google)")
    while True :
        try :
            compiler = int(input("Make your choose : "))
        except Exception :
            print("Incorrect input! Try again!")
        else :
            if compiler != 1 and compiler != 2 : 
                print("Incorrect input! Try again!")
                continue
            print("")
            return compiler

def defconfig_choose() :
    print("Choose kernel config :")
    print("  1. SDM660 defconfig")
    print("  2. SDM660-perfomance defconfig")
    while True :
        try :
            compiler = int(input("Make your choose : "))
        except Exception :
            print("Incorrect input! Try again!")
        else :
            if compiler != 1 and compiler != 2 : 
                print("Incorrect input! Try again!")
                continue
            print("")
            return compiler

def clone_kernel_source() :
    print("Cloning kernel source...")
    system("git clone https://gitlab.com/KonstantIMP/nokia_7_1_stock_kernel.git")
    system("cd nokia_7_1_stock_kernel")
    print("Done...")
    print("")

def clone_gcc_compiler() :
    print("Cloning GCC compiler (prebuilt by Google):")
    system("git clone https://github.com/RaghuVarma331/aarch64-linux-android-4.9.git -b master --depth=1 aarch64-linux-android-4.9")
    print("Done...")
    print("")

def clone_clang_compiler() :
    print("Cloning Clang compiler (prebuilt by Google):")
    system("git clone https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86")
    print("Done...")
    print("")

def gcc_build(d) :
    print("Build started :")
    print("  ARCH=arm64")
    print("  SUBARCH=arm64")
    print("  CROSS_COMPILE=" + __file__[0:-22] + "aarch64-linux-android-4.9/bin/aarch64-linux-android-")
    print("  O=output")

    arch = "ARCH=arm64"
    subarch = "SUBARCH=arm64"
    cross = "CROSS_COMPILE=" + __file__[0:-22] + "aarch64-linux-android-4.9/bin/aarch64-linux-android-"
    out = "O=output"

    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " clean")
    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " mrproper")
    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + (" sdm660_defconfig" if d == 1 else " sdm660-perf_defconfig"))
    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + ' ' + cross + " -j4")

if __name__ == "__main__" :
    print_hello()
    
    os_check()

    compiler = compiler_choose()
    defconfig = defconfig_choose()

    clone_kernel_source()

    if compiler == 1 :
        print("Compiling by GCC")
        print("")

        clone_gcc_compiler()

        gcc_build(defconfig)
    else :
        print("Compiling by Clang")
        print("")

        clone_clang_compiler()

    #clone_kernel_source()