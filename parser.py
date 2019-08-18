'''
--------------------------------------------------
DBPP - Data Breach Python Parser
--------------------------------------------------
Written by: Taro
Version: 1.0

'''

import argparse
import sys

def getlang():
    print('[1] English version')
    print('[2] Magyar verzió')
    lang = input()
    if lang != '1' and lang != '2':
        sys.exit('Please choose the language! (1 - English; 2 - Hungarian)')
    return lang

def getargs_en():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--find',dest='find', help='Provide the search term, 2 formats are accepted: Either it starts with @, like @gmail.com, then the program gives all the results which end with @gmail.com, or just provide the start of the email / the whole email like this: example / example@example.com')
    parser.add_argument('-o', '--output', dest='output', help='Three values accepted: t, f, b meaning terminal, file and both. This option lets you choose how you want to see the output after the search is done. Default value is b = both')
    parser.add_argument('-p', '--path', dest='path', help='This argument lets you provide the input folder, you have to provide the root breach folder, which contains folders like: 0, 1, 2 etc. Default setting is the same folder that the python script is in. Example: C:/something1/databreach')
    parser.add_argument('-m', '--mode', dest='mode', help='This let you choose whether you want to search for a password or email. Accepted values are: p - for password, and e - for email.')
    args = parser.parse_args()

    if not args.find:
        parser.error('[-] You forgot to provide the search term, use -f or --find to do so, or use -h or --help for help.')

    if not args.mode:
        parser.error('[-] You forgot to provide a search mode! Aviable options are: "p" for password and "e" for email.')

    if args.mode != 'p' and args.mode != 'e':
        parser.error('[-] You gave the wrong search mode. Aviable options are: "p" for password and "e" for email.')

    if not args.output:
        args.output = 'b'
    else:
        if args.output not in ['t', 'f', 'b']:
            parser.error('[-] You gave a wrong value for the output. Accepted values are: t, f, b')

    if not args.path:
        args.path = './data'
    return args
    

def getargs_hu():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--find',dest='find', help='Add meg a keresendő dolgot! 2 féle formátum az elfogadott: Vagy @-al kezdődik amit beírsz, pl mint a @gmail.com, ekkor a program visszaad mindent, ami @gmail.com-al végződik, vagy csak add meg egy email elejét / az egész emailt pl. így: valami / valami@valami.hu')
    parser.add_argument('-o', '--output', dest='output', help='Három értéket fogadunk el bemenetként: t, f, b amiknek a jelentése: terminal (t), file (f) és mindkettő (b). Ezzel kiválasztod, hogyan szeretnéd kapni a kimenetet. Az alapértelmezett beállítás a b = mindkettő')
    parser.add_argument('-p', '--path', dest='path', help='Ezzel adhatod meg, hogy hol vannak az adat fájlok. A sikeres működéshez a gyökérkönyvtárat kell megadni, amikben ezek a mappák vannak: 0, 1, 2 stb. Az alapbeállítás, ha nem adsz meg semmit, az a könyvtár, amiben a python script is van. Példa: C:/valami1/databreach')
    parser.add_argument('-m', '--mode', dest='mode', help='Ezzel lehet kiválasztani, hogy a jelszavak vagy az emailek között keresel. Az elfogadott értékek: p - ha jelszavak között, és e - ha emailek között.')
    args = parser.parse_args()

    if not args.find:
        sys.exit('[-] Elfelejtetted megadni, hogy mit keresel! Használd a -f vagy --find -ot, vagy kérj segítséget -h -val vagy --help -val.')

    if not args.mode:
        parser.error('[-] Nem adtál meg keresési módot! használd a -m-et, és adj p vagy e értéket neki.')

    if args.mode != 'p' and args.mode != 'e':
        parser.error('[-] Rossz keresési módot adtál meg. A két elfogadott érték: "p" és "e"')
        
    if not args.output:
        args.output = 'b'
    else:
        if args.output not in ['t', 'f', 'b']:
            sys.exit('[-] Rossz értéket adtál meg outputnak. Az elfogadott értékek: t, f, b')

    if not args.path:
        args.path = './data'
    return args


def kiir_terminal(mit):
    print(mit)


def kiir_file(mit):
    with open('passes.txt', 'a') as kifile_pass:
        if mit.find(':') != -1:
            mit_pass = mit.split(':')
        else:
            if mit.find(';') != -1:
                mit_pass = mit.split(';')
        if len(mit_pass) > 2:
            passwd = ''
            for i in (range(len(mit_pass)-1)):
                passwd += mit_pass[i + 1]
        else:
            passwd = mit_pass[1]
        try:
            print(passwd, file=kifile_pass)
        except UnicodeEncodeError:
            print(mit.encode('utf-8', 'ignore'), file=kifile_pass)


    with open('emails.txt', 'a') as kifile_email:
        if mit.find(':') != -1:
            mit_email = mit.split(':')[0]
        else:
            if mit.find(';') != -1:
                mit_email = mit.split(';')[0]
        try:
            print(mit_email, file=kifile_email)
        except UnicodeEncodeError:
            print(mit.encode('utf-8', 'ignore'), file=kifile_email)


    with open('emails_and_passes.txt', 'a') as kifile_all:
        try:
            print(mit, file=kifile_all)
        except UnicodeEncodeError:
            print(mit.encode('utf-8', 'ignore'), file=kifile_all)

