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
        print("Sorry! You have to use Linux based michine to run the script")
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

def choose_option(choose_name, options_list) :
    print(choose_name + ' :')
    for i in range(len(options_list)) :
        print('\t' + str(i + 1) + '. ' + options_list[i])

    print('')

    while True :
        answer = int(input('Enter your answer : '))

        if answer <= 0 or answer > len(options_list) :
            print('  [ERROR] Incorrect number. Try again')
            print('')
        else :
            print('')
            return answer

def get_vendor() :
    answer = choose_option('Choose vendor version', ['Stock Android 10 vendor', 'Stock Android 10 vendor modified by RaghuVarma', 'Community Vendor 11'])

if __name__ == '__main__' :
    print_hello()

    os_check()

    gsi_path = get_gsi_path()
    rom_name = get_rom_name()

    get_vendor()