# LeetCode 150. 逆波兰表达式求值（中等）
# 套路：栈（遇数字入栈，遇运算符弹出两个数算完再压回）
# 2026-10-31
# 我的解答（逻辑框架对，但两个操作数弹出顺序反了，减法和除法全错）

class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        ans_stack = []
        for ch in tokens:
            if ch.lstrip('-').isdigit():        # 这一行是对的：兼容多位数和负数
                ans_stack.append(int(ch))
            else:
                num1 = ans_stack.pop()          # 错：先弹出的是「右操作数」
                num2 = ans_stack.pop()          #     后弹出的才是「左操作数」
                ans_stack.append(self._clac(num1, num2, ch))
        return ans_stack.pop()

    def _clac(self, a: int, b: int, op: str):   # 拼写也是 _calc
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return int(a / b)                   # 向零取整，这行是对的


if __name__ == "__main__":
    s = Solution()

    # 下面的断言是「本版实际输出」，用来保留 WA 证据
    assert s.evalRPN(["2", "1", "+"]) == 3
    print("碰巧通过 ✓ ['2','1','+'] -> 3（加法满足交换律，顺序反了也看不出来）")

    assert s.evalRPN(["2", "1", "-"]) == -1
    print("反面演示 ✓ ['2','1','-'] 返回 -1，正确答案应为 1（算成了 1-2）")

    assert s.evalRPN(["4", "13", "5", "/", "+"]) == 4
    print("反面演示 ✓ ['4','13','5','/','+'] 返回 4，正确答案应为 6（算成了 5/13=0）")

    assert s.evalRPN(["3", "-4", "*"]) == -12
    print("碰巧通过 ✓ ['3','-4','*'] -> -12（乘法也满足交换律）")

    big = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    assert s.evalRPN(big) == -198
    print("反面演示 ✓ 官方大用例返回 -198，正确答案应为 22")

    # 这一组不是返回错误值，而是直接崩溃
    try:
        s.evalRPN(["0", "3", "/"])
        print("意外：没有崩溃")
    except ZeroDivisionError:
        print("反面演示 ✓ ['0','3','/'] 直接抛 ZeroDivisionError（算成了 3/0）")


# 踩坑记录：
# 1. 核心错误：两个操作数弹出顺序反了。
#    RPN 写法是「操作数1 操作数2 运算符」，入栈顺序是 2、1，出栈是 1、2。
#    所以第一次 pop 拿到的是「右操作数」，第二次才是「左操作数」。
#    写成 num1 = pop() 会让 _clac(a, b) 里的 a 变成右边的数，减法除法全反。
# 2. 这类 bug 最阴险的地方：**加法和乘法满足交换律，测试时会碰巧通过**。
#    ['2','1','+'] 和 ['3','-4','*'] 两个用例都是 OK 的，容易误判成"已经对了"。
#    自查方法：专门挑减法和除法测，或者挑一个会让除数为 0 的用例（会暴露得更彻底）。
# 3. 除零崩溃比答错更严重：['0','3','/'] 顺序反了会算成 3/0，程序直接抛异常。
# 4. 除法取整方向：题目要求「向零取整」，Python 的 // 是「向下取整」，
#    -7/2 用 // 得 -4，用 int(-7/2) 得 -3。必须用 int(a / b)。
# 5. 判断数字那行写对了：ch.lstrip('-').isdigit() 能兼容 "-11"，
#    单纯用 ch.isdigit() 会把负数误判成运算符。
# 6. 方法名 _clac 拼写应为 _calc，不影响运行但影响可读性。
# 7. 修正版见 solution_v2.py。
