# LeetCode 232. 用栈实现队列（简单）
# 套路：双栈 + 懒惰倒腾（push 直接进 in，pop/peek 时才把 in 倒进 out），各操作均摊 O(1)
# 2026-10-26
# 最优代码

class MyQueue:
    def __init__(self):
        self.in_stack = []      # 只管进：push 一律压这里
        self.out_stack = []     # 只管出：pop/peek 只认这里

    def push(self, x: int) -> None:
        self.in_stack.append(x)                 # 进队：直接压 in，不做任何搬移

    def pop(self) -> int:
        self._shift()                           # 先保证 out 有货
        return self.out_stack.pop()

    def peek(self) -> int:
        self._shift()                           # peek 也要先搬，不能直接看 in 的栈顶
        return self.out_stack[-1]

    def empty(self) -> bool:
        # 两个栈都空才算队空：in 空了但 out 还有货时，队列其实非空
        return not self.in_stack and not self.out_stack

    def _shift(self) -> None:
        # 只在 out 空的时候搬一次，这是整题的关键
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())


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

    # 交错操作：in 和 out 同时有元素时，出队顺序不能乱
    q = MyQueue()
    q.push(1); q.push(2)
    assert q.pop() == 1          # 此时 out 被清空，in 也空
    q.push(3)                    # 新元素进 in
    assert q.peek() == 2         # out 还有货，直接用，不搬 in
    assert q.pop() == 2
    assert q.pop() == 3          # out 空了才把 in 里的 3 搬过来
    assert q.empty() is True

    # 全部元素先入后出（FIFO 顺序）
    q = MyQueue()
    for v in range(1, 6):
        q.push(v)
    assert [q.pop() for _ in range(5)] == [1, 2, 3, 4, 5]
    assert q.empty() is True

    # 倒腾之后继续 push，顺序依然正确
    q = MyQueue()
    q.push(1)
    q.pop()
    q.push(2); q.push(3)
    assert q.pop() == 2
    q.push(4)
    assert q.pop() == 3
    assert q.pop() == 4

    # 单元素
    q = MyQueue()
    q.push(7)
    assert q.peek() == 7 and q.pop() == 7 and q.empty() is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 分水岭在「什么时候倒」。每次 pop 前都从 in 倒一遍是 O(n) 每次，
#    累计 O(n²)；只在 out 空时倒，每个元素一生最多被搬两次
#    （一次进 in、一次倒进 out），所以所有操作均摊 O(1)。
# 2. peek 也必须先 _shift。直接返回 in_stack[-1] 是错的——
#    in 的栈顶是最后进的元素，而队首是最早进的。
# 3. empty() 必须同时看两个栈。只判 in 为空会把「还有货没出」误判成空队列。
# 4. out 非空时不要往里倒：倒进去会把旧元素压在新元素下面，顺序直接乱掉。
#    这也是 _shift 里 `if not self.out_stack` 这层判断的真正意义。
# 5. 这题是 LC225（用队列实现栈）的镜像题，两题一起做能彻底理解「用 A 模拟 B」
#    这类题的通用套路：用两个容器互相倒腾，把顺序翻过来。
