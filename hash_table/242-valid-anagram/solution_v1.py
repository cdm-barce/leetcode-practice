# LeetCode 242. 有效的字母异位词（简单）
# 套路：排序后比较，O(n log n) 时间 / O(n) 空间
# 2026-09-08
# 我的解答（排序思路的修正版，v1 原始写法误用了 split）
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # str 本身就是「字符的可迭代对象」，sorted 会把它拆成字符列表再排序
        # sorted("anagram") → ['a','a','a','g','m','n','r']
        # 两个字符串若是异位词，排序后的字符列表必然完全相同
        return sorted(s) == sorted(t)


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.isAnagram("anagram", "nagaram") is True
    assert s.isAnagram("rat", "car") is False
    # 边界用例
    assert s.isAnagram("", "") is True              # 两个空串
    assert s.isAnagram("a", "ab") is False          # 长度不等
    assert s.isAnagram("ab", "ba") is True          # 两字符互换
    assert s.isAnagram("aacc", "ccac") is False     # 长度相等但字符构成不同
    assert s.isAnagram("Aa", "aA") is True          # 大小写敏感，位置互换仍算异位
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 【核心 bug】第一版写成了：
#       seen1 = s.split(" ")
#       seen1.sort()
#       seen2 = t.split(" ")
#       seen2.sort()
#       return seen1 == seen2
#    结果 s="anagram", t="nagaram" 期望 True 却返回了 False。
#    根因：split(" ") 是「按分隔符切词」，给句子用的。
#      "anagram" 里没有空格，split 后得到的是 ['anagram'] —— 整个字符串
#      变成列表里的一个元素。sort() 对单元素列表什么都排不动，
#      最后比较的是 ["anagram"] == ["nagaram"]，整串比整串，自然 False。
#    正确做法：要排字符就不要 split，直接 sorted(s)，
#      或者先 list(s) 转成字符列表再 .sort()。
# 2. 字符串要用 sorted 排序字符时，返回的是「字符列表」而不是字符串。
#    想拿回字符串得 "".join(sorted(s))。
# 3. sorted() 与 list.sort() 的区别：sorted 返回新列表、原对象不变；
#    sort() 原地修改且返回 None。写成 b = a.sort() 会得到 None。
# 4. 复杂度：排序 O(n log n)，空间 O(n)（字符列表）。
#    这题还存在 O(n) 的计数解法，见 v2。
