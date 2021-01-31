from os import system
from os import path
import subprocess
import platform

def print_hello() :
    print('== == == == == == == == == == == == == == ==')
    print('== Woof!                                  ==')
    print('== Script for creating stable ports       ==')
    print('==             of GSI ROMs for Nokia 7.1  ==')
    print('== Script was made by KonstantIMP         ==')
    print('== Take a cup of coffee and wait...       ==')
    print('== == == == == == == == == == == == == == ==')
    print('')

def os_check() :
    if platform.system() != "Linux" :
        print("Sorry! You have to use Linux based machine to run the script")
        print("")
        exit(-1)

def get_gsi_path() :
    while True :
        gsi_path = input('Enter full path to the GSI .img file : ')

        if path.exists(gsi_path) == True and path.isfile(gsi_path) == True :
            print('')
            return gsi_path
        print('Error! File doesn\'t exist or it is a folder')

def get_rom_name() :
    rom_name = input('Enter ROMs name (will be used for archive creating) : ')
    print('')
    return rom_name

def create_rom_dir(name) :
    print('Creating working directory...')
    system('mkdir ' + name + '_working')
    print('Creating output directory...')
    system('mkdir ' + name)
    print('Done!')
    print('')

def choose_option(choose_name, options_list) :
    print(choose_name + ' :')
    for i in range(len(options_list)) :
        print('\t' + str(i + 1) + '. ' + options_list[i])

    print('')

    while True :
        answer = int(input('Enter your answer : '))

        if answer <= 0 or answer > len(options_list) :
            print('[ERROR] Incorrect number. Try again')
            print('')
        else :
            print('')
            return answer

def get_system(s_path, name) :
    print('Coping system image to work directory...')
    system('cp ' + s_path + ' ' + name + '_working/system.img')

def get_vendor(name) :
    answer = choose_option('Choose vendor version', ['Stock Android 10 vendor', 'Stock Android 10 vendor modified by RaghuVarma', 'Community Vendor 11'])

    if answer == 1 :
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_stock.img -o ' + name + '_working/vendor.img')
    elif answer == 2 :
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_stock_by_RaghuVarma.img -o ' + name + '_working/vendor.img')
    else :
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_community.img -o ' + name + '_working/vendor.img')

    print('')

def get_boot(name) :
    print('Getting stock boot image...')
    system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/boot/boot.img ' + name + '_working/boot.img')
    print('Done!')
    print('')

if __name__ == '__main__' :
    print_hello()

    os_check()

    gsi_path = get_gsi_path()
    rom_name = get_rom_name()

    create_rom_dir(rom_name)

    get_system(gsi_path, rom_name)
    get_vendor(rom_name)
    get_boot(rom_name)