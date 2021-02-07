from os import system
import subprocess
import platform

def print_hello() :
    print("== == == == == == == == == == == == == == ==")
    print("== Woof!!!                                ==")
    print("== Kernel building for Nokia 7.1 started  ==")
    print("== Script was made by : KonstantIMP       ==")
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
    print("  3. SDM636-perfomance defconfig")
    while True :
        try :
            compiler = int(input("Make your choose : "))
        except Exception :
            print("Incorrect input! Try again!")
        else :
            if compiler != 1 and compiler != 2 and compiler != 3 : 
                print("Incorrect input! Try again!")
                continue
            print("")
            return compiler

def clone_kernel_source() :
    print('Cloning kernel source...')
    system('git clone https://gitlab.com/KonstantIMP/nokia_7_1_stock_kernel.git -b dev')
    system('cd nokia_7_1_stock_kernel')
    print('Done...')
    print('')

def clone_gcc_compiler() :
    print("Cloning GCC compiler (prebuilt by Google):")
    system("git clone https://github.com/RaghuVarma331/aarch64-linux-android-4.9.git -b master --depth=1 aarch64-linux-android-4.9")
    print("Done...")
    print("")

def clone_clang_compiler() :
    print("Cloning Clang compiler (prebuilt by Google):")
    system("git clone https://github.com/RaghuVarma331/clang.git -b android-11.0 --depth=1 clang")
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

    if d == 1 : system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm660_defconfig")
    elif d == 2 : system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm660-perf_defconfig")
    else : system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm636-perf_defconfig")
    
    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " prepare")

    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + ' ' + cross + " -j4")
    system("cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + ' ' + cross + " modules")

    print("Done...")
    print("")

def clang_build(d) :
    print("Build started :")
    print("  CC=clang")
    print("  ARCH=arm64")
    print("  SUBARCH=arm64")
    print("  CLANG_TRIPLE=" + __file__[0:-22] + "clang/bin/aarch64-linux-gnu-")
    print("  CROSS_COMPILE=" + __file__[0:-22] + "aarch64-linux-android-4.9/bin/aarch64-linux-android-")
    print("  O=output")

    cc = "CC=clang"
    arch = "ARCH=arm64"
    subarch = "SUBARCH=arm64"
    cross = "CROSS_COMPILE=aarch64-linux-android-"
    triple = "CLANG_TRIPLE=aarch64-linux-gnu-"
    out = "O=output"

    path_ex = "export PATH=" + __file__[0:-22] + "clang/bin:" + __file__[0:-22] + "aarch64-linux-android-4.9/bin:${PATH} && "

    system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " clean")
    system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " mrproper")
    
    if d == 1 : system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm660_defconfig")
    elif d == 2 : system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm660-perf_defconfig")
    else : system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " sdm636-perf_defconfig")

    system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + arch + ' ' + subarch + " prepare")

    system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + cc + ' ' + triple + ' ' + arch + ' ' + subarch + ' ' + cross + " -j4")
    system(path_ex + "cd nokia_7_1_stock_kernel && sudo make " + out + ' ' + cc + ' ' + triple + ' ' + arch + ' ' + subarch + ' ' + cross + " modules")

    print("Done...")
    print("")

def create_flashable(c, d) :
    print("Creating flashable .ZIP for A slot :")
    system("git clone https://github.com/KonstantIMP/AnyKernel3_nokia_7_1.git -b boot_a")
    system("cp nokia_7_1_stock_kernel/output/arch/arm64/boot/Image.gz-dtb AnyKernel3_nokia_7_1")
    system("find nokia_7_1_stock_kernel/output -name \"*.ko\" -exec cp {} AnyKernel3_nokia_7_1/modules/system/lib/modules \\;")
    system("cd AnyKernel3_nokia_7_1 && zip -r nokia_7_1_" + ("sdm660_" if d == 1 else "sdm660-perf_") + ("gcc" if c == 1 else "clang") + "_a.zip *")
    system("cp AnyKernel3_nokia_7_1/nokia_7_1_*.zip ./")
    system("rm -rf AnyKernel3_nokia_7_1")

    print("Creating flashable .ZIP for B slot :")
    system("git clone https://github.com/KonstantIMP/AnyKernel3_nokia_7_1.git -b boot_b")
    system("cp nokia_7_1_stock_kernel/output/arch/arm64/boot/Image.gz-dtb AnyKernel3_nokia_7_1")
    system("find nokia_7_1_stock_kernel/output -name \"*.ko\" -exec cp {} AnyKernel3_nokia_7_1/modules/system/lib/modules \\;")
    system("cd AnyKernel3_nokia_7_1 && zip -r nokia_7_1_" + ("sdm660_" if d == 1 else "sdm660-perf_") + ("gcc" if c == 1 else "clang") + "_b.zip *")
    system("cp AnyKernel3_nokia_7_1/nokia_7_1_*.zip ./")
    system("rm -rf AnyKernel3_nokia_7_1")
    
    print("Done...")
    print("")

def print_bye() :
    print("== == == == == == == == == == == == == == == == == ==")
    print("== Thank you for script using!                     ==")
    print("== You can make some usefull changes for it        ==")
    print("== And upload it to GitHub (by Pull Request)       ==")
    print("==                                                 ==")
    print("== Or you can buy me a coffee :-D                  ==")
    print("== Here : https://sobe.ru/na/coffee_and_learning   ==")
    print("== == == == == == == == == == == == == == == == == ==")
    print("")

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
        clone_gcc_compiler() #Haha, but it`s true

        clang_build(defconfig)

    create_flashable(compiler, defconfig)

    print_bye()
