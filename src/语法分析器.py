# encoding: utf-8
# Auther:段云飞
# Since: 2019-11-30

from 词法分析器 import Lexme
from 语法树结点 import N
from 产生式 import Ii
from 语义分析器 import Semantics


class Parser:
    SEMM = Semantics()

    P = [
        Ii('S', 'V:=E', 3, lambda E, op, V: Parser.SEMM.Gen_assign(V, E, 'S')),
        Ii('V', 'ID', 1, lambda ID: Semantics.trans(ID, 'V')),
        Ii('E', 'E+T', 3, lambda T, op, E: Parser.SEMM.Gen(op, E, T, 'E')),
        Ii('E', 'E-T', 3, lambda T, op, E: Parser.SEMM.Gen(op, E, T, 'E')),
        Ii('E', 'T', 1, lambda T: Semantics.trans(T, 'E')),
        Ii('T', 'T*F', 3, lambda F, op, T: Parser.SEMM.Gen(op, T, F, 'T')),
        Ii('T', 'T/F', 3, lambda F, op, T: Parser.SEMM.Gen(op, T, F, 'T')),
        Ii('T', 'T%F', 3, lambda F, op, T: Parser.SEMM.Gen(op, T, F, 'T')),
        Ii('T', 'F', 1, lambda F: Semantics.trans(F, 'T')),
        Ii('F', '(E)', 3, lambda r, E, l: Semantics.trans(E, 'F')),
        Ii('F', 'ID', 1, lambda ID: Semantics.trans(ID, 'F')),
        Ii('F', 'i', 1, lambda i: Semantics.trans(i, 'F'))
    ]

    GOTO = {
        (0, 'V'): 1, (0, 'S'): 22, (3, 'E'): 4,
        (3, 'T'): 5, (3, 'F'): 6, (7, 'E'): 15,
        (7, 'T'): 5, (7, 'F'): 6, (10, 'T'): 16,
        (10, 'F'): 6, (11, 'T'): 17, (11, 'F'): 6,
        (12, 'F'): 18, (13, 'F'): 19, (14, 'F'): 20
    }

    ACTION = {
        (0, 'ID'): ('s', 2), (1, ':='): ('s', 3), (2, ':='): ('r', 1),
        (3, 'ID'): ('s', 8), (3, '('): ('s', 7), (3, 'i'): ('s', 9),
        (4, '+'): ('s', 10), (4, '-'): ('s', 11), (4, '#'): ('r', 0),
        (5, '+'): ('r', 4), (5, '-'): ('r', 4), (5, '*'): ('s', 12),
        (5, '/'): ('s', 13), (5, '%'): ('s', 14), (5, ')'): ('r', 4),
        (5, '#'): ('r', 4), (6, '+'): ('r', 8), (6, '-'): ('r', 8),
        (6, '*'): ('r', 8), (6, '/'): ('r', 8), (6, '%'): ('r', 8),
        (6, ')'): ('r', 8), (6, '#'): ('r', 8), (7, 'ID'): ('s', 8),
        (7, '('): ('s', 7), (7, 'i'): ('s', 9),
        (8, '+'): ('r', 10), (8, '-'): ('r', 10),
        (8, '*'): ('r', 10), (8, '/'): ('r', 10), (8, '%'): ('r', 10),
        (8, ')'): ('r', 10), (8, '#'): ('r', 10),
        (9, '+'): ('r', 11), (9, '-'): ('r', 11),
        (9, '*'): ('r', 11), (9, '/'): ('r', 11), (9, '%'): ('r', 11),
        (9, ')'): ('r', 11), (9, '#'): ('r', 11),
        (10, 'ID'): ('s', 8), (10, '('): ('s', 10), (10, 'i'): ('s', 9),
        (11, 'ID'): ('s', 8), (11, '('): ('s', 11), (11, 'i'): ('s', 9),
        (12, 'ID'): ('s', 8), (12, '('): ('s', 12), (12, 'i'): ('s', 9),
        (13, 'ID'): ('s', 8), (13, '('): ('s', 13), (13, 'i'): ('s', 9),
        (14, 'ID'): ('s', 8), (14, '('): ('s', 14), (14, 'i'): ('s', 9),
        (15, '+'): ('s', 10), (15, '-'): ('s', 11), (15, ')'): ('s', 21),
        (16, '+'): ('r', 2), (16, '-'): ('r', 2),
        (16, '*'): ('s', 12), (16, '/'): ('s', 13), (16, '%'): ('s', 14),
        (16, ')'): ('r', 2), (16, '#'): ('r', 2),
        (17, '+'): ('r', 3), (17, '-'): ('r', 3),
        (17, '*'): ('s', 12), (17, '/'): ('s', 13), (17, '%'): ('s', 14),
        (17, ')'): ('r', 3), (17, '#'): ('r', 3),
        (18, '+'): ('r', 5), (18, '-'): ('r', 5),
        (18, '*'): ('r', 5), (18, '/'): ('r', 5), (18, '%'): ('r', 5),
        (18, ')'): ('r', 5), (18, '#'): ('r', 5),
        (19, '+'): ('r', 6), (19, '-'): ('r', 6),
        (19, '*'): ('r', 6), (19, '/'): ('r', 6), (19, '%'): ('r', 6),
        (19, ')'): ('r', 6), (19, '#'): ('r', 6),
        (20, '+'): ('r', 7), (20, '-'): ('r', 7),
        (20, '*'): ('r', 7), (20, '/'): ('r', 7), (20, '%'): ('r', 7),
        (20, ')'): ('r', 7), (20, '#'): ('r', 7),
        (21, '+'): ('r', 9), (21, '-'): ('r', 9),
        (21, '*'): ('r', 9), (21, '/'): ('r', 9), (21, '%'): ('r', 9),
        (21, ')'): ('r', 9), (21, '#'): ('r', 9), (22, '#'): ('acc',)
    }

    def __init__(self, file):
        self.__lex = Lexme(file)
        self.__itor = iter(self.__lex)

    def complie(self, file=''):
        if file != '':
            self.__init__(file)
        # LR分析过程
        # 状态栈与符号栈
        stack = [
            (0, N('#'))
        ]
        nextN = None
        try:
            nextN = next(self.__itor)
            while True:
                # action表示分析动作
                action = Parser.ACTION[(stack[-1][0], nextN.key)]
                print('分析动作 {}, 栈顶 {}{}, 符号 {}'.format(action, stack[-1][0], stack[-1][1], nextN.key))
                if action[0] == 'acc':
                    # acc函数
                    if len(stack) > 2:
                        print(len(stack))
                        self.__err('自底向上规约失败，但遇到acc动作')
                    else:
                        self.complie()
                    break
                elif action[0] == 's':
                    stack.append((action[1], nextN))
                    nextN = next(self.__itor)
                elif action[0] == 'r':
                    gen = Parser.P[action[1]]
                    vn = gen.f(*(stack.pop()[1] for cnt in range(gen.lens)))
                    stack.append((Parser.GOTO[stack[-1][0], vn.Vnname], vn))
                else:
                    self.__err('不能识别LR分析表的动作: {}{}'.format(action[0], action[1]))
                    break
        except KeyError:
            self.__err('LR分析表中没有指定项：(状态 {}, 余留符号 {})'.format(stack[-1][0], nextN.key))
        except StopIteration:
            if len(stack) > 1:
                self.__err('源程序未遇到符号 # 就结束')
        except BaseException as e:
            self.__err(e.args[0])
        finally:
            return Parser.SEMM.quadruple_list

    def __err(self, errmsg):
        print(self.__lex.msg(), errmsg, sep='')


if __name__ == '__main__':
    lists = Parser('source.dyf').complie()
    with open('source.dyfc', 'w', encoding='utf-8') as f:
        for xy in lists:
            print(xy)
            f.write(str(xy))
