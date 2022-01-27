import os, shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename

if os.path.exists('config'):
    with open('config', 'r') as inf:
        dir_file = inf.readlines()
else:
    Tk().withdraw()
    dir = askdirectory()
    file = askopenfilename()
    dir_file = [dir, file]
    with open('config', 'w+') as ouf:
        ouf.write(dir + '\n' + file)

path_of_file_on_server = dir_file[0][:-1] + '/' + dir_file[1].split('/')[-1]
print(path_of_file_on_server)
if os.path.exists(path_of_file_on_server):
    time_of_change_file_on_server = os.stat(path_of_file_on_server).st_mtime
    time_of_change_file_on_local = os.stat(dir_file[1]).st_mtime
    print('time of change server: ', time_of_change_file_on_server)
    print('time of change local: ', time_of_change_file_on_local)
    server_need_update = [True if time_of_change_file_on_local > time_of_change_file_on_server
                          and time_of_change_file_on_local + 1 > time_of_change_file_on_server
                          and time_of_change_file_on_local - 1 > time_of_change_file_on_server
                          else False]
    locale_need_update = [True if time_of_change_file_on_server > time_of_change_file_on_local
                          and time_of_change_file_on_server + 1 > time_of_change_file_on_local
                          and time_of_change_file_on_server - 1 > time_of_change_file_on_local
                          else False]
    print('server need update:', server_need_update)
    print('local need update: ', locale_need_update)
    if server_need_update:
        os.remove(path_of_file_on_server)
        shutil.copy(dir_file[1], path_of_file_on_server)
    if locale_need_update:
        os.remove(dir_file[1])
        shutil.copy(path_of_file_on_server, dir_file[1])
else:
    shutil.copy(dir_file[1], path_of_file_on_server)


