# LeetCode 438. 找到字符串中所有字母异位词（中等）
# 套路：排序后比较（暴力），O(n·m log m) 时间 / O(m) 空间
# 2026-09-25
# 我的解答（初版：思路正确但两处边界写错，输出错误）

class Solution:
    def findAnagrams(self, s: str, p: str) -> list:
        n = len(s)
        m = len(p)
        ans = []
        p1 = 0

        while p1 < m:                       # BUG②：边界该由 s 决定，不是 p
            cnt = sorted(list(p))           # p 排一次序作为基准
            list1 = sorted(list(s[p1:p1 + m - 1]))   # BUG①：右开区间，少取一格
            if list1 == cnt:
                ans.append(p1)
            p1 += 1
        return ans


if __name__ == "__main__":
    s = Solution()
    # 本版实际会输出错误的空结果，这里用 assert 固化它的真实行为作为反面证据
    assert s.findAnagrams("cbaebabacd", "abc") == []   # 正确应为 [0, 6]
    assert s.findAnagrams("abab", "ab") == []          # 正确应为 [0, 1, 2]
    print("反面演示 ✓ 本版因两处边界 bug 恒返回空列表")


# 踩坑记录
# 1. 【致命】切片右开区间：s[p1 : p1 + m - 1] 实际只取 m-1 个字符，
#    永远比 p 短一格，所以 list1 == cnt 一次都不成立 → 返回 []。
#    应写成 s[p1 : p1 + m]（左闭右开，右端是「起始 + 长度」）。
# 2. 【致命】循环边界用错：while p1 < m 里的 m 是 p 的长度，
#    但窗口是在 s 上滑动的，p1 的上限应该由 len(s) 决定（p1 + m <= n，即 p1 <= n - m）。
#    这里 p1 只从 0 滑到 2，连 s 都扫不全。
# 3. 这版复杂度 O(n·m log m)：每轮都要 sort(list(p)) + sort(list(窗口))，
#    n、m 到 3×10⁴ 时会超时（实测 33/65 后就 TLE）。正解见 v3 滑动窗口。
