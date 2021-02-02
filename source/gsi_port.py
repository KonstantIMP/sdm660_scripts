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
    system('mkdir ' + name + '_working/m_system')
    system('mkdir ' + name + '_working/m_vendor')
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
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_stock.img -O ' + name + '_working/vendor.img')
    elif answer == 2 :
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_stock_by_RaghuVarma.img -O ' + name + '_working/vendor.img')
    else :
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/vendor/vendor_community.img -O ' + name + '_working/vendor.img')

    print('')

def get_boot(name) :
    print('Getting stock boot image...')
    system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/boot/boot.img -O ' + name + '_working/boot.img')
    print('Done!')
    print('')

def mount_system(name) :
    print('Mount system image...')
    system('sudo simg2img ' + name + '_working/system.img ' + name + '_working/system.img.ext')
    system('sudo mount -o rw,loop ' + name + '_working/system.img.ext ' + name + '_working/m_system')
    print('Done!!!')
    print('')

def mount_vendor(name) :
    print('Mount vendor image...')
    system('sudo mount -o rw,loop ' + name + '_working/vendor.img ' + name + '_working/m_vendor')
    print('Done!')
    print('')

def vendor_change(name) :
    print('Start working with vendor :')
    
    answer = choose_option('Include Bluetooth Headset fix(Android 10 mostly)', ['Yes', 'No'])
    if answer == 1 :
        print('Getting fixed audio policy :')
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/patch/audio_policy_configuration.xml?inline=false -O ' + name + '_working/audio_policy_configuration.xml')

        print('Fixing process...')
        system('sudo rm' + name + '_working/m_vendor/etc/audio_policy_configuration.xml')
        system('sudo rm' + name + '_working/m_vendor/etc/audio/audio_policy_configuration.xml')
        system('sudo cp ' + name + '_working/audio_policy_configuration.xml ' + name + '_working/m_vendor/etc/audio_policy_configuration.xml')
        system('sudo cp ' + name + '_working/audio_policy_configuration.xml ' + name + '_working/m_vendor/etc/audio/audio_policy_configuration.xml')
        system('sudo chmod 644 ' + name + '_working/m_vendor/etc/audio_policy_configuration.xml')
        system('sudo chmod 644 ' + name + '_working/m_vendor/etc/audio/audio_policy_configuration.xml')

        print('Done!')
        print('')

    answer = choose_option('Include AOD and adaptive brightness', ['Yes', 'No'])
    if answer == 1 :
        print('Getting overlay .apk...')
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/patch/framework-res__auto_generated_rro.apk -O ' + name + '_working/framework-res__auto_generated_rro.apk')

        print('Fixing process...')
        system('sudo mkdir ' + name + '_working/m_vendor/overlay')
        system('sudo cp ' + name + '_working/framework-res__auto_generated_rro.apk ' + name + '_working/m_vendor/overlay/')
        print('Done!!!')
        print('')
        print('== == == == == == == == == == == == == == == ==')
        print('          WARNING! WARNING! WARNING!')
        print('   The patch was installed but wasnt applied')
        print('   To apply it after flashing rebot to twrp')
        print('   Mount system, vendor and data')
        print('   And enter the command :')
        print('   chcon u:object_r:vendor_overlay_file:s0 /system/system/vendor/overlay;chcon u:object_r:vendor_overlay_file:s0 /system/system/vendor/overlay/framework-res__auto_generated_rro.apk')
        print('   chcon u:object_r:vendor_overlay_file:s0 /vendor/overlay;chcon u:object_r:vendor_overlay_file:s0 /vendor/overlay/framework-res__auto_generated_rro.apk')
        print('== == == == == == == == == == == == == == == ==')
        print('')

