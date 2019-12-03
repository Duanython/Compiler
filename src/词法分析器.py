# encoding: utf-8
# Auther:段云飞
# Since: 2019-11-30
from 扫描器 import Scanner
from 语法树结点 import N


class Lexme:
    """
    词法分析器从
    """
    RESEVERED = {
        'if': N('if'),
        'then': N('then'),
        'else': N('else'),
        'while': N('while'),
        'begin': N('begin'),
        'end': N('end'),
        'break': N('break'),
        'assert': N('assert'),
        'abstract': N('abstract'),
        'bool': N('bool'),
        'catch': N('catch'),
        'char': N('char'),
        'class': N('class'),
        'const': N('const'),
        'continue': N('continue'),
        'int': N('int'),
        'real': N('real'),
        'for': N('for'),
        'in': N('in'),
        'is': N('is'),
        'null': N('null'),
        'unkown': N('unkown'),
        'this': N('this'),
        'try': N('try'),
        'void': N('void'),
        'super': N('super'),
        'return': N('return')
    }

    SINGLE_OP = {
        '<': N('<', f=lambda x, y: x < y),
        '=': N('=', f=lambda x: x),
        '>': N('>', f=lambda x, y: x > y),
        ':': N(':'),
        '+': N('+', f=lambda x, y: x + y),
        '-': N('-', f=lambda x, y: x - y),
        '*': N('*', f=lambda x, y: x * y),
        '/': N('/', f=lambda x, y: x / y),
        '%': N('%', f=lambda x, y: x % y),
        '!': N('!', f=lambda x: not x),
        '^': N('^', f=lambda x, y: x ^ y),
        '&': N('&', f=lambda x, y: x & y),
        '(': N('('),
        ')': N(')'),
        '[': N('['),
        ']': N(']'),
        '|': N('|', f=lambda x, y: x | y),
        '#': N('#')
    }

    CP_OP = {
        '<=': N('<=', f=lambda x, y: x <= y),
        '<>': N('<>', f=lambda x, y: x != y),
        '>=': N('>=', f=lambda x, y: x >= y),
        ':=': N(':=', f=lambda x: x),
        '==': N('==', f=lambda x, y: x == y),
        '**': N('**', f=lambda x, y: pow(x, y)),
        '&&': N('&&', f=lambda x, y: x and y),
        '||': N('||', f=lambda x, y: x or y)
    }

    CP_OP_PREFIX = ['<', '=', '>', ':', '+', '-', '*', '&', '|']

    def __init__(self, file):
        self.__scan = Scanner(file)
        self.__itor = iter(self.__scan)
        self.__nextc = ''
        self.__drive = {
            '.': self.__numeric,
            '_': self.__alnumor_,
            "'": self.__char,
            '"': self.__string,
        }

    def __iter__(self):
        return self

    def __next__(self):
        while next(self.__itor).isspace():
            pass
        else:
            self.__nextc = self.__scan.current()
        if self.__nextc.isnumeric():
            return self.__numeric()
        if self.__nextc.isalpha():
            return self.__alnumor_()
        if self.__nextc == '/':
            return self.__slash()
        if self.__nextc in Lexme.CP_OP_PREFIX:
            return self.__needpeek()
        func = self.__drive.get(self.__nextc, lambda: Lexme.SINGLE_OP.get(self.__nextc))
        sym = func()
        if sym is None:
            raise SyntaxError(self.msg() + '无法分析符号 {}\n'.format(self.__nextc))
        return sym

    def __alnumor_(self):
        start = self.__scan.index
        while self.__nextc.isalnum() or self.__nextc == '_':
            self.__nextc = next(self.__itor)
        iden = self.__scan[start]
        self.__scan.back()
        return Lexme.RESEVERED.get(iden, N('ID', iden))

    def __numeric(self):
        start = self.__scan.index
        has_exp = False
        has_pnt = False if self.__nextc != '.' else True
        has_sign = False
        radix = ['b', 'x', 'o']
        exp = ['E', 'e']
        sign = ['+', '-']
        while True:
            self.__nextc = next(self.__itor)
            if self.__nextc.isnumeric() or self.__nextc in radix:
                continue
            elif self.__nextc == '.' and not has_pnt:
                has_pnt = True
            elif self.__nextc in exp and not has_exp:
                has_exp = True
            elif self.__nextc in sign and has_exp and not has_sign:
                has_sign = True
            else:
                break
        num = self.__scan[start]
        self.__scan.back()
        try:
            return N('REAL', float(num), key='i') if has_exp or has_pnt else N('INT', int(num), key='i')
        except ValueError:
            raise SyntaxError(self.msg() + '无法将 {} 转换为数字\n'.format(num))

    def __char(self):
        core = next(self.__itor)
        if next(self.__itor) != "'":
            raise SyntaxError(self.msg() + '字符常量 {} 后面出现不匹配的单引号'.format(core))
        return N('CHAR', "'{}'".format(core))

    def __string(self):
        start = self.__scan.index
        while next(self.__itor) != '"':
            pass
        self.__nextc = self.__scan.current()
        return N('STRING', self.__scan[start] + '"')

    def __slash(self):
        tmp = self.__scan.peek()
        if tmp == '/':
            self.__scan.nextline()
        elif tmp == '*':
            try:
                pos = self.__scan.content.index('*/', self.__scan.index + 2)
            except ValueError:
                raise SystemError(self.msg() + '没有与/*匹配的*/')
            for cnt in range(pos + 1 - self.__scan.index):
                self.__nextc = next(self.__itor)
        else:
            return Lexme.SINGLE_OP['/']
        return next(self)

    def __needpeek(self):
        tmp = Lexme.CP_OP.get(self.__nextc + self.__scan.peek())
        if tmp is None:
            return Lexme.SINGLE_OP[self.__nextc]
        next(self.__itor)
        return tmp

    def msg(self):
        return '文件：{} 行号：{}\n'.format(self.__scan.file, self.__scan.linenum)

    def to_statement_end(self):
        while next(self.__itor) != '#':
            pass
        else:
            return Lexme.SINGLE_OP['#']


if __name__ == '__main__':
    for si in Lexme('source.txt'):
        print(si)
