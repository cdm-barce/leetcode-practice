# LeetCode 392. 判断子序列（简单）
# 套路：双指针（本版为有 bug 的初版，边界与 return 逻辑错误，作反面教材）
# 2026-09-24
# 我的解答（WA 版本）

# 原始版本（复现当时的错误，便于复盘）：
#   while p1 < n1:
#       if s[p1] == t[p2]:
#           p1 += 1
#       p2 += 1
#       if p2 >= len(t):
#           return True
# 这个版本有两处问题，见文件末尾「踩坑记录」。


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # 复现原始 bug 版本，方便跑出它真实的错误行为
        n1 = len(s)
        p1 = 0
        p2 = 0
        while p1 < n1:
            if s[p1] == t[p2]:          # 越界点：p2 可能已经 == len(t)
                p1 += 1
            p2 += 1
            if p2 >= len(t):            # 逻辑错：把「t 扫完」当成了成功
                return True
        return False


if __name__ == "__main__":
    sol = Solution()
    # 本版是 WA 版本：assert 断言它「实际会输出的错误结果」，再用 print 点出正确值
    assert sol.isSubsequence("abc", "ahbgdc") is True    # 官方示例 1，凑巧能过
    # 官方示例 2 会触发越界（IndexError），这里不做断言，仅文字说明：
    #   sol.isSubsequence("axc", "ahbgdc") -> IndexError: string index out of range
    print("反面演示 ✓ 官方示例 1 凑巧 True；示例 2 会 IndexError，答案应为 False")

# 踩坑记录：
# 1. 【致命·越界】`while p1 < n1` 只约束了 p1，没有约束 p2；而 p2 每轮无条件 +1，
#    比 p1 跑得快。当 t 被扫完（p2 == len(t)）而 s 还没匹配完时，循环条件仍成立，
#    下一轮进入循环体访问 t[p2] 就越界。反例：s="axc", t="ahbgdc"。
#    根因：第 5 行 `t[p2]` 执行前，没有任何一条语句保证 p2 < len(t)。
# 2. 【致命·逻辑】`if p2 >= len(t): return True` 把「t 用完了」当成了成功。
#    但 t 用完意味着再也提供不了新字符，此时若 s 还没匹配完，正确结果应是 False。
#    判断成功应该看「p1 是否走到 n1」（s 的所有字符都按顺序找到了），
#    而「p2 到头」是判失败的一端。终止条件被误当成了成功条件。
# 3. 【易误读】`while ... else:` 在没有 break 的循环里永远执行，等价于卸载循环后面。
#    这里没害处，但容易误读成「循环正常结束才执行」。以后见到 while/else 先想有没有 break。
# 4. 【知识点】双指针判断子序列是标准解：p1 读 s、p2 读 t，字符相等 p1/p2 同进，
#    否则只 p2 进。时间 O(n+m)，空间 O(1)，单次查询已是最优。
#    进阶场景（大量 s、同一个 t）见 solution_v3.py：位置表 + 二分。
