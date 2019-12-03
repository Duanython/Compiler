## 编译原理
* 语言简介   
1.解释型语言   
2.支持简单变量的赋值与四则运算   
3.简单变量使用前需赋初值，否则报错   
4.该语言以#作为语句分隔符   
5.该语言的注释为// 或 /* */   
6.源文件以dyf后缀名结尾，中间代码生成文件以dyfc后缀名结尾
* 词法分析器简介   
1.支持任何你能想到的关键字、保留字、运算符的识别   
2.词法分析器接受字符流，输出终结符流   
3.词法分析器与扫描器属于第二次设计，可复用性较好
*语法分析器   
1.可读性较差   
2.类的设计的有问题，属于面向对象的半成品
*语义分析器   
1.字面值在语义分析阶段就计算完成   
2.设计与实现仅用一天，比较仓促，没有参考主流解释器的构造
####赋值与四则运算语句的文法：
* S' -> S
* S-> V:=E
* V -> ID
* E -> E+T
* E -> E-T
* E -> T
* T -> T*F
* T -> T/F
* T -> T%F
* T -> F
* F ->(E)
* F-> ID
* F->i   
注：i 代表字面值，如'REAL','INT'