# LeetCode 392. 判断子序列（简单）
# 套路：双指针（修正版），O(n+m) 时间 / O(1) 空间
# 2026-09-24
# 我的解答（正确版）


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        p1 = 0                              # 读 s 的指针
        p2 = 0                              # 读 t 的指针
        n1, n2 = len(s), len(t)

        # 两个边界都塞进循环条件：p2 也有停下来的理由，不再靠循环体事后补救
        while p1 < n1 and p2 < n2:
            if s[p1] == t[p2]:              # 匹配成功：两指针同进
                p1 += 1
            p2 += 1                         # 不管匹不匹配，t 都要继续往后扫

        # 循环能结束只有两种可能：① s 匹配完(p1==n1) ② t 扫完(p2==n2)。
        # 只需在出口判断「s 是否匹配完」这一种，另一种自然就是 False。
        return p1 == n1


if __name__ == "__main__":
    sol = Solution()

    cases = [
        ("abc", "ahbgdc", True),            # 官方示例 1
        ("axc", "ahbgdc", False),           # 官方示例 2（v1 在此越界）
        ("", "ahbgdc", True),               # 空 s 必为子序列
        ("abc", "", False),                 # t 为空、s 非空
        ("", "", True),                     # 双双为空
        ("b", "abc", True),                 # 单字符、在中间
        ("acb", "ahbgdc", False),           # 顺序错误：b 出现在 c 之前
        ("aaaa", "a", False),               # s 比 t 长
    ]

    for src, target, want in cases:
        got = sol.isSubsequence(src, target)
        assert got == want, f"{src!r} in {target!r} 得到 {got}，期望 {want}"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 相比 v1 的两处改动：① 循环条件补上 `p2 < n2`，p2 也有了自己的边界，越界根除；
#    ② 把 return 挪到循环外，用 `return p1 == n1` 一行判定成功，
#       成功条件从「t 用完」纠正为「s 匹配完」。
# 2. `if ... : return True else: return False` 可简化为 `return p1 == n1`，
#    比较表达式本身就是 bool，直接返回。
# 3. 复杂度：时间 O(n+m)（最坏 s、t 都要扫到底），空间 O(1)。
#    单次查询下这是最优解；进阶「大量 s、同一 t」见 solution_v3.py 的位置表 + 二分。