def kiir(mit, hogyan):
    if hogyan == 't':
        kiir_terminal(mit)
    elif hogyan == 'f':
        kiir_file(mit)
    elif hogyan == 'b':
        kiir_terminal(mit)
        kiir_file(mit)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

lang = getlang()
alphnum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

if lang == '1':
    args = getargs_en()

elif lang == '2':
    args = getargs_hu()


if args.mode == 'e':    # if we are searching for an email
    if args.find[0] == '@': # if we looking for an email and we start with @
        alphnum.append('symbols')
        for mappa in alphnum:
            for fajl in alphnum:
                if mappa == 'symbols':
                    openstring = args.path + '/' + mappa
                else:
                    openstring = args.path + '/' + mappa + '/' + fajl
                try:
                    with open(openstring, 'rb') as befile:
                        for sor in befile:
                            sor = sor.decode('utf-8', 'ignore').strip()
                            if sor.find(args.find) != -1:
                                kiir(sor, args.output)
                except PermissionError:
                    for alfajl in alphnum:
                        openstring = args.path + '/' + mappa + '/' + fajl + '/' + alfajl
                        try:
                            with open(openstring, 'rb') as befile:
                                for sor in befile:
                                    sor = sor.decode('utf-8', 'ignore').strip()
                                    if sor.find(args.find) != -1:
                                        kiir(sor, args.output)
                        except PermissionError:
                            continue
                if mappa == 'symbols':
                    break

# if we looking for an email, but we dont start with an @
    else:
        if args.find[0].lower() in alphnum: # if the thing we are looking for doesnt start with a symbol
            if args.find[1].lower() not in alphnum:
                vege = 'symbols'
            else:
                vege = args.find[1]

            try:
                with open(args.path + '/' + args.find[0] + '/' + vege, 'rb') as befile:
                    for sor in befile:
                        sor = sor.decode('utf-8', 'ignore')
                        sor = sor.strip()
                        if sor.find(':') == -1:
                            sor_keres = sor.split(':')[0]
                        else:
                            if sor.find(';') == -1:
                                sor_keres = sor.split(';')[0]
                            else:
                                sor_keres = sor
                        if sor_keres.find(args.find) != -1:
                            kiir(sor, args.output)
            except PermissionError:
                if args.find[0].lower() in alphnum: # if the thing we are looking for doesnt start with a symbol
                    if args.find[2].lower() not in alphnum:
                        vege = args.find[1] + '/' + 'symbols'
                    else:
                        vege = args.find[1] + '/' + args.find[2]

                with open(args.path + '/' + args.find[0] + '/' + vege, 'rb') as befile:
                    for sor in befile:
                        sor = sor.decode('utf-8', 'ignore')
                        sor = sor.strip()
                        if sor.find(':') == -1:
                            sor_keres = sor.split(':')[0]
                        else:
                            if sor.find(';') == -1:
                                sor_keres = sor.split(';')[0]
                            else:
                                sor_keres = sor
                        if sor_keres.find(args.find) != -1:
                            kiir(sor, args.output)
        
        else:
            # if the thing we are looking for starts with a symbol
            with open(args.path + '/' + 'symbols', 'rb') as befile:
                for sor in befile:
                    sor = sor.decode('utf-8').strip()
                    if sor.find(args.find) != -1:
                        kiir(sor, args.output)


elif args.mode == 'p': # if we are searching for a password

    for mappa in alphnum:
            for fajl in alphnum:
                if mappa == 'symbols':
                    openstring = args.path + '/' + mappa
                else:
                    openstring = args.path + '/' + mappa + '/' + fajl
                try:
                    with open(openstring, 'rb') as befile:
                        for sor in befile:
                            sor_atal = sor.decode('utf-8', 'ignore').strip()
                            if sor_atal.find(':') == -1:
                                sor_l = sor_atal.split(':')
                            else:
                                if sor_atal.find(';') == -1:
                                    sor_l = sor_atal.split(';')
                                else:
                                    sor_l = sor_atal
                            if len(sor_l) > 2:
                                passwd = ''
                                for i in (range(len(sor_l)-1)):
                                    passwd += sor_l[i + 1]
                            else:
                                if len(sor_l) > 1:
                                    passwd = sor_l[1]
                                else:
                                    passwd = sor_l
                            if passwd == args.find:
                                kiir(sor_atal, args.output)
                            elif sor_atal.find(args.find) != -1:
                                kiir(sor_atal, args.output)
                except PermissionError:
                    for alfajl in alphnum:
                        openstring = args.path + '/' + mappa + '/' + fajl + '/' + alfajl
                        try:
                            with open(openstring, 'rb') as befile:
                                for sor in befile:
                                    sor_atal = sor.decode('utf-8', 'ignore').strip()
                                    if sor_atal.find(':') == -1:
                                        sor_l = sor_atal.split(':')
                                    else:
                                        if sor_atal.find(';') == -1:
                                            sor_l = sor_atal.split(';')
                                        else:
                                            sor_l = sor_atal
                                    if len(sor_l) > 2:
                                        passwd = ''
                                        for i in (range(len(sor_l)-1)):
                                            passwd += sor_l[i + 1]
                                    else:
                                        if len(sor_l) > 1:
                                            passwd = sor_l[1]
                                        else:
                                            passwd = sor_l
                                    if passwd == args.find:
                                        kiir(sor_atal, args.output)
                                    elif sor_atal.find(args.find) != -1:
                                        kiir(sor_atal, args.output)
                        except PermissionError:
                            continue
                if mappa == 'symbols':
                    break


