# LeetCode 438. 找到字符串中所有字母异位词（中等）
# 套路：定长滑动窗口 + 26 位计数数组增量更新，O(n) 时间 / O(1) 空间
# 2026-09-25
# 最优代码（面试首推）

class Solution:
    def findAnagrams(self, s: str, p: str) -> list:
        n, m = len(s), len(p)
        ans = []
        if n < m:                    # s 比 p 短，不可能有异位词，直接返回
            return ans

        need = [0] * 26              # p 的字母计数，只算一次（循环外，固定不变）
        for ch in p:
            need[ord(ch) - ord('a')] += 1

        win = [0] * 26               # 当前窗口计数，也只初始化一次
        for ch in s[:m]:             # 初始窗口 s[0:m]，只完整数这一遍
            win[ord(ch) - ord('a')] += 1

        if win == need:              # Python 列表 == 会逐位比较 26 格，常数级
            ans.append(0)

        for i in range(m, n):        # 右端从 m 起，窗口逐步右移
            # 只做「一进一出」两次 O(1) 更新，中间 m-2 个字符原地不动
            win[ord(s[i]) - ord('a')] += 1       # 进来：s[i]
            win[ord(s[i - m]) - ord('a')] -= 1   # 出去：s[i - m]
            if win == need:
                ans.append(i - m + 1)            # 窗口起点 = 右端 - 长度 + 1
        return ans


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert s.findAnagrams("abab", "ab") == [0, 1, 2]
    # 边界用例
    assert s.findAnagrams("ab", "abc") == []           # s 比 p 短
    assert s.findAnagrams("a", "a") == [0]             # 单字符
    assert s.findAnagrams("aaaaaaaaaa", "aaaaaaaaaaaaa") == []  # s 全同但更短
    assert s.findAnagrams("abc", "abc") == [0]         # 完全相等，只命中起点 0
    assert s.findAnagrams("zzz", "aaa") == []          # 首尾字母下标 25 不越界
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 核心思想：相邻两个窗口只差「一进一出」两个字符，中间的 m-2 个字符原地不动。
#    所以窗口计数不必每轮重数，只需 win[进] += 1、win[出] -= 1 两笔 O(1) 更新。
#    这是从 v2 的 O(n·m) 超时优化到 O(n) 的关键。
# 2. win == need 直接用列表比较：两个长度 26 的列表，== 会从第 0 格比到第 25 格，
#    26 是常数，所以整体仍是 O(1)。不必手写 diff 差分计数（那是更进阶的玩法，本题不必）。
# 3. 命中下标 = i - m + 1：窗口右端在 i、长度 m，则左端（起点）= i - m + 1。
#    写成 i - m 会差一格，是这类题最容易写错的地方。
# 4. ord(ch) - ord('a')：把字符映射到 0~25 的格子下标（a→0，z→25），
#    只对小写字母成立，与 LC 242 同一技巧。
# 5. 同类题：LC 567 字符串的排列（近亲）、LC 76 最小覆盖子串（进阶，窗口长度可变），
#    都是「滑动窗口 + 计数数组」家族，吃透一个能带一串。
