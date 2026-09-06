# LeetCode 9. 回文数（简单）
# 套路：拆位存列表 + 切片反转比较，O(n) 时间 / O(n) 空间
# 2026-09-06
# 我的解答（v2，第一次提交报解答错误后修复）
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        digits = []
        while x:
            digits.append(x % 10)   # 摘下末位
            x //= 10                # 甩掉末位
        return digits == digits[::-1]


if __name__ == "__main__":
    s = Solution()
    assert s.isPalindrome(121) is True
    assert s.isPalindrome(-121) is False
    assert s.isPalindrome(10) is False
    assert s.isPalindrome(0) is True
    print("全部用例通过 ✓")

# 踩坑记录（重要！）：
# 第一次提交写的是：
#     if list_num == list_num.reverse():   # 错！
#         return True
#     else:
#         return False
#
# 原因：list.reverse() 是【原地】反转，返回值是 None，
#       所以这行实际是 list_num == None，永远 False，
#       连 121 都判错，LeetCode 三个用例全挂。
#
# 知识点：Python 刻意让原地操作方法（reverse / sort / append...）
# 返回 None，提醒你别误用。需要"返回新结果"时用：
#   - 切片：lst[::-1]（反转）、sorted(lst)（排序）
#   - 内置函数：reversed(lst)
# 或者先 lst.reverse() 再单独比较。
#
# 备注：此解法比 v3 多用 O(n) 空间存列表，但比纯字符串法
# 更贴近"纯数学"的思路，是 v3 的过渡版。
