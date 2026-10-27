# LeetCode 225. 用队列实现栈（简单）
# 套路：单队列 + 旋转（push 后把前面 n-1 个元素挪到队尾，让新元素浮到队首）
# 2026-10-27
# 我的解答（逻辑正确，但用 list 模拟队列，pop(0) 是 O(n)，性能差）

class MyStack:
    def __init__(self):
        self.queue = []

    def push(self, x: int) -> None:
        self.queue.append(x)
        self.shift()                        # 立刻旋转，保证队首永远是最新元素

    def pop(self) -> int:
        return self.queue.pop(0)            # 从队首弹出 = 弹栈顶，但 list 的 pop(0) 是 O(n)

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return not self.queue

    def shift(self) -> None:
        n = len(self.queue) - 1
        if self.queue:                      # 这句多余，range(负数) 本来就是空循环
            for i in range(n):
                self.queue.append(self.queue.pop(0))   # 每次 pop(0) 都要挪动后面所有元素


def run(ops, args):
    s = MyStack()
    out = []
    for op, a in zip(ops, args):
        out.append(getattr(s, op)(a) if op == "push" else getattr(s, op)())
    return out


if __name__ == "__main__":
    # 官方示例
    assert run(["push", "push", "top", "pop", "empty"],
               [1, 2, None, None, None]) == [None, None, 2, 2, False]

    # LIFO：后进先出，和队列顺序相反
    s = MyStack()
    for v in range(1, 6):
        s.push(v)
    assert [s.pop() for _ in range(5)] == [5, 4, 3, 2, 1]

    # 边进边出
    s = MyStack()
    s.push(1)
    assert s.top() == 1 and s.pop() == 1
    s.push(2); s.push(3)
    assert s.top() == 3
    assert s.pop() == 3
    s.push(4)
    assert s.pop() == 4
    assert s.pop() == 2
    assert s.empty() is True

    # 单元素
    s = MyStack()
    s.push(9)
    assert s.top() == 9 and s.pop() == 9 and s.empty() is True

    print("全部用例通过 ✓（逻辑正确，但 push 累计到 O(n³)，见踩坑记录）")


# 踩坑记录：
# 1. 思路是对的：单队列旋转。push 时把前面 n-1 个元素依次从队首挪到队尾，
#    新元素就自然浮到队首，于是 pop/top 直接取队首即可。
# 2. 性能问题在 `list.pop(0)`：list 是连续内存，从头部弹出要把后面所有元素前移一格，O(n)。
#    放到 push 的循环里，第 k 次 push 要挪 k-1 次、每次 O(k)，单次 O(k²)，累计到 O(n³)。
#    实测（n 次 push）：
#      n=300   list 1.8 ms   deque 1.4 ms
#      n=600   list 7.5 ms   deque 4.6 ms
#      n=1000  list 30.6 ms  deque 13.5 ms
#    换成 collections.deque 的 popleft()（O(1)）后，push 降到 O(n)、pop 降到 O(1)。
#    见 solution_v2.py。
# 3. `if self.queue:` 这层判断是多余的：队列空时 n = -1，range(-1) 本来就是空循环。
# 4. 方法名 shift 实际做的是「旋转」，叫 _rotate 更准确；下划线前缀表示内部方法。
# 5. 这题是 LC232（用栈实现队列）的镜像题。两题对照着看：
#      LC232 → 两个栈 + 懒惰倒腾，均摊 O(1)
#      LC225 → 一个队列 + 旋转，push O(n)、pop O(1)
#    本质都是「用 A 的规则去模拟 B 的顺序」，靠反转让顺序翻转。
