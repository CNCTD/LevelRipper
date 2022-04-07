#if it does not work because of this, open cmd and run the following command:
#python -m pip install xml zlib base64
#then run this script again


import xml.etree.ElementTree as ET
import xml
import base64, zlib, os, sys


def print_menu() -> None:
    os.system('cls')
    print(f'Welcome to LocalLevels Extractor, make sure your save file is fixed\n'
          '\n'
          'Decryption code downloaded from https://pastebin.com/JakxXUVG by Absolute Gamer\n'
          '\n'
          'Menu Shamelessly Copied from WEGFan\n'
          '\n'
          '1. Convert save to XML\n'
          '2. Dump level names\n'
          '3. Dump level to GMD\n'
          '4. Dump all levels to GMD (Dangerous)\n')


def xor_bytes(data: bytes, value: int) -> bytes:
    return bytes(map(lambda x: x ^ value, data))

def to_xml(savefile: str = 'CCLocalLevels.dat') -> None:
    with open(savefile, 'rb') as f:
        encrypted_data = f.read()

        decrypted_data = xor_bytes(encrypted_data, 11)
        decoded_data = base64.b64decode(decrypted_data, altchars=b'-_')
        decompressed_data = zlib.decompress(decoded_data[10:], -zlib.MAX_WBITS)
        with open(f'{savefile}.xml', 'wb') as f:
                        f.write(decompressed_data)
        return decompressed_data

def dump_level_names(xmlfile: str = 'CCLocalLevels.dat.xml') -> None:
    parser = ET.XMLParser(encoding="utf-8")
    with open(xmlfile, 'r') as f:
        xmlstring = f.read()
    tree = ET.fromstring(xmlstring, parser=parser)


    levels = []
    items = list(tree.iter())
    for i, item in enumerate(items):
        if item.text == "k2":
            next_item = items[i + 1]
            #print(next_item.text)
            levels.append(next_item.text)
    with open('levels.txt', 'w') as f:
        for level in levels:
            f.write(level + '\n')
    print(f'{len(levels)} levels found!')
    print('Saved to levels.txt')

def dump_level_gmd(name, xmlfile: str = 'CCLocalLevels.dat.xml') -> None:
    with open('default.gmd', 'r') as f:
            default_data = f.read()
    parser = ET.XMLParser(encoding="utf-8")
    with open(xmlfile, 'r') as f:
        xmlstring = f.read()
    tree = ET.fromstring(xmlstring, parser=parser)
    #find name in tree
    level_data = []
    song_data = []
    items = list(tree.iter())
    for i, item in enumerate(items):
        if item.text == name:
            next_item = items[i + 2]
            song = items[i + 18].text
            level_data.append(next_item.text)
            song_data.append(song)
    if len(level_data) > 1:
        print('There are more than one level with this name, all will be dumped.')
    num = 0
    for i in level_data:
        final_data = default_data.replace('LEVEL_NAME', f'{name}')
        final_data = final_data.replace('LEVEL_DATA', i)
        final_data = final_data.replace('SONG_ID', song_data[num])
        with open(f'{name}_{num}.gmd', 'w') as f:
            f.write(final_data)
        num += 1
    print(f'{num} levels dumped!')

def main():
    print_menu()
    while True:
        print()
        s = input('>>> ')
        print()

        try:
            index = int(s)
        except ValueError as err:
            sys.exit()
        if index == 1:
            
            to_xml()
            input('Save file has been converted to an xml file, press enter to exit.')
            
        elif index == 2:
            dump_level_names()
            input('Level names have been dumped, press enter to exit.')
            
        elif index == 3:
            name = input('Enter level name: ')
            dump_level_gmd(name)
            input('Level has been dumped, press enter to exit.')
            
        elif index == 4:
            #read levels.txt
            
            with open('levels.txt', 'r') as f:
                levels = f.read().splitlines()
            for i in levels:
                dump_level_gmd(i)
            input('All levels have been dumped, press enter to exit.')
            
        else:
            print('Invalid input, try again.')
            continue

if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt) as err:
        sys.exit()






