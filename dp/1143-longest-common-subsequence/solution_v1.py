# LeetCode 1143. 最长公共子序列（中等）
# 套路：二维 DP，dp[i][j] 表示两个前缀之间的 LCS，O(m·n) 时间 / O(m·n) 空间
# 2026-11-18
# 参考解法（本次是主动求助讲解后整理，非本人独立提交）


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        :param text1: 第一个字符串，仅含小写字母，长度 1..1000
        :param text2: 第二个字符串，仅含小写字母，长度 1..1000
        :return: 最长公共子序列的长度；没有公共子序列时返回 0

        为什么不能用双指针 / 滑动窗口：
        子序列允许跳过中间的字符，窗口的右边界无论怎么滑，
        都无法判断"这个字符该不该跳过"（跳过可能是对的，也可能是错的）。
        只有把"两个前缀之间"的所有答案缓存下来，才能避免同一个子问题反复重算。

        状态定义：dp[i][j] = text1 的**前 i 个字符** 与 text2 的**前 j 个字符**
                            的最长公共子序列长度。
        注意是"前 i 个"（下标 0..i-1），所以真正参与比较的末位是 text1[i-1]。
        数组多开一行一列，让 i=0 / j=0 表示空串，值自然是 0，
        这样就不用在下标 0 处写一堆边界特判。

        转移只取决于两个末位字符相不相等：
        - 相等 → 这对字符一定能进答案，接在"双方各去掉末位"的最优解后面
        - 不等 → 它们不可能同时出现在 LCS 末尾，至少有一边的末位要扔掉
        """
        m, n = len(text1), len(text2)

        # (m+1) x (n+1) 的表格，第 0 行 / 第 0 列代表"空串"，全 0 即初值
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    # 末位字符相等：把它接在"左上角"那个子问题的最优解后面。
                    # 这里不必再和 dp[i-1][j]、dp[i][j-1] 取 max：
                    # 数学上恒有 dp[i-1][j] <= dp[i-1][j-1] + 1，
                    # 所以左上角加一已经是三者中的最大值。
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    # 末位不等：这两个字符不可能同时是 LCS 的最后一个字符，
                    # 于是至少能丢掉一边 —— 丢掉 text1 的末位（看上边），
                    # 或丢掉 text2 的末位（看左边），哪个损失小取哪个。
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    assert s.longestCommonSubsequence("abcde", "ace") == 3, "示例1：LCS 是 ace"
    assert s.longestCommonSubsequence("abc", "abc") == 3, "示例2：完全相同"
    assert s.longestCommonSubsequence("abc", "def") == 0, "示例3：无公共子序列"

    # 边界用例
    assert s.longestCommonSubsequence("a", "a") == 1, "单字符相等"
    assert s.longestCommonSubsequence("a", "b") == 0, "单字符不等"
    assert s.longestCommonSubsequence("a", "ba") == 1, "一边是另一边的后缀"
    assert s.longestCommonSubsequence("abc", "cba") == 1, "顺序相反，只能取 1 个"
    assert s.longestCommonSubsequence("aaaa", "aa") == 2, "重复字符，取短的"

    # 官方样例里的长串：验证表填得对
    assert s.longestCommonSubsequence("bsbininm", "jmjkbkjkv") == 1, "长串官方用例"

    # 陷阱用例：容易把"子序列"误当"子串"——答案是 2（"ac"），不是 1（"a"）
    assert s.longestCommonSubsequence("ace", "abcde") == 3, "反过来也算，顺序无关"
    assert s.longestCommonSubsequence("abcde", "ae") == 2, "'ae' 是子序列（跳过 b、c、d）"
    assert s.longestCommonSubsequence("cab", "ab") == 2, "跳过开头的 c"

    # ---------- 与暴力对拍（枚举 text1 的全部子序列，2^m 种） ----------
    def is_subsequence(sub, t):
        """双指针判断 sub 是不是 t 的子序列"""
        k = 0
        for ch in t:
            if k < len(sub) and sub[k] == ch:
                k += 1
        return k == len(sub)

    def brute(t1, t2):
        best = 0
        for mask in range(1 << len(t1)):
            sub = "".join(t1[i] for i in range(len(t1)) if mask >> i & 1)
            if len(sub) > best and is_subsequence(sub, t2):
                best = len(sub)
        return best

    import random
    random.seed(1143)
    for _ in range(500):
        a = "".join(random.choice("abc") for _ in range(random.randint(1, 8)))
        b = "".join(random.choice("abc") for _ in range(random.randint(1, 8)))
        assert s.longestCommonSubsequence(a, b) == brute(a, b), f"与暴力解不一致：{a} / {b}"

    print("全部用例通过 ✓（含 500 组暴力对拍）")


# 踩坑记录
# 【说明】这题是天宇主动求助讲解后整理的，下面不是实际报错日志，
# 而是讲解过程中确认过的高频误区，写下来当作自查清单。
#
# 1. 【最大坑：下标偏移】dp[i][j] 里的 i、j 是"前 i 个字符"的计数，
#    不是字符下标。比较时必须写 text1[i-1] == text2[j-1]。
#    写成 text1[i] 时，i 最大取到 m，会直接 IndexError；
#    就算不越界，逻辑上也整体错位了一格。
#
# 2. 【"子序列"≠"子串"】子序列可以跳过中间字符（ace 是 abcde 的子序列），
#    子串必须连续（bcd 才是）。所以这题不能用双指针 / 滑动窗口，
#    也不能套"最长公共子串"的转移（那题 dp[i][j] 必须以 i、j 结尾，
#    不等时直接置 0，答案也不是 dp[m][n] 而是全表最大值）。
#
# 3. 【不等时不要漏掉 max】只写 dp[i][j] = dp[i-1][j] 或只写 dp[i][j-1]
#    都不对，必须两者的较大值。因为无法预知丢哪一边更划算。
#
# 4. 【相等时用不用再取 max】用不着。恒有 dp[i-1][j] <= dp[i-1][j-1] + 1，
#    所以直接取 dp[i-1][j-1] + 1 就是三者最大值。
#    写成 max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1] + 1) 结果也对，只是多余。
#
# 5. 【第 0 行 / 第 0 列为什么是 0】它们代表"其中一方是空串"，
#    空串和任何串的 LCS 长度都是 0。这是递推的底座，不能省。
#
# 6. 【复杂度】1000 x 1000 = 10^6 格，每格 O(1)，Python 约 0.3~0.6s 能过。
#    空间可以压到 O(n)，见 solution_v2.py 的滚动数组写法。
#
# 7. 【这题是 DP 母题】后面的变体都是在同一张表上换规则：
#    72 编辑距离（max 改 min，加三个来源）、516 最长回文子序列
#    （text2 取 text1 的逆序）、583 两个字符串的删除操作（m + n - 2*LCS）、
#    1035 不相交的线（与本题完全等价）。
