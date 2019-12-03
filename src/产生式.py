# encoding: utf-8
# Auther:段云飞
# Since: 2019-12-1
from 语法树结点 import *


class Ii:
    """
    语法制导翻译的属性文法规则，含语义动作，在初始化时指定。
    """
    def __init__(self, left, right, lens, f=None):
        require_fuc(f)
        self.left = str(left)
        self.right = str(right)
        if lens > len(self.right):
            raise ValueError('参数lens是产生式右部Vn,Vt的长度且大于右部字符长度')
        self.__lens = lens
        self.f = f

    def __call__(self, *args, **kwargs):
        """
        仿函数的语法糖，便于产生式对象的语义动作执行
        但是多了一层元组的 pack与 unpack
        :param args:
        :param kwargs:
        :return:
        """
        if self.f is not None:
            return self.f(*args, **kwargs)

    def __str__(self):
        return '{} -> {}'.format(self.left, self.right)

    @property
    def lens(self):
        return self.__lens


if __name__ == '__main__':
    pass
