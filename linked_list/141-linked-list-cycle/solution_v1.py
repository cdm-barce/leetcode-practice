# LeetCode 141. 环形链表（简单）
# 套路：哈希集合记录访问过的节点，再遇即环，O(n) 时间 / O(n) 空间
# 2026-09-21
# 我的解答

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        seen = set()                 # 集合里存的是“节点对象本身”，不是 val
        while head:
            if head in seen:         # 身份比较（同一个对象才会命中），set 查找 O(1)
                return True
            seen.add(head)           # 先标记当前节点，再前进
            head = head.next
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
    # 边界：空链表
    assert s.hasCycle(build([], -1)) is False
    # 边界：单节点自环
    assert s.hasCycle(build([1], 0)) is True
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 第一版用 list 存 head.val、却用 `if head.next in h` 查节点对象 —— 类型不匹配（int vs ListNode），
#    永远不会命中 True；有环时 `head.next` 永远不在 h 里，循环停不下来 → 死循环直到超时（TLE）。
#    修正：存“节点对象本身”（set 存 head），比身份不比值。
# 2. list 的 `in` 是线性扫描 O(n)，每步都扫一遍 → 总复杂度 O(n²)；换成 set 后查找 O(1)，整体降到 O(n)。
# 3. `head = head.next if head else None` 多余：while 头已保证 head 非空，直接 head = head.next 即可。
