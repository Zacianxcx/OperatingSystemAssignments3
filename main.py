from User_definition import *
from File_definition import *
from menu import *

users = Users()
disk = Disk()
home = Directory(None, "home")
while True:
    user_name = user_menu(users)
    user_home = home.find_directory(user_name)  # 寻找用户文件夹是否存在
    if not user_home:  # 不存在则创建一个
        user_home = home.make_directory(user_name)
    print("正在初始化文件系统......请稍后........")
    time.sleep(2)
    os.system('cls')
    terminal(user_home, disk)
