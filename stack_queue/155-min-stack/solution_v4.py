# LeetCode 155. 最小栈（中等）
# 套路：差值编码（栈里存「当前值 - 入栈时最小值」，用差值的正负当标记位），额外空间 O(1)
# 2026-10-25
# 理论最优（面试加分项；但 Python 里并不比 v3 省内存，见末尾实测）

class MinStack:
    def __init__(self):
        self.diff = []               # 存 val - 入栈那一刻的 min_val
        self.min_val = 0             # 真实最小值，只占一个变量

    def push(self, value: int) -> None:
        if not self.diff:
            self.diff.append(0)      # 第一个元素差值为 0
            self.min_val = value
        else:
            self.diff.append(value - self.min_val)
            if value < self.min_val:
                self.min_val = value  # 刷新最小值，只改变量，不额外存东西

    def pop(self) -> None:
        d = self.diff.pop()
        if d < 0:                    # 负数 = 它入栈时就是历史最小值
            self.min_val -= d        # 反解出上一个最小值

    def top(self) -> int:
        d = self.diff[-1]
        # 差值为负说明当时它自己就是最小值，真实值就是 min_val
        return self.min_val if d < 0 else self.min_val + d

    def getMin(self) -> int:
        return self.min_val


def run(ops, args):
    s = MinStack()
    out = []
    for op, a in zip(ops, args):
        out.append(getattr(s, op)(a) if op == "push" else getattr(s, op)())
    return out


if __name__ == "__main__":
    # 官方示例
    assert run(["push", "push", "push", "getMin", "pop", "top", "getMin"],
               [-2, 0, -3, None, None, None, None]) == [None, None, None, -3, None, 0, -2]

    # 边界：最小值重复
    s = MinStack()
    for v in [0, 1, 0]:
        s.push(v)
    assert s.getMin() == 0
    s.pop()
    assert s.getMin() == 0

    # 边界：负数嵌套（差值会跨正负，最容易算错）
    s = MinStack()
    for v in [-5, -3, -8, 2]:
        s.push(v)
    assert s.getMin() == -8
    assert s.top() == 2
    s.pop()
    assert s.top() == -8
    s.pop()
    assert s.getMin() == -5

    # 边界：单调递减
    s = MinStack()
    for v in [4, 3, 2, 1]:
        s.push(v)
    assert s.getMin() == 1
    s.pop()
    assert s.getMin() == 2 and s.top() == 2

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心思想：栈里不存元素本身，存「它相对当时最小值的差值」。
#    差值 >= 0 说明入栈时它不是最小值（真实值 = min_val + 差值）；
#    差值 < 0 说明它就是新的最小值（真实值 = 当前 min_val）。
#    一个符号位同时承担了「数据」和「标记」两个作用，所以额外空间只有 min_val 一个变量。
# 2. C++/Java 实现这题必须用 long long 防溢出（差值可能到 INT_MAX - INT_MIN），
#    Python 整数是任意精度，天然没有这个问题，写起来反而更简单。
# 3. 但在 Python 里它并不是内存最优。实测 n=20000 的 tracemalloc 峰值：
#        数据形态      同步辅助栈   最小值栈(v3)   差值法
#        严格递增       338 KB      169 KB       786 KB
#        严格递减       338 KB      338 KB       169 KB
#        全部相同       338 KB      338 KB       169 KB
#    原因：push 进来的值来自输入数组、对象本来就存在，append 只是加引用（8 字节）；
#    而差值法要现算 `value - min_val`，在严格递增时会新造 n 个 int 对象（每个 28 字节），
#    反而比 v3 多占 4 倍内存。定长整型语言里省空间的技巧，到了 Python 未必成立。
# 4. 结论：LeetCode 提交用 v3（实测最省、代码最直白）；面试时把这一版讲出来证明
#    「知道额外空间可以压到 O(1)」。
