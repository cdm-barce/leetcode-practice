# LeetCode 155. 最小栈（中等）
# 套路：最小值栈（辅助栈只存「历史最小值」，push 用 <=、pop 用 == 配对），四操作全 O(1)
# 2026-10-25
# 最优代码（实测最省内存的一版）

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_num = []            # 只存历史最小值序列，不是每个元素一份

    def push(self, value: int) -> None:
        self.stack.append(value)
        # 用 <= 而不是 <：重复的最小值必须各存一份，否则弹掉一个后最小值就丢了
        if not self.min_num or value <= self.min_num[-1]:
            self.min_num.append(value)

    def pop(self) -> None:
        val = self.stack.pop()
        # 只有被弹出的正好是当前最小值，辅助栈才退一格，让上一个最小值重新上位
        if val == self.min_num[-1]:
            self.min_num.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_num[-1]


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

    # 边界：最小值重复出现（v2 就是栽在这里）
    s = MinStack()
    for v in [0, 1, 0]:
        s.push(v)
    assert s.getMin() == 0
    s.pop()
    assert s.getMin() == 0
    s.pop()
    assert s.getMin() == 0

    # 边界：最小值被弹出后要恢复上一个
    s = MinStack()
    for v in [5, 3, 7, 1]:
        s.push(v)
    assert s.getMin() == 1
    s.pop()
    assert s.getMin() == 3
    s.pop(); s.pop()
    assert s.getMin() == 5

    # 边界：单调递减（辅助栈会存满，退化成和主栈一样长）
    s = MinStack()
    for v in [4, 3, 2, 1]:
        s.push(v)
    assert s.getMin() == 1
    s.pop()
    assert s.getMin() == 2

    # 边界：单个元素
    s = MinStack()
    s.push(42)
    assert s.top() == 42 and s.getMin() == 42

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. push 的 `<=` 和 pop 的 `==` 是一对，必须同时改。
#    只改 push 不改 pop → 两栈脱钩（见 solution_v2.py）。
# 2. 用 `<` 代替 `<=` 会漏掉重复最小值：
#    依次 push 0、1、0 时辅助栈只存 [0]，弹掉第一个 0 后辅助栈就空了。
# 3. 空间不再固定 2n：辅助栈长度取决于「最小值被刷新的次数」。
#    实测 n=20000（tracemalloc 峰值）：
#      严格递增 → 169 KB（辅助栈只有 1 个元素）
#      严格递减 → 338 KB（每次都在刷新最小值，退化成 2n）
#      全部相同 → 338 KB（`<=` 让每个相同值都入栈）
# 4. 与同步辅助栈相比省下的不多，但代码一样短，是 LeetCode 提交的推荐版本。
