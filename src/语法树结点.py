# encoding: utf-8
# Auther:段云飞
# Since: 2019-12-1
import types


def require_fuc(func):
    if func is not None and not isinstance(func, types.FunctionType):
        raise TypeError('参数 func 必须是函数或方法或None。')


class N:
    """
    学习完属性文法之后认为有必要设计一个类，代表文法中的终结符和
    非终结符，其中终结符可能具有综合属性 self.val ，如 INT,REAL
    的 val 值就是它的字面值，非终结符的综合属性和继承属性因Python
    的语法性质，可以动态添加，便于扩展和调试。
    """

    def __init__(self, msg, val=None, f=None, key=None):
        require_fuc(f)
        self.f = f
        # 参数 msg 必须是可描述的字符串
        self.msg = str(msg)
        self.val = val
        # 参数 self.key 是为了与语法分析器LR分析表兼容而设计的
        # 如LR分析表中的非终结符可以代表变量，整形常量，实型常量
        self.key = self.msg if key is None else key

    def __str__(self):
        """
        学属性文法之前我使用元组表示文法符号，所以为了信息
        表示上的兼容，重写了 self.__str__
        :return: 一种元组的视图
        """
        return "('{}', '{}')".format(self.msg, '' if self.val is None else self.val)

    def __call__(self, *args, **kwargs):
        """
        暂时是多余的设计，因为学过一些仿函数的思想
        所以就重写了 self.__call__
        :param args:
        :param kwargs:
        :return:
        """
        if self.f is not None:
            return self.f(*args, **kwargs)


if __name__ == '__main__':
    pass