def system_change(name) :
    print('Start working with system :')

    answer = choose_option('Add Magisk support (Android 11 only)', ['Yes', 'No'])
    if answer == 1 :
        print('Applying fix...')
        system('echo \"\nexport PATH /sbin:/product/bin:/apex/com.android.runtime/bin:/apex/com.android.art/bin:/system_ext/bin:/system/bin:/system/xbin:/odm/bin:/vendor/bin:/vendor/xbin\" >> ' + name + '_working/m_system/init.environ.rc')
        print('Done...')

    answer = choose_option('Try to fix ADB bug (Adnroid 10 mostly)', ['Yes', 'No'])
    if answer == 1 :
        print('Applying fix (Mau be cause of bootloop :-D)...')
        
        print('Getting verified keys...')
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/patch/adb_keys?inline=false -O ' + name + '_working/adb_keys')
        system('sudo mkdir -p ' + name + '_working/m_system/data/misc/adb')
        system('sudo cp ' + name + '_working/adb_keys ' + name + '_working/m_system/data/misc/adb/')
        
        print('Changib prop.default')
        prop_default_path = name + '_working/m_system/sustem/etc/prop.default'

        system('sudo echo \"ro.adb.secure=0\" >> ' + prop_default_path)
        system('sudo echo \"ro.secure=0\" >> ' + prop_default_path)
        system('sudo echo \"ro.debuggable=1\" >> ' + prop_default_path)
        system('sudo echo \"persist.sys.usb.config=mtp,adb\" >> ' + prop_default_path)
        system('sudo echo \"persist.service.adb.enable=1\" >> ' + prop_default_path)
        system('sudo echo \"persist.service.debuggable=1\" >> ' + prop_default_path)

        system('sudo sed -i \'s/ro.adb.secure=.*./ro.adb.secure=0/g\' ' + prop_default_path)
        system('sudo sed -i \'s/ro.secure=.*./ro.secure=0/g\' ' + prop_default_path)
        system('sudo sed -i \'s/ro.debuggable=.*./ro.debuggable=1/g\' ' + prop_default_path)
        system('sudo sed -i \'s/persist.sys.usb.config=.*./persist.sys.usb.config=mtp,adb/g\' ' + prop_default_path)
        system('sudo sed -i \'s/persist.service.adb.enable=.*./persist.service.adb.enable=1/g\' ' + prop_default_path)
        system('sudo sed -i \'s/persist.service.debuggable=.*./persist.service.debuggable=1/g\' ' + prop_default_path)
        system('sudo sed -i \'s/ro.adb.secure 1/ro.adb.secure 0/g\' ' + prop_default_path)
        system('sudo sed -i \'s/ro.secure 1/ro.secure 0/g\' ' + prop_default_path)
        system('sudo sed -i \'s/ro.debuggable 0/ro.debuggable 1/g\' ' + prop_default_path)
        system('sudo sed -i \'s/persist.service.adb.enable 0/persist.service.adb.enable 1/g\' ' + prop_default_path)
        system('sudo sed -i \'s/persist.service.debuggable 0/persist.service.debuggable 1/g\' ' + prop_default_path)

        print('Done!')
        print('')

    answer = choose_option('Fix play protect(doesn\'t work with adb fix)', ['Yes', 'No'])
    if answer == 1 :
        print('Working...')
        system('sudo mkdir -p ' + name + '_working/m_system/system/phh/')
        system('sudo touch ' + name + '_working/m_system/system/phh/secure')
        system('sudo chmod 644 ' + name + '_working/m_system/system/phh/secure')
        print('Done!')
        print('')

    answer = choose_option('Change name to Nokia 7.1', ['Yes', 'No'])
    if answer == 1 :
        print('Changing build.prop')
        build_prop_path = name + '_working/m_system/system/build.prop'

        system('sudo sed -i \'s/ro.system.build.fingerprint=.*./ro.system.build.fingerprint=Nokia\\/Crystal_00WW\\/CTL_sprout:10\\/QKQ1.190828.002\\/00WW_4_15I:user\\/release-keys/g\' ' + build_prop_path)
        system('sudo sed -i \'s/ro.product.system.brand=.*./ro.product.system.brand=Unknown/g\' ' + build_prop_path)
        system('sudo sed -i \'s/ro.product.system.manufacturer=.*./ro.product.system.manufacturer=Unknown/g\' ' + build_prop_path)
        system('sudo sed -i \'s/ro.product.system.model=.*./ro.product.system.model=Nokia 7.1/g\' ' + build_prop_path)
        system('sudo sed -i \'s/ro.product.system.name=.*./ro.product.system.name=B2N_00WW_FIH/g\' ' + build_prop_path)
        system('sudo sed -i \'s/ro.product.system.device=.*./ro.product.system.device=B2N/g\' ' + build_prop_path)
        
        print('Done!!!')
        print('')

    answer = choose_option('Include phh\'superuser app', ['Yes', 'No'])
    if answer == 1 :
        print('Getting apk')
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/app/me.phh.superuser_1033.apk -O ' + name + '_working/phh_superuser.apk')
        system('sudo cp ' + name + '_working/phh_superuser.apk ' + name + '_working/m_system/system/app/')
        system('sudo chmod 644 ' + name + '_working/m_system/system/app/phh_superuser.apk')
        
        print('Done!')
        print('')

    answer = choose_option('Include tales for power menu app', ['Yes', 'No'])
    if answer == 1 :
        print('Getting apk')
        system('wget https://gitlab.com/KonstantIMP/gsi_port_resource/-/raw/master/app/Device_Control.apk -O ' + name + '_working/device_control.apk')
        system('sudo cp ' + name + '_working/device_control.apk ' + name + '_working/m_system/system/app/')
        system('sudo chmod 644 ' + name + '_working/m_system/system/app/device_control.apk')
        
        print('Done!')
        print('')

    print('== == == == == == == == == == == == == == == ==')
    print('          WARNING! WARNING! WARNING!')
    print('   If you included some app to the rom you need to')
    print('   Reboot into twrp, mount system, vendor and data')
    print('   And enter the commands :')
    print('   find /system/app -exec chcon u:object_r:system_file:s0 {} \\;')
    print('   chcon u:object_r:system_file:s0 /system/app/*.apk')
    print('== == == == == == == == == == == == == == == ==')
    print('')

