import sys
import os

sys.path.append(os.path.abspath("."))
import sys
import os

sys.path.append(os.path.abspath("."))
from cilly_work.cilly.lexer.scanner import tokenize
from cilly_work.cilly.lexer.tokens import get_token_tag, get_token_value


def test_operator(code, expected_operator):
    print(f"\n测试代码: {code}")
    tokens = tokenize(code)
    print("\n生成的 tokens:")
    for token in tokens:
        print(f"Token type: {get_token_tag(token)}, value: {get_token_value(token)}")

    found = False
    for token in tokens:
        if get_token_tag(token) == expected_operator:
            print(f"\n✅ 成功识别 {expected_operator} 运算符!")
            found = True
            break

    if not found:
        print(f"\n❌ 未能识别 {expected_operator} 运算符!")

    return found


# 测试各种运算符
test_cases = [
    ("if (x == y) {}", "=="),
    ("if (a != b) {}", "!="),
    ("if (x >= y) {}", ">="),
    ("if (x <= y) {}", "<="),
    ("if (a && b) {}", "&&"),
    ("if (a || b) {}", "||"),
]

print("\n=== 开始测试所有双字符运算符 ===")
all_passed = True
for code, operator in test_cases:
    result = test_operator(code, operator)
    all_passed = all_passed and result

if all_passed:
    print("\n✅✅✅ 所有测试通过! ✅✅✅")
else:
    print("\n❌❌❌ 部分测试失败! ❌❌❌")
for code, operator in test_cases:
    test_operator(code, operator)
