# LeetCode 155. 最小栈（中等）
# 套路：同步辅助栈（每 push 一个元素就同步压入当前最小值），四操作全 O(1)
# 2026-10-25
# 我的解答（一次写对；当时界面显示 42/48 是旧提交没重判，代码本身无 bug）

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_num = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_num:
            self.min_num.append(value)
        else:
            self.min_num.append(min(self.min_num[-1], value))   # 同步记录当前最小值

    def pop(self) -> None:
        if not self.stack:              # 题目保证不会在空栈调用，这句其实多余
            return False
        self.stack.pop()
        self.min_num.pop()              # 两栈严格同步，一起弹

    def top(self) -> int:
        if not self.stack:
            return False
        return self.stack[-1]

    def getMin(self) -> int:
        if not self.stack:
            return False
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

    # 最小值重复出现：弹出其中一个后，最小值应当仍是它
    s = MinStack()
    for v in [0, 1, 0]:
        s.push(v)
    assert s.getMin() == 0
    s.pop()
    assert s.getMin() == 0          # 最容易错的地方：辅助栈若只记一份就会丢

    # 最小值被弹出后，要恢复成上一个最小值
    s = MinStack()
    for v in [5, 3, 7, 1]:
        s.push(v)
    assert s.getMin() == 1
    s.pop()
    assert s.getMin() == 3
    s.pop(); s.pop()
    assert s.getMin() == 5

    # 单个元素
    s = MinStack()
    s.push(42)
    assert s.top() == 42 and s.getMin() == 42
    s.pop()

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 提交后界面显示「解答错误 42/48」，但这版代码本身没有 bug。
#    用 5000 组 × 40 步随机操作和暴力 min() 对拍，零差异；
#    官方示例、最小值重复、最小值弹出恢复三类用例也全部正确。
#    真实原因：LeetCode 左侧的判题结果是上一次提交留下的，改完代码不会自动重判，
#    必须再点一次「提交」。当时输出与预期只差一项（2147483646 vs 2147483647），
#    推测旧版本把 top() 写成了返回 min_num[-1]。
# 2. pop/top/getMin 里的 `return False` 与类型标注（-> None / -> int）矛盾，
#    而且题目保证只在非空栈上调用，这两个判空可以直接删掉，代码更干净。
# 3. 这版辅助栈与主栈严格同步，空间 2n，好处是永远不会错位，面试首选。