def umount_all(name) :
    print('Umount images...')
    system('sudo umount ' + name + '_working/m_system')
    system('sudo umount ' + name + '_working/m_vendor')
    print('Done!')
    print('')

def complete_vendor(name) :
    print('Packing and resizing vendor')
    system('sudo e2fsck -fy ' + name + '_working/vendor.img')
    system('sudo resize2fs ' + name + '_working/vendor.img')
    system('sudo cp ' + name + '_working/vendor.img ' + name + '/vendor.img')
    system('sudo chmod 777 ' + name + '/vendor.img')
    print('Done!')
    print('')

def complete_system(name) :
    print('Packing and resizing system')
    system('sudo e2fsck -fy ' + name + '_working/system.img.ext')
    system('sudo resize2fs ' + name + '_working/system.img.ext')
    system('sudo img2simg ' + name + '_working/system.img.ext ' + name + '/system.img')
    system('sudo chmod 777 ' + name + '/system.img')
    print('Done!')
    print('')

def complete_boot(name) :
    print('Adding boot to release')
    system('sudo cp ' + name + '_working/boot.img ' + name + '/boot.img')
    system('sudo chmod 777 ' + name + '/boot.img')
    print('Done!')
    print('')

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

if __name__ == '__main__' :
    print_hello()
    
    os_check()

    gsi_path = get_gsi_path()
    rom_name = get_rom_name()

    create_rom_dir(rom_name)

    get_system(gsi_path, rom_name)
    get_vendor(rom_name)
    get_boot(rom_name)

    mount_system(rom_name)
    mount_vendor(rom_name)

    vendor_change(rom_name)
    system_change(rom_name)

    umount_all(rom_name)

    complete_system(rom_name)
    complete_vendor(rom_name)
    complete_boot(rom_name)

    print_bye()
