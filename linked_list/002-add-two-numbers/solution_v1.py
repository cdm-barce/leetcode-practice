# LeetCode 2. 两数相加（中等）
# 类别：链表
# 套路：模拟竖式加法 + 哑节点(dummy)，逐位相加处理进位
# 复杂度：时间 O(max(m, n))，空间 O(1)
# 2026-09-05
# 查看解析后的解答
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode],
                            l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()          # 哑节点：假头，方便统一拼接结果
        cur = dummy                 # cur 负责往后接新节点
        carry = 0                   # 进位

        while l1 or l2 or carry:    # 任一链表没走完、或还有进位，就继续
            a = l1.val if l1 else 0     # 短链表走完后补 0（判空判对象本身，不是 .next）
            b = l2.val if l2 else 0

            total = a + b + carry       # 本位的和（含低位进位）
            carry = total // 10         # 新进位：11 → 1，7 → 0
            cur.next = ListNode(total % 10)  # 新节点只留个位
            cur = cur.next

            l1 = l1.next if l1 else None    # 指针后移，None 就原地不动
            l2 = l2.next if l2 else None

        return dummy.next            # 跳过假头，返回真正的结果链表


# ---- 本地测试 ----
def build(nums):
    """列表 → 链表"""
    dummy = ListNode()
    cur = dummy
    for x in nums:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


def to_list(head):
    """链表 → 列表"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    s = Solution()
    assert to_list(s.addTwoNumbers(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]     # 342+465=807
    assert to_list(s.addTwoNumbers(build([0]), build([0]))) == [0]                       # 示例 2
    assert to_list(s.addTwoNumbers(build([9]*7), build([9, 9, 9, 9]))) == [8, 9, 9, 9, 0, 0, 0, 1]  # 不等长+连续进位
    assert to_list(s.addTwoNumbers(build([5]), build([5]))) == [0, 1]                    # 5+5=10，末尾进位落地
    print("全部用例通过 ✓")

# ---- 踩坑记录 ----
# 1. 后移写成 l1 = l1.next if l1.next else None → 对 None 取 .next 直接崩
#    （用例 [9,9,9,9,9,9,9]+[9,9,9,9] 暴露）。判空要判对象本身 l1，不是 l1.next。
# 2. while 条件里的 or carry 不能漏：5+5=10 时两条链都走完还剩进位 1，要补节点。
