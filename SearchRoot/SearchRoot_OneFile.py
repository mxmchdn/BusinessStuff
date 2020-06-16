from tkinter import filedialog
from tkinter import *
from xlwt import Workbook

root = Tk()
Item_Path = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))

def id_out(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    lines.pop(0)
    ID = []
    for line in lines:
        tmp, occ = '', 0
        id = ''
        for c in line:
            if c == ',':
                if occ == 0:
                    id = tmp
                elif occ == 4:
                    print(tmp)
                    if tmp == 'TB':
                        ID.append(id)
                tmp = ''
                occ += 1
            else:
                tmp += c
    return ID


def item_out(path):
    file = open(path, "r", encoding = 'utf-8')
    lines = file.readlines()
    file.close()
    lines.pop(0)
    list = []
    for elt in lines:
        id = ""
        name = ""
        parent_id = ""
        item_type = ""
        file_size = ""
        count = 0
        tmp = ""
        for c in elt:
            if c == ',':
                if count == 0:
                    if tmp == '""':
                        tmp = ''
                    id = tmp
                elif count == 1:
                    if tmp == '""':
                        tmp = ''
                    name = tmp
                elif count == 3:
                    if tmp == '""':
                        tmp = ''
                    parent_id = tmp
                elif count == 4:
                    if tmp == '""':
                        tmp = ''
                    item_type = tmp
                count += 1
                tmp = ""
            elif c == '\n':
                if tmp == '""':
                    tmp = ''
                file_size = tmp
            else:
                tmp += c
        if file_size == '':
            file_size = tmp
        list.append((id, name, parent_id, item_type, file_size))
    return list


def rise_up(ID_list, Item_list, filename):
    wb = Workbook()
    sheet = wb.add_sheet('sheet 1')

    sheet.write(0, 0, "id")
    i = 1
    max = 0
    for id in ID_list:
        sheet.write(i, 0, id)

        tuple = Search_Parent(id, Item_list)

        id = tuple[0]
        name = tuple[1]
        parent = tuple[2]
        filetype = tuple[3]
        filesize = tuple[4]

        if max == 0:
            sheet.write(0, 1, "id_1")
            sheet.write(0, 2, "name_1")
            sheet.write(0, 3, "file_type_1")
            sheet.write(0, 4, "file_size_1")
            max = 1

        if parent == 'NOT':
            sheet.write(i, 1, "NOT_FOUND")
            sheet.write(i, 2, "NOT_FOUND")
            sheet.write(i, 3, "NOT_FOUND")
            sheet.write(i, 4, "NOT_FOUND")
            i += 1
            continue
        else:
            sheet.write(i, 1, id)
            sheet.write(i, 2, name)
            sheet.write(i, 3, filetype)
            sheet.write(i, 4, filesize)

        c = 1
        j = 5
        while parent != '' and parent != 'NOT':
            c += 1
            tuple = Search_Parent(parent, Item_list)

            id = tuple[0]
            name = tuple[1]
            parent = tuple[2]
            filetype = tuple[3]
            filesize = tuple[4]

            if c > max:
                sheet.write(0, j, "id_" + str(c))
                sheet.write(0, j + 1, "name_" + str(c))
                sheet.write(0, j + 2, "file_type_" + str(c))
                sheet.write(0, j + 3, "file_size_" + str(c))
                max = c

            if c == 2 and filetype == 'RS':
                c = 1
                continue

            if parent == 'NOT':
                sheet.write(i, j, "NOT_FOUND")
                j += 1
                sheet.write(i, j, "NOT_FOUND")
                j += 1
                sheet.write(i, j, "NOT_FOUND")
                j += 1
                sheet.write(i, j, "NOT_FOUND")
                j += 1
            else:
                sheet.write(i, j, id)
                j += 1
                sheet.write(i, j, name)
                j += 1
                sheet.write(i, j, filetype)
                j += 1
                if filesize == '':
                    filesize = '0'
                sheet.write(i, j, filesize)
                j += 1

            if c > 50:
                break
        i += 1
    wb.save("./Arborescence_" + filename + ".xls")


def Search_Parent(id, list):
    for tuple in list:
        if tuple[0] == id:
            return tuple
    return ('', '', 'NOT', '', '')


name = 'OutPut'
list1 = id_out(Item_Path)
list2 = item_out(Item_Path)
rise_up(list1, list2, name)
