# 用户类定义
import time


class Users:
    accounts = []  # 用户名序列
    passwords = []  # 密码序列

    def register(self):   # 注册
        print("注册账号.....")
        acnt = input("用户名：")
        pwd1 = input("密码：")
        pwd2 = input("再次输入密码：")

        if pwd1 != pwd2:   # 判断两次输入的密码是否一致
            print("两次输入的密码不一致！")
            return

        if self.accounts.count(acnt):  # 判断用户名是否已经存在
            print("用户名已存在！")
            return

        # 注册成功
        print("注册成功！")
        self.accounts.append(acnt)
        self.passwords.append(pwd1)

    def login(self):   # 登录，有返回值，True时登录成功
        print("登录到文件系统....")
        acnt = input("用户名：")
        pwd1 = input("密码：")

        if not self.accounts.count(acnt):  # 查找用户名是否存在
            print("用户名或密码错误！")
            return False

        pwd2 = self.passwords[self.accounts.index(acnt)]
        if pwd1 != pwd2:   # 密码错误
            print("用户名或密码错误！")
            return False

        print("登录成功！")
        return acnt

    def show_all_users(self):   # 显示所有用户
        length = len(self.accounts)
        if length == 0:
            print("无用户！")
            return

        for i in range(length):
            print(self.accounts[i], end=" ")
        print("")

    def delete_user(self):   # 删除用户
        acnt = input("用户名：")
        pwd1 = input("密码：")

        if not self.accounts.count(acnt):  # 查找用户名是否存在
            print("用户名或密码错误！")
            return

        pwd2 = self.passwords[self.accounts.index(acnt)]
        if pwd1 != pwd2:   # 密码错误
            print("用户名或密码错误！")
            return

        # 删除账号的下标p
        p = self.accounts.index(acnt)
        self.accounts.pop(p)
        self.passwords.pop(p)

        print("删除成功！")

