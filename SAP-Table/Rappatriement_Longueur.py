#!/usr/bin/python

#Author: maxime.chardon, Stage EPITA SPE


import sys, os, time
from xlwt import Workbook
import requests


# Color Text
Normal = "\033[0;37m "
Red = "\033[31m "
Green = "\033[32m "

time_tmp = time.localtime(time.time())
year = str(time_tmp[0])
month = str(time_tmp[1])
day = str(time_tmp[2])
hour = str(time_tmp[3])
minute = str(time_tmp[4])
seconde = str(time_tmp[5])

Log = open('./' + year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + seconde + '.txt', "w")

# Scan all file in a directory => list of tuples, tuples type: (Name, file_path)
def Scan_directory(directory_path, name_separator, name_position, file_ext):

    files_list = os.listdir(directory_path)

    not_save = 0

    WB_notsave = Workbook()
    sheet1 = WB_notsave.add_sheet('Sheet 1')

    name_list = []
    for i in range(len(files_list)): #keep all .txt file
        l = len(files_list[i])
        if files_list[i][l - len(file_ext) : l] != file_ext:
            print(files_list[i] + ' is not the search file!')
            Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + files_list[i] + ' is not the search file!\n')

            # register file not load
            sheet1.write(not_save, 0, files_list[i])
            not_save += 1

            continue
        else:
            (name, path) = find_name(files_list[i], name_separator, name_position)
            if name != '':
                find = False
                for y in range(len(name_list)):
                    replace = False
                    if name == name_list[y][0]:
                        find = True
                        old_path = name_list[y][1]
                        if os.path.getsize(directory_path + '/' + path) > os.path.getsize(old_path):
                            name_list.pop(y)
                            name_list.append((name, directory_path + '/' + path))
                            print(path + ' replaced beacause heavier!')
                            Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + path + ' replaced because heavier!\n')
                            break
                        else:
                            print(path + ' not replaced beacause lighter!')
                            Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + path + ' not replaced because lighter!\n')
                            break
                if not find:
                    print(path + ' is loaded!')
                    Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + path + ' is loaded!\n')
                    name_list.append((name, directory_path + '/' + path))
            else:
                print(path + ' is not the search file')
                Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + path + ' is not the search file\n')

                # register file not load
                sheet1.write(not_save, 0, files_list[i])
                not_save += 1

                continue

    if not os.path.exists("./FinalResult"):
        os.makedirs("./FinalResult")
    WB_notsave.save("./FinalResult/File_Not_Load.xls")
    Log.write('\n-------------------------------------Scan END---------------------------------------\n\n')
    return name_list


# Find Name in the path => tuple(Name, file_path)
def find_name(file_path, name_separator, name_position):
    x = 1
    name = ""
    for c in file_path:
        if c == name_separator and x == name_position:
            return(name, file_path)
        elif c == name_separator:
            x += 1
            name = ""
        else:
            name += c
    return ('', file_path)


# Extract all fields an lengths of each file => list of tuples, tuples type: (Name, List of tuple type: (field, len))
def Fields_Len_Extraction(list_name, file_separator):
    file_field_list = []
    for n, p in list_name:
        print('Begin analyse on: ' + p)
        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'Begin analyse on: ' + p + '\n')
        list = __Fields_Len_Extraction(n, p, file_separator)
        file_field_list.append((n, list))
        print('End analyse on: ' + p)
        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'End analyse on: ' + p + '\n')
    Log.write('\n------------------------------------File Analyse END-------------------------------------\n\n')
    return file_field_list

# under function extract field and name of one file
def __Fields_Len_Extraction(name, path, separator):
    # Output
    fields_len = []

    # Open and read file
    file = open(path, encoding = 'utf-8')
    lines = file.readlines()

    field = ""
    for c in lines[0]:
        if c == separator:
            fields_len.append((field[len(name) + 1 : len(field)], 0))
            field = ""
        else:
            field += c
    fields_len.append((field[0 : len(field) - 1], 0))

    lines.pop(0)

    #Len for each field
    for line in lines:
        tmp = ''
        x = 0
        for c in line:
            if c == separator:
                l = len(tmp)
                if l > fields_len[x][1]:
                    li = list(fields_len[x])
                    li[1] = l
                    fields_len[x] = tuple(li)
                x += 1
                tmp = ''
            else:
                tmp += c
        l = len(tmp) - 1
        if l > fields_len[x][1]:
            li = list(fields_len[x])
            li[1] = l
            fields_len[x] = tuple(li)
    return fields_len


