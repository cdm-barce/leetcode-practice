# LeetCode 141. 环形链表（简单）
# 套路：Floyd 快慢指针，速度差 1 必在环内相遇，O(n) 时间 / O(1) 空间
# 2026-09-21
# 最优代码

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        # 循环继续前提：fast 和 fast.next 都存活。
        # fast 一次跳两步，二者任一为 None 都要停，否则下面的 fast.next.next 会踩空。
        while fast and fast.next:
            slow = slow.next        # 慢指针走 1 步
            fast = fast.next.next   # 快指针走 2 步
            if slow == fast:        # 比的是节点身份（同一对象），不是 val
                return True
        return False


if __name__ == "__main__":
    def build(vals, pos):
        """按 vals 建链表，pos>=0 时让尾节点指向 index=pos 的节点形成环；pos=-1 无环。"""
        if not vals:
            return None
        nodes = [ListNode(v) for v in vals]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if pos >= 0:
            nodes[-1].next = nodes[pos]
        return nodes[0]

    s = Solution()
    # 官方用例 1：tail 指向 index 1，有环
    assert s.hasCycle(build([3, 2, 0, -4], 1)) is True
    # 官方用例 2：tail 指向 index 0，有环
    assert s.hasCycle(build([1, 2], 0)) is True
    # 官方用例 3：无环
    assert s.hasCycle(build([1], -1)) is False
    # 边界：空链表 —— fast 一进来就是 None，循环不进，返回 False
    assert s.hasCycle(build([], -1)) is False
    # 边界：单节点自环 —— fast.next 指向自己，走一步后 slow==fast
    assert s.hasCycle(build([1], 0)) is True
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. while 条件只写 `fast.next != None` 漏了 `fast` 自身 —— 空链表时 fast=None，取 fast.next 直接
#    AttributeError('NoneType' object has no attribute next')。修正：`while fast and fast.next`。
# 2. 顺序问题：必须先迈步（slow/fast 各走）再判 `slow==fast`。若一进循环就判相等，起点 slow==fast
#    会被误判成“有环”。
# 3. 为什么速度差 1 一定相遇：进环后把 slow 当静止参考系，fast 每轮相对靠近 1 步，永远不会跨过 slow，
#    只会“刚好到达”，所以 2 步 vs 1 步是最优配置（差为 1 保证精确相遇）。
