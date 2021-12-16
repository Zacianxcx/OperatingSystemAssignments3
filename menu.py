import os
import re


# 路径解析
# 路径字符串，当前工作目录，家目录home，用户名
import sys


def path_resolve(path, cur_directory, home, user):
    absolute = False
    # 绝对路径
    if path[0] == '/':
        absolute = True
        d = home
    # 相对路径
    else:
        absolute = False
        d = cur_directory

    # 处理前后的'/'
    if path[0] == '/':
        path = path[1:]
    if path[-1] == '/':
        path = path[:-1]

    path = path.split('/')
    # 是绝对路径，去掉第一个home
    if absolute:
        path = path[1:]

    for i in path:
        if i == "..":
            if d.pre_directory is None:
                return 0
            else:
                d = d.pre_directory
        elif i == ".":
            continue
        else:
            if d == home and i != user:
                return -1
            d = d.find_directory(i)
            # 文件夹不存在，返回
            if not d:
                return 0
    return d


def user_menu(users):
    while True:
        print("*" * 10 + "文件管理系统" + "*" * 10)
        print("*" * 10 + "FileSystem" + "*" * 10)
        print("1:注册" + ' ' * 5 + "2:登录" + ' ' * 5 + "3:显示所有用户")
        print("4:删除用户" + ' ' * 5 + "5:退出")
        choice = int(input("请输入选择："))
        if choice == 1:
            users.register()
        elif choice == 2:
            login_user_name = users.login()
            if login_user_name:
                return login_user_name
        elif choice == 3:
            users.show_all_users()
        elif choice == 4:
            users.delete_user()
        elif choice == 5:
            sys.exit(0)
        else:
            print("输入有误！")


def terminal(user_home, disk):
    cur_directory = user_home
    cur_path = cur_directory.path
    user = user_home.directory_name
    while True:
        command_str = input(user + "@FileSystem:" + cur_path + "$ ")
        # 格式化指令（将多个的空转化为一个，方便分割）
        command_str = re.sub(' +', ' ', command_str)

        command = command_str.split(" ")    # 分割指令

        if command[0] == "ls":    # ls命令：显示工作目录下的内容
            cur_directory.list_file()

        elif command[0] == "mkdir":  # mkdir命令：工作目录下创建文件夹
            dire_list = command[1:]
            for i in dire_list:
                cur_directory.make_directory(i)

        elif command[0] == "mkfile":  # mkfile：工作目录下创建文件
            file_list = command[1:]
            for i in file_list:
                cur_directory.make_file(i, disk)

        elif command[0] == "rm":   # rm：删除文件或目录
            if len(command) == 3 and command[2] == "-r":  # 有-r：删除目录
                cur_directory.remove_directory(command[1])
            else:   # 无-r：删除文件
                cur_directory.remove_file(command[1], disk)

        elif command[0] == "cd":  # cd：更改工作目录

            if len(command) > 2:
                print("路径格式错误")
            else:   # des：目标目录

                des = path_resolve(command[1], cur_directory, user_home.pre_directory, user)
                if des == 0:
                    print("路径不存在！")
                elif des == -1:
                    print("不可进入其他用户文件夹！")
                else:
                    cur_directory = des
            cur_path = cur_directory.path
            # if command[1] == "..":   # ..: 返回上级目录
            #     if cur_directory.pre_directory is None:
            #         print("目录不存在！")
            #     else:
            #         cur_directory = cur_directory.pre_directory
            #         cur_path = cur_directory.path
            # else:
            #     des = cur_directory.find_directory(command[1])   # des：目标目录
            #     if not des:
            #         des = cur_directory.find_file(command[1])
            #         if not des:
            #             print("目录不存在！")
            #         else:
            #             print(command[1] + ":不是一个目录！")
            #     else:
            #         cur_directory = des
            #         cur_path = cur_directory.path

        # fread: 读文件
        # 2个参数
        # 文件名
        # 读指针位置：无参数，起始；<1：报错
        elif command[0] == "fread":
            # 先查找文件是否存在
            des = cur_directory.find_file(command[1])
            if not des:
                print("文件不存在！")
            else:
                if len(command) == 2:
                    pointer = 1
                else:
                    pointer = int(command[2])
                des.read_file(pointer, disk)

        # fwrite：写文件
        # 两个参数
        # 文件名
        # 写指针位置：无参数：末尾；<1：报错
        elif command[0] == "fwrite":
            # 先查找文件是否存在：
            des = cur_directory.find_file(command[1])
            if not des:
                print("文件不存在！")
            else:
                # 处理文件指针
                if len(command) == 2:
                    pointer = des.length
                    if des.length == 0:
                        pointer += 1
                else:
                    pointer = int(command[2])
                des.write_file(pointer, disk)

        elif command[0] == "sbm":   # 展示位图
            disk.show_bitmap()

        elif command[0] == "sd":    # 展示磁盘
            disk.show_disk()

        elif command[0] == "shutdown":  # 关闭，退出系统
            os.system('cls')
            return

        else:
            print("无法解析的指令！")

