# LeetCode 9. 回文数（简单）
# 套路：字符串比较，O(n) 时间 / O(n) 空间
# 2026-09-06
# 我的解答（v1 精简版）
# 思路：负号会让字符串反转后位置对不上（"-121" -> "121-"），
#       所以负数天然判为 False，不需要特判
class Solution:
    def isPalindrome(self, x: int) -> bool:
        s = str(x)
        return s == s[::-1]


# 海象运算符一行版（Python 3.8+，:= 在表达式里顺便赋值）
# return (s := str(x)) == s[::-1]


if __name__ == "__main__":
    s = Solution()
    assert s.isPalindrome(121) is True
    assert s.isPalindrome(-121) is False
    assert s.isPalindrome(10) is False
    # 边界：0~9 单个数字正反读一样，都是回文数
    for d in range(10):
        assert s.isPalindrome(d) is True
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 最初写法 if str(x) == y[::-1]: return True else: return False
#    —— 条件本身就是布尔值，直接 return 条件 即可，别写冗余分支
# 2. 性能：Python 里切片是 C 实现，这个解法 7ms 击败 70%+，
#    纯刷题够用；但面试常追问"不转字符串怎么做"，见 v2/v3
