# lec3 Json2py

**设计要求：**写一个json到python的转换器，输入为字符串表示的json值，将其转换为对应的python的值（json数组转换为python的list，json对象转换为python的dict）。

**设计思想：**采用模块化设计，满足编程规范。

**测试思想：**自底而上的测试方法，从单元测试到集成测试（包含错误注入测试）

## 词法分析器lexer

将输入的JSON字符串拆分为Token流。

### Token定义:tokens.py

**token:**

 num | string | 'true' | 'false' | 'null'
     | '[' | ']' | ',' | '{' | '}' | ':'
     ;

### Token扫描器:scanner.py

将JSON字符串转换为list[Token]。

**数字类型NUMNER：**
int : [0-9]+;
frac: '.' [0-9]*;
exp: \[Ee]('+'|'-')? [0-9]+;

**关键字：**

'true', 'false', 'null';

**转义字符：**

 (' ' | '\t' | '\r' |'\n')+;

### 功能方法

扫描主函数：scan_tokens

提取数字：_number

提取关键字：_keyword

提取字符串：_string

提取转义符：_escape_char

查看前后字符：_peek，\_peek_prev

添加Token：_add_token

下一个字符：_next

是否在结尾:_is_end

## 语法分析器parser

递归下降地将Token流转换为Python数据结构list/dict。

json : num
     | string
     | 'true' | 'false' | 'null'
     | '[' elements? ']'
     | '{' pairs? '}'
     ;

###  功能方法

解析下一个token值：_parse_value

解析成Python列表：_parse_list

解析Python字典：_parse_dict

匹配并消费：_match

匹配并消费指定类型：_consume

报错：_error

下一个token：_next

检查token类型：_check


## 测试

见test_lexer.ipynb

见test_compiler.ipynb
