# LeetCode 232. 用栈实现队列（简单）
# 套路：双栈 + 每次 push 都倒腾（保证 pop/peek 严格 O(1)，代价是 push O(n)）
# 2026-10-26
# 对照代码（能用但通常次优，仅在「出队远多于入队」时才有优势）

class MyQueue:
    def __init__(self):
        self.stack = []         # 栈顶永远是队首，所以 pop 直接弹就行
        self.tmp = []           # 倒腾用的临时栈

    def push(self, x: int) -> None:
        # 把现有元素全部倒进 tmp（顺序反转），腾空 stack
        while self.stack:
            self.tmp.append(self.stack.pop())
        self.stack.append(x)    # 新元素压到「栈底」，成为最后一个出队的
        # 再把 tmp 倒回来，原有的队首重新回到栈顶
        while self.tmp:
            self.stack.append(self.tmp.pop())

    def pop(self) -> int:
        return self.stack.pop()         # 栈顶即队首，O(1)

    def peek(self) -> int:
        return self.stack[-1]           # 同样 O(1)

    def empty(self) -> bool:
        return not self.stack


def run(ops, args):
    q = MyQueue()
    out = []
    for op, a in zip(ops, args):
        out.append(q.push(a) if op == "push" else getattr(q, op)())
    return out


if __name__ == "__main__":
    # 官方示例
    assert run(["push", "push", "peek", "pop", "empty"],
               [1, 2, None, None, None]) == [None, None, 1, 1, False]

    # FIFO 顺序
    q = MyQueue()
    for v in range(1, 6):
        q.push(v)
    assert [q.pop() for _ in range(5)] == [1, 2, 3, 4, 5]

    # 边出边进
    q = MyQueue()
    q.push(1); q.push(2)
    assert q.pop() == 1
    q.push(3)
    assert q.pop() == 2
    assert q.pop() == 3
    assert q.empty() is True

    print("全部用例通过 ✓（逻辑正确，但 push 是 O(n)，见踩坑记录）")


# 踩坑记录：
# 1. 这版把「倒腾」放在 push 里，好处是 pop/peek 严格 O(1)，
#    坏处是每来一个新元素都要搬两趟，单次 push O(n)，n 次 push 就是 O(n²)。
#    solution_v1.py 的懒惰倒腾把 n 次 push 摊薄成均摊 O(1)，是更通用的选择。
# 2. 只有一种场景这版更划算：出队次数远多于入队次数，
#    且希望「出队」这条路径绝对快。日常不建议，面试也不加分。
# 3. 踩过的边界：倒腾时必须先把 stack 清空再 append 新元素，
#    否则新元素会被压到栈顶（变成队首），顺序直接反了。
# 4. 这版 empty() 只需看 stack，因为所有元素始终都在 stack 里，tmp 只是过渡。
