# encoding: utf-8
# Auther:段云飞
# Since: 2019-12-1
from 语法树结点 import N
from types import FunctionType


class Semantics:
    """
    语义分析器封装了课上所学的使用 C语言 表达的
    语义变量及函数，如四元式生成函数Gen，但是本
    实现仅支持二元运算，符号表仅存储了变量名：变量值
    键值对，四元式表存储了以四元式表示的中间代码，
    字面值型的数值计算已优化，不生成中间代码。
    Semantics.trans 方法用于将终结符转换为
    非终结符，添加了非终结符的一些额外的属性
    """
    @classmethod
    def trans(cls, wrapped, Vnname):
        wrapped: N
        wrapped.Vnname = Vnname
        return wrapped

    def __init__(self):
        self.count = 0
        self.__symbol = {}
        self.__fours = []

    @property
    def sysmbol_table(self):
        return self.__symbol

    @property
    def quadruple_list(self):
        return self.__fours

    def Entry(self, key):
        """
        查符号表
        :param key: 变量的标识符
        :return: 标识符所引用的内存地址的值
        """
        value = self.__symbol.get(key)
        if value is None:
            raise ValueError('变量 {} 未初始化。'.format(key))
        return value

    def addEntry(self, key, value):
        """
        添加符号表
        :param key: 变量的标识符
        :param value: 标识符的值，类型任意
        :return: None
        """
        self.__symbol[key] = value

    def Gen(self, op, left, right, Vnname):
        # 类型
        op: N
        left: N
        right: N
        # 参数正确性检查之一
        if not isinstance(op.f, FunctionType):
            raise TypeError('参数op应是可执行函数或方法。')
        # 两个运算对象均为字面值
        numlist = ['INT', 'REAL', 'STRING']
        if left.msg in numlist and right.msg in numlist:
            const = op(left.val, right.val)
            longname = N('REAL' if type(const) == float else 'INT', const, key='i')
            return Semantics.trans(longname, Vnname)
        # 两个运算对象至少有一个是变量
        rightval = self.Entry(right.val) if right.msg == 'ID' else right.val
        leftval = self.Entry(left.val) if left.msg == 'ID' else left.val
        # 生成临时变量。未优化
        tmpname = 'TEMP{}'.format(self.count)
        self.count = self.count + 1
        # 因为是解释型语言，所以解释语句并执行语句的值
        self.addEntry(tmpname, op(rightval, leftval))
        self.__fours.append((op.msg, left.val, right.val, tmpname))
        return Semantics.trans(N('ID', tmpname), Vnname)

    def Gen_assign(self, left, right, Vnname):
        if right.msg == 'ID':
            rightval = self.Entry(right.val)
        elif right.msg in ['CHAR', 'STRING', 'INT', 'REAL']:
            rightval = right.val
        else:
            raise ValueError('右部变量不可赋值给左部。')
        self.addEntry(left.val, rightval)
        self.__fours.append((':=', right.val, '', left.val))
        return Semantics.trans(left, Vnname)


if __name__ == '__main__':
    pass
