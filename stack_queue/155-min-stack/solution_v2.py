# LeetCode 155. 最小栈（中等）
# 套路：最小值栈改到一半 —— push 改成「只在新最小值时入栈」，但 pop 仍无条件弹两个栈
# 2026-10-25
# 我的解答（反面教材：两栈长度脱钩，一个用例崩、一个用例返回错值）

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_num = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_num or value <= self.min_num[-1]:   # 改对了：只记最小值
            self.min_num.append(value)

    def pop(self) -> None:
        self.stack.pop()
        self.min_num.pop()              # 错：无条件弹，主栈弹掉 3 时辅助栈弹掉的是 1

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_num[-1]


if __name__ == "__main__":
    # 反例 1：辅助栈被提前弹空 → 直接崩
    s = MinStack()
    for v in [1, 2, 3]:
        s.push(v)
    assert s.stack == [1, 2, 3] and s.min_num == [1]
    s.pop()
    assert s.stack == [1, 2] and s.min_num == []      # 本版实际状态，正是 bug 证据
    try:
        s.getMin()
        assert False, "本版本应抛 IndexError"
    except IndexError as e:
        print("反面演示 ✓ push 1,2,3 后 pop，getMin 抛 IndexError:", e)

    # 反例 2：不崩，但返回错值
    s = MinStack()
    for v in [5, 3, 7]:
        s.push(v)
    assert s.stack == [5, 3, 7] and s.min_num == [5, 3]
    s.pop()
    assert s.stack == [5, 3] and s.min_num == [5]     # 弹掉了 3，但 3 还在主栈里
    assert s.getMin() == 5
    print("反面演示 ✓ push 5,3,7 后 pop，getMin 返回 5，正确答案应为 3")


# 踩坑记录：
# 1. 这是「半成品优化」的典型翻车：push 改成了只在 value <= 栈顶最小值时入辅助栈，
#    但 pop 没有跟着改，还是无条件弹两个栈。
#    结果两个栈长度不再一致：主栈弹出的是栈顶元素，辅助栈弹出的却是最小值，
#    要么弹空（IndexError），要么把还在栈里的最小值弄丢（返回错值）。
# 2. push 里的 `<=` 是对的（重复最小值必须各存一份），但 pop 必须配合判断：
#    只有「被弹出的值 == 当前最小值」时才弹辅助栈。修正见 solution_v3.py。
# 3. 教训：栈的 push/pop 永远是一对，改了一边的条件，另一边必须同步改。
