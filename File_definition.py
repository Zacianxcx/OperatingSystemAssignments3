class Disk:
    def __init__(self):
        self.row = 16   # 行数
        self.col = 16   # 列数
        self.block = 8  # 每个块大小
        self.capacity = self.row * self.col * self.block
        self.bitmap = [[0 for i in range(self.col)] for j in range(self.row)]  # 位图
        self.disk_content = [["" for i in range(self.col)] for j in range(self.row)]  # 模拟磁盘
        self.next = 0   # 准备写入哪个磁盘块

    def show_bitmap(self):  # 打印位图
        print("   ", end="")
        for i in range(self.col):
            print('%-3s' % '{}'.format(i), end="")
        print("")
        for i in range(self.row):
            print('%-3s' % '{}'.format(i), end="")
            for j in range(self.col):
                print('%-3s' % '{}'.format(self.bitmap[i][j]), end="")
            print("")

    def show_disk(self):  # 打印磁盘
        for i in range(self.row):
            print(i, end=" ")
            for j in range(self.col):
                print(self.disk_content[i][j], end=" ")
            print("")

    def find_next(self):  # 找到下一个可用块
        for i in range(self.row):
            for j in range(self.col):
                if self.bitmap[i][j] == 0:
                    self.next = i * self.col + j
                    return


class File:
    def __init__(self, father, file_name, disk):
        self.directory = father   # 该文件所在目录
        self.file_name = file_name   # 该文件的名字
        self.length = 0   # 该文件长度
        self.index_num = disk.next   # 索引位于哪个磁盘块
        # 索引所在磁盘的行号和列号
        self.index_r = self.index_num // disk.col
        self.index_c = self.index_num % disk.col
        # 更新磁盘
        # 计算索引所在的磁盘块行号和列号
        disk.disk_content[self.index_r][self.index_c] = [-1 for i in range(disk.block)]  # 更新磁盘
        disk.bitmap[self.index_r][self.index_c] = 1  # 更新位图
        # 找到下一个可用的块
        disk.find_next()
        disk.capacity -= 1  # 更新容量

    def read_file(self, p, disk):  # 读文件，参数：文件指针
        # 先处理文件指针参数
        p -= 1  # 对应到字符串下标
        if p < 0:
            print("文件指针设置有误！")
            return
        index = disk.disk_content[self.index_r][self.index_c]
        content = ""
        for i in index:
            if i == -1:
                break
            else:
                r = i // disk.col
                c = i % disk.col
                content += disk.disk_content[r][c]
        print(content[p:])

    def write_file(self, p, disk):  # 写文件，参数：文件指针；磁盘
        p -= 1  # 对应到字符串下标
        if p < 0:
            print("文件指针设置有误！")
            return
        write_content = input("")
        # 文件最多64个字符
        if len(write_content) + self.length > 64:
            print("写入失败！")
            return

        disk.capacity -= len(write_content)  # 更新磁盘容量

        # 先将文件从内存中提取
        s = ""
        index = disk.disk_content[self.index_r][self.index_c]  # 先找到索引
        # 提取文件
        for i in index:
            if i == -1:
                break
            else:
                r = i // disk.col
                c = i % disk.col
                s += disk.disk_content[r][c]

        content_list = list(s)
        content_list.insert(p, write_content)
        s = ''.join(content_list)
        self.length = len(s)   # 更新文件长度

        # 将磁盘装入文件的位置清空
        for i in index:
            if i == -1:
                break
            else:
                r = i // disk.col
                c = i % disk.col
                disk.disk_content[r][c] = ""
                disk.bitmap[r][c] = 0
        # 写入磁盘
        p = 0      # 指向字符串的指针
        i = 0      # 指向index的指针
        while True:
            if index[i] != -1:
                r = index[i] // disk.col
                c = index[i] % disk.row
                disk.bitmap[r][c] = 1
                disk.find_next()
                disk.disk_content[r][c] = s[p:p+8]
                p += 8
                i += 1
            if p > len(s):
                break
            else:
                index[i] = disk.next
        print("文件写入成功！")


