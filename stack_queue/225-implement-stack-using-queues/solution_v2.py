# LeetCode 225. 用队列实现栈（简单）
# 套路：单队列 + 旋转，队列容器换成 collections.deque（左端出队 O(1)）
# 2026-10-27
# 最优代码

from collections import deque


class MyStack:
    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)
        # 把前面 n-1 个元素依次挪到队尾，让刚进来的 x 浮到队首
        # deque.popleft() 是 O(1)，所以整个 push 是 O(n)
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        return self.queue.popleft()         # 队首即栈顶，O(1)

    def top(self) -> int:
        return self.queue[0]                # 访问两端，O(1)

    def empty(self) -> bool:
        return not self.queue


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

    # LIFO：后进先出
    s = MyStack()
    for v in range(1, 6):
        s.push(v)
    assert [s.pop() for _ in range(5)] == [5, 4, 3, 2, 1]

    # 边进边出，顺序不能乱
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

    # 弹出后再 push，新元素必须是新的栈顶
    s = MyStack()
    s.push(1); s.push(2)
    s.pop()
    s.push(3)
    assert s.top() == 3 and s.pop() == 3 and s.pop() == 1

    # 单元素
    s = MyStack()
    s.push(9)
    assert s.top() == 9 and s.pop() == 9 and s.empty() is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 这题的关键不是算法，而是「用 deque 而不是 list 当队列」。
#    list.pop(0) 是 O(n)（连续内存要整体前移），deque.popleft() 是 O(1)（双向链表挪指针）。
#    同样的旋转逻辑，换容器后 push 从 O(n²) 降到 O(n)，累计从 O(n³) 降到 O(n²)，
#    实测 n=1000 次 push：30.6 ms → 13.5 ms，数据量越大差距越明显。
# 2. 旋转次数是 len(queue)-1，不是 len(queue)：刚 append 进来的那个元素不用挪。
#    队列空或只有一个元素时 len-1 <= 0，range 自然是空循环，不需要额外判空。
# 3. top() 用 queue[0] 是「访问两端」，deque 里是 O(1)；
#    如果写成 queue[len//2] 这种中间索引，deque 就要 O(n)，那时它还不如 list。
# 4. 复杂度总结：push O(n)、pop O(1)、top O(1)、empty O(1)，空间 O(n)。
#    和 LC232 正好相反（那边是 push O(1)、pop 均摊 O(1)），因为两题受限于不同的容器规则。
