# lec3 Json2py

设计要求：写一个json到python的转换器，输入为字符串表示的json值，将其转换为对应的python的值（json数组转换为python的list，json对象转换为python的dict）。

设计思想：采用模块化设计，满足编程规范。

测试思想：集成测试

## 词法分析器lexer

将输入的JSON字符串拆分为Token流。

### Token定义:tokens.py

token: num | string | 'true' | 'false' | 'null'
     | '[' | ']' | ',' | '{' | '}' | ':'
     ;

### Token扫描器:scanner.py

将JSON字符串转换为Token List。


数字类型NUMNER：
int : [0-9]+;
frac: '.' [0-9]*;
exp: [Ee]('+'|'-')? [0-9]+;

关键字：'true', 'false', 'null';

转义字符： (' ' | '\t' | '\r' |'\n')+;

## 语法分析器parser

将Token流转换为Python数据结构list/dict。

## 测试
