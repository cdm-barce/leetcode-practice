# LeetCode 9. 回文数（简单）
# 套路：反转后半段数字，O(n) 时间 / O(1) 额外空间（进阶要求：不用字符串）
# 2026-09-06
# 最优代码
#
# 核心思想：不用翻转整个数，只翻转"后半段"，和剩下的"前半段"比。
#   例：1221 -> 循环摘位 -> x=12, reverted=12 -> 相等，是回文
#   例：12321 -> 奇数位 -> x=12, reverted=123（多含中间位3）
#                -> reverted // 10 = 12 -> 相等，是回文
#
# 循环不变量：每轮把 x 的末位摘下来接到 reverted 末尾，
#   当 reverted >= x 时说明已处理完至少一半位数，循环结束。
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # 陷阱：末尾为 0 的数（10、100、110...）除 0 外都不可能是回文，
        # 因为反转后 0 会跑到开头。不做这个特判，10 会被误判为 True。
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        original, reverted = x, 0
        while x > reverted:
            reverted = reverted * 10 + x % 10   # 摘 x 末位，接到 reverted 尾部
            x //= 10                            # x 甩掉末位
        # 偶数位：x == reverted 直接比
        # 奇数位：reverted 多一位（中间位），//10 丢掉后再比
        return x == reverted or x == reverted // 10


if __name__ == "__main__":
    s = Solution()
    assert s.isPalindrome(121) is True
    assert s.isPalindrome(-121) is False
    assert s.isPalindrome(10) is False      # 关键用例：末尾为 0 的陷阱
    assert s.isPalindrome(1000021) is False
    assert s.isPalindrome(12321) is True    # 奇数位
    assert s.isPalindrome(1221) is True     # 偶数位
    assert s.isPalindrome(0) is True
    for d in range(10):                     # 0~9 都是回文数
        assert s.isPalindrome(d) is True
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 循环条件必须写 x > reverted（严格大于），保证只处理半截；
#    如果写成 x > 0 翻转整个数，会溢出风险且失去 O(1) 意义
# 2. 漏掉末尾为 0 的特判时，输入 10 会错误返回 True：
#    10 -> 第1轮 reverted=0, x=1 -> 第2轮 reverted=1, x=0
#    -> 0 == 1//10 = 0 命中第二个条件，误判
# 相关题目：234. 回文链表（快慢指针找中点 + 反转链表）