class Directory:
    def __init__(self, father, directory_name):
        self.pre_directory = father   # 上一个目录：对象
        self.directory_name = directory_name   # 该目录的名字
        self.directory = []   # 该目录里的其他目录，directory列表
        self.file = []   # 该目录里的文件，file列表
        if self.pre_directory is None:
            self.path = "/" + self.directory_name
        else:
            self.path = self.pre_directory.path + "/" + self.directory_name

    def list_file(self):   # ls命令：展示所有目录和文件
        length1 = len(self.directory)
        length2 = len(self.file)
        if length1 + length2 > 0:  # 存在目录或文件
            for i in range(length1):
                print('\033[34m{}\033[0m'.format(self.directory[i].directory_name), end=" ")
            for i in range(length2):
                print(self.file[i].file_name, end=" ")
            print("")

    def make_directory(self, dire):   # mkdir命令：创建目录  目录名称
        flag = True
        if dire.count("/"):   # 文件夹名称不能含有'/'
            print("不能创建目录" + dire + ": 目录名称不能含有'/'")
            flag = False
        if flag:   # 文件夹不能重名
            for i in self.directory:
                if i.directory_name == dire:
                    print("不能创建文件夹" + dire + ": 文件夹已存在")
                    flag = False
        if flag:
            new = Directory(self, dire)
            self.directory.append(new)
            print("文件夹" + dire + "创建成功！")
            return new

    def make_file(self, fl, disk):  # mkfile命令：创建文件： 文件名称
        if disk.capacity == 0:
            print("磁盘容量已满！")
            return
        if fl.count("/"):   # 文件名称不能含有'/'
            print("不能创建文件" + fl + ": 文件名称不能含有'/'")
            return
        # 文件不能重名
        for i in self.file:
            if i.file_name == fl:
                print("不能创建文件" + fl + ": 文件已存在")
                return

        self.file.append(File(self, fl, disk))
        print("文件" + fl + "创建成功！")

    def remove_directory(self, dire):  # rm XXX -r命令：删除文件夹：文件夹名称
        length = len(self.directory)
        for i in range(length):  # 寻找该文件夹
            if self.directory[i].directory_name == dire:
                t = self.directory.pop(i)
                # 删除文件夹中的所有文件
                for j in range(len(t.file)):
                    t.remove_file(t.file[j].file_name)
                # 删除文件夹里的文件夹
                for j in range(len(t.directory)):
                    t.remove_directory(t.directory[j].name)
                return
        print("不能删除目录" + dire + ": 文件夹不存在")

    def remove_file(self, fl, disk):  # rm XXX命令：删除文件：文件夹名称
        length = len(self.file)
        for i in range(length):  # 寻找该文件
            if self.file[i].file_name == fl:
                f = self.file.pop(i)  # f：待删除文件
                # 更新磁盘信息
                disk.capacity += (f.length + 1)   # 更新磁盘容量
                index = disk.disk_content[f.index_r][f.index_c]  # 取出文件的索引

                for j in index:   # 遍历文件索引，清空磁盘块，位图置0
                    if j == -1:
                        break
                    else:
                        r = j // disk.col
                        c = j % disk.col
                        disk.disk_content[r][c] = ""
                        disk.bitmap[r][c] = 0

                disk.disk_content[f.index_r][f.index_c] = ""  # 索引所在的磁盘清空
                disk.bitmap[f.index_r][f.index_c] = 0  # 索引所在位图置0

                print("文件删除成功！")
                return

        print("不能删除文件" + fl + ": 文件不存在")

    def find_directory(self, dire):  # 查找文件夹内是否存在dire目录，是则返回对象，否则返回False
        length = len(self.directory)
        for i in range(length):
            if self.directory[i].directory_name == dire:
                return self.directory[i]
        return False

    def find_file(self, fl):  # 查找文件夹内是否存在fl文件，是则返回对象，否则返回False
        length = len(self.file)
        for i in range(length):
            if self.file[i].file_name == fl:
                return self.file[i]
        return False



