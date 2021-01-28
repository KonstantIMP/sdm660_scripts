from os import system
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

def clone_kernel_source() :
    print("Cloning kernel source...")
    system("git clone https://gitlab.com/KonstantIMP/nokia_7_1_stock_kernel.git")
    print("Done...")
    print("")

def clone_gcc_compiler() :
    print("Cloning GCC compiler (prebuilt by Google):")
    system("git clone https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9")
    print("Done...")
    print("")

def get_clang_compiler() :
    print("Cloning Clang compiler (prebuilt by Google):")
    system("git clone https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86")
    print("Done...")
    print("")

if __name__ == "__main__" :
    print_hello()
    
    os_check()

    if compiler_choose() == 1 :
        print("Compiling by GCC")
        print("")
    else :
        print("Compiling by Clang")
        print("")

    #clone_kernel_source()