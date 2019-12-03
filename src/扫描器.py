# encoding: utf-8
# Auther:段云飞
# Since: 2019-11-29
import os


def check_file(file: str):
    if file is None:
        raise ValueError('文件名不应为空。')
    if not os.path.isfile(file):
        raise ValueError('参数 {} 应该是文件。'.format(file))
    if not os.path.exists(file):
        raise ValueError('文件 {} 不存在。'.format(file))


class Scanner:
    """
    Scanner 类从源文件中读取并返回单个字符，供词法分析器使用
    其灵感来源于 Java 中的 LineNUmberReader,某些方法是针对
    词法分析器设计的，在其他应用场景并不适合，这是我第一次使
    用Python写比较长的代码，有些语法糖使用的并不熟练，甚至
    将切片用 ',' 分隔。self.__index__有些设计缺陷，但对词
    法分析器来说有省去了许多'+1'或'-1'的计算。
    注：Scanner仅测试了核心函数。
    """

    def __init__(self, file):
        check_file(file)
        with open(file, encoding='utf-8') as f:
            self.__content = f.read()  # 完全读入内存，不适合大文件读取，此处为了简化程序设计难度
        self.__linenum = 1
        # self.__index 可能取值范围，[-1, self.__len]
        # self.__index 的含义有点像文本文件的光标，位于两字符中间，其值代表光标前一个字符的索引
        # 两个非法值：-1代表在第一个字符之前，self.__len代表在最后一个字符之后
        self.__index = -1
        self.__len = len(self.__content)
        self.__file = file

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def back(self):
        if self.__index < 0:
            raise IndexError('已到源文件开头，不能回退。')
        if self.__content[self.__index] == '\n':
            self.__linenum = self.__linenum - 1
        self.__index = self.__index - 1

    def current(self):
        self.__checkrange()
        return self.__content[self.__index]

    def next(self):
        self.__index = self.__index + 1
        if self.__index >= self.__len:
            raise StopIteration('源文件发出EOF信号。')
        tmp = self.__content[self.__index]
        if tmp == '\n':
            self.__linenum = self.__linenum + 1
        return tmp

    def peek(self):
        """
        查看但不消耗掉下一个字符
        :return: 下一个字符
        """
        tmp = self.next()
        self.back()
        return tmp

    def nextline(self):
        """
        将self.__index__移动到字符\n后
        下一次调用self.__next__()方法返回下一行的第一个字符
        :return:
        """
        # 因为self.__index__有两个特殊值，所以这么麻烦
        pos = -1
        start = self.__index
        if start < self.__len:
            if start == -1:
                start = 0
            pos = self.__content.find('\n', start)
        if pos == -1:
            # 没找到\n，自动移到源文件结尾
            self.__index = self.__len
            raise StopIteration('已到达最后一行，行号：{}'.format(self.__linenum))
        self.__index = pos
        self.linenum = self.linenum + 1

    def __getitem__(self, start):
        """
        返回从开始索引（闭区间）到向前位置（开区间）的源文件内容的切片
        :param start:
        :return:
        """
        # 因为没有找到重写切片的magic method，只能用索引方法不合适的代替
        spec = [-1, self.__len]
        if start in spec or self.__index in spec or start > self.__index:
            raise ValueError('索引范围出错：[{}, {}]'.format(start, self.__index))
        return self.__content[start: self.__index]

    def __checkrange(self):
        if self.__index == -1:
            raise ValueError('未调用过__next__或next方法')
        if self.__index >= self.__len:
            raise ValueError('已到达源文件结束位置')

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, newfile):
        self.__init__(self, newfile)

    @property
    def content(self):
        return self.__content

    @property
    def index(self):
        self.__checkrange()
        return self.__index

    @property
    def linenum(self):
        return self.__linenum

    @linenum.setter
    def linenum(self, newlinenum: int):
        if newlinenum <= 0:
            raise ValueError('行号 {} 不能为负数'.format(newlinenum))
        self.__linenum = newlinenum


if __name__ == '__main__':
    for si in Scanner('source.txt'):
        print(si, end='')
