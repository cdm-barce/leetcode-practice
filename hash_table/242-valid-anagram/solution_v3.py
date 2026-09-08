# LeetCode 242. 有效的字母异位词（简单）
# 套路：collections.Counter 计数比较，O(n) 时间 / O(k) 空间（k 为不同字符数）
# 2026-09-08
# 我的解答（工程写法：不挑字符集，中文、Unicode 都能处理）
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Counter(s) 会一次性统计每个字符的出现次数，返回 dict 子类
        # Counter 之间可以直接用 == 比较，键和值都相同才相等
        return Counter(s) == Counter(t)


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.isAnagram("anagram", "nagaram") is True
    assert s.isAnagram("rat", "car") is False
    # 边界用例
    assert s.isAnagram("", "") is True                      # 两个空串
    assert s.isAnagram("a", "ab") is False                  # 长度不等
    assert s.isAnagram("ab", "ba") is True                  # 两字符互换
    assert s.isAnagram("aacc", "ccac") is False             # 长度相等但构成不同
    assert s.isAnagram("Aa", "aA") is True                  # 大小写敏感
    assert s.isAnagram("你好吗", "好吗你") is True            # Unicode 中文同样有效
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 别用 str.count() 一行流，看着优雅实则是 O(n²)：
#       return len(s) == len(t) and all(s.count(c) == t.count(c) for c in set(s))
#    因为 count() 每次调用都要把字符串重扫一遍，set(s) 有多少个不同字符就扫多少轮。
#    数据量大直接超时。
# 2. Counter 的几个实用特性：
#       Counter("anagram")['a']  → 3
#       Counter("anagram")['z']  → 0   访问不存在的 key 返回 0，不抛 KeyError
#       Counter("anagram") - Counter("nagaram")  → Counter()  空即相等
#    它是 dict 的子类，dict(...) 能转回普通字典。
# 3. 复杂度：时间 O(n)；空间 O(k)，k 为不同字符数，
#    比 v2 的定长数组多占一点，但换来了字符集无关的可读性。
# 4. 三版怎么选：面试手写用 v2（展现代价分析），实际项目用 v3（更稳），
#    只想最快 AC 用 v1 的 sorted 一行。