# GET requests for each table => html file
def GET_requests(list_name):
    for name, p in list_name:
        result = requests.get("https://www.stechno.net/sap-tables.html?id=" + name, verify = False)
        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'GET requet done on: ' + name + '\n')
        print('GET requet done on: ' + name)

        # Save in a HTML file
        if not os.path.exists("./GETresult"):
            os.makedirs("./GETresult")
        file = open("./GETresult/GET_result_" + name + '.html', "w")
        file.write(result.text)
        file.close()
    Log.write('\n------------------------------------GET END---------------------------------------\n\n')


#Scan HTML pages => List of tuples, tuple type: (Name, list of tuples: (field, len))
def Fields_Len_HTML_Extractions(list_name):
    GET_fields_list = []
    for name, p in list_name:
        file = open("./GETresult/GET_result_" + name + '.html', "r")
        lines = file.readlines()

        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'Begin analyse on HTML of: ' + name + '\n')
        print('GET requet done on: ' + name)

        if len(lines[309]) < 28:
            GET_fields_list.append((name, [('', 0)]))
        else:
            here = 322
            list = []
            while len(lines[here]) > 20:
                i, j = 22, 22
                tmp, l = '', ''
                while lines[here][i] != '<':
                    tmp += lines[here][i]
                    i += 1
                here += 5
                while lines[here][j] != '<':
                    l += lines[here][j]
                    j += 1
                list.append((tmp, int(l)))
                here += 6
            GET_fields_list.append((name, list))

        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'End analyse on HTML of: ' + name + '\n')
        print('End analyse on HTML of: ' + name)

        file.close()
    Log.write('\n------------------------------------HTML Analyse END--------------------------------------\n\n')
    return GET_fields_list


# Merge GET_list and File_list for preserve only max length => list of a tuple, tuple type:(name, list of tuples, tuples type: (field, len))
def MergeTwoList(file_fields_list, get_fields_list):
    final_list = []
    for i in range(len(file_fields_list)):
        name = file_fields_list[i][0]
        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'Begin merging on: ' + name + '\n')
        print('Begin merging on: ' + name)
        fields_file = file_fields_list[i][1]
        fields_get = get_fields_list[i][1]
        if fields_get[0][0] == '':
            tmp = []
            for field, l in fields_file:
                tmp.append((field, l, 'File'))
            final_list.append((name, tmp))
        else:
            list = []
            for field, length in fields_file:
                j = isField(field, fields_get)
                if j == -1:
                    list.append((field, length, 'File'))
                else:
                    lg = fields_get[j][1]
                    if lg > length:
                        list.append((field, lg, 'WebSite'))
                    else:
                        list.append((field, length, 'File'))
                    fields_get.pop(j)
            final_list.append((name, list))
        Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'End merging on: ' + name + '\n')
        print('End merging on: ' + name)
    Log.write('\n--------------------------------------Merging END----------------------------------------\n\n')
    return final_list


# Determine the position of a field if is in GET_fields_list if not return -1
def isField(field, fields_get):
    for y in range(len(fields_get)):
        if field == fields_get[y][0]:
            return y
    return -1


#Save all in excel, .xls file
def SaveAll(Final_list, Is_unicode, Default_len, extension):
    multiplicateur = 1
    if Is_unicode:
        multiplicateur = 2

    Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'Begin save\n')
    print('Begin save')

    wb = Workbook()
    sheet = wb.add_sheet('sheet 1')

    sheet.write(0, 0, 'Table_champ')
    sheet.write(0, 1, 'champ')
    sheet.write(0, 2, 'longueur')
    sheet.write(0, 3, 'Provenance')
    i = 1
    for name, field_list in Final_list:
        for field, length, where in field_list:
            field_name = name + '_' + field
            sheet.write(i, 0, field_name)
            sheet.write(i, 1, field)

            if length == 0:
                length = Default_len
                where = 'User'
            length *= multiplicateur

            sheet.write(i, 2, length)
            sheet.write(i, 3, where)

            i += 1

    if not os.path.exists("./FinalResult"):
        os.makedirs("./FinalResult")
    wb.save('./FinalResult/Reference_longueur_' + extension[1 : len(extension)] + '.xls')
    print('Table is save here: ./FinalResult/Reference_longueur_' + extension[1 : len(extension)] + '.xls')
    Log.write('[ ' + time.asctime(time.localtime(time.time())) + ' ] : ' + 'Table is save here: ./FinalResult/Reference_longueur_' + extension[1 : len(extension)] + '.xls')
    Log.write('\n-------------------------------------Save in xls END----------------------------------------')
