'''
    @ file  :   code_fmt.py
    @ brief :   script for my dear friend to formart his C code files
    @ auther:   JRL
    @ date  :   2016.07.05
    @ note  :   Python 3.5.1, or higher edition
'''

import os, sys, glob
import shutil

fileList = []

# define the suffix type of the target files
suffixList = ['h', 'hpp', 'c', 'cpp', 'cc']


# # get the path of your work derectory
# def cur_dir():
#     path = sys.path[0]

#     if os.path.isdir(path):
#         return path
#     elif os.path.isfile(path):
#         return os.path.dirname(path)


# # traversal all the files in current path
# def file_walk(dir, topdown = True):
#     for root, dirs, files in os.walk(dir, topdown):
#         for name in files:
#             fileList.append(name)


# # traversal the current folder
# file_walk(cur_dir())


# traversal all the files in current path
for suffix in suffixList:
    files = glob.glob('*.' + suffix)
    for each in files:
        fileList.append(each)


# delete all the files in specific folder
def delete_files_in_folder(src):
    if os.path.isfile(src):
        os.remove(src)
    elif os.path.isdir(src):
        for file in os.listdir(src):
            file_src = os.path.join(src, file)
            delete_files_in_folder(file_src)


# copy and backup files
def backup_file(dir):
    for i in fileList:
        shutil.copy(i,dir)


# make a directory and backup all the files
def mkdir_and_bcp(dir):
    isExists = os.path.exists(dir)

    if not isExists:
        os.makedirs(dir)
        backup_file(dir)
    else:
        delete_files_in_folder(dir)
        backup_file(dir)


# back the files in your work folder
back_folder_name = 'sources_backup'
mkdir_and_bcp(back_folder_name)

print('\n Your code files are backuped in\n --> [./' + back_folder_name
    + '] <-- folder \n in your work derectory, check for necessory\n')

# change the working derectory into the backup folder
os.chdir(back_folder_name)

print(' Formarting your code ...\n')


''' ---------------------------------------------
    up to now, we finally backup all the exist
    source files into the backup folder

    and now, it's time to formart your code,
    let's do it
 ---------------------------------------------'''


slash_symbol = '//'

# return the index of '//' in one line
# return -1     : '//' is not in the line
#        0 ~ n  : index of the '//'
def index_of_slash_symbol(str2fmt):
    return str2fmt.find(slash_symbol)

# formart TAB into four spaces
def fmt_tab2spaces(str2fmt):
    return str2fmt.replace('\t', 4 * ' ')


# insert some spaces before '//' symbol for alignment
def spaces_insert(str2fmt, index, num):
    return str2fmt[:index] + num * ' ' + str2fmt[index:]


for each in fileList:
    file = open(each)
    w_file = open('../' + 'test','wt')

    stack = []
    new_style = []
    new_tmp = []

    index_max = 0

    while True:
        line = file.readline()

        if not line:
            break

        new_line = fmt_tab2spaces(line)

        if '{' in new_line:
            stack.append('{')

            if '}' in new_line:
                stack.pop()

                if stack:
                    index = index_of_slash_symbol(new_line)

                    if(index >= index_max):
                        index_max = index

                    new_tmp.append(new_line)

                    continue
                else:
                    # deal new_tmp list
                    for ii in new_tmp:
                        cur_index = index_of_slash_symbol(new_line)
                        if(cur_index <= 4):
                            new_style.append(ii)
                        else:
                            new_style.append(spaces_insert(ii, cur_index, 5 + index_max - cur_index))

                    index_max = 0
                    continue
            else:
                new_tmp.append(new_line)
                continue
        else:
            new_style.append(new_line)
            continue





        # index = index_of_slash_symbol(new_line)

        # if(index >= index_max):
        #     index_max = index

        # if(4 < index):
        #     new_style.append(spaces_insert(new_line, index, 10))
        #     continue


    print(index_max)

    for i in new_style:
        # print(i)
        w_file.write(i)

    file.close
    w_file.close


