# LeetCode 1143. 最长公共子序列（中等）
# 套路：一维滚动数组，dp[j] 原地复用上一行的值，O(m·n) 时间 / O(n) 空间
# 2026-11-18
# 最优代码


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        :param text1: 第一个字符串，仅含小写字母
        :param text2: 第二个字符串，仅含小写字母
        :return: 最长公共子序列的长度

        二维版里 dp[i][j] 只依赖三个位置：左边 dp[i][j-1]、上边 dp[i-1][j]、
        左上角 dp[i-1][j-1]。也就是说整张表里，**只有"上一行"和"本行已算出的部分"有用**，
        再往上的行永远用不到了 —— 所以可以把整张表压成一行。

        压缩后 dp[j] 是"一个会被覆盖的槽位"，读它之前必须想清楚
        此刻它代表的是上边还是左边：
        - 更新前：dp[j] 还留着上一行的值 → 代表 dp[i-1][j]（上边）
        - 更新后：dp[j] 已经是本行的值 → 供 j+1 轮当"左边"用（dp[i][j]）
        - 左上角 dp[i-1][j-1] 会被 dp[j-1] 的覆盖动作抹掉，所以要单独存一个变量。
        """
        m, n = len(text1), len(text2)

        # 只有一行：长度为 n+1，下标 0 是"空串"那一列，恒为 0
        # 外层循环开始前，它等价于二维表的第 0 行
        dp = [0] * (n + 1)

        for i in range(1, m + 1):
            # prev_diag 扮演 dp[i-1][j-1]。每行开头 j=1 时，
            # "左上角" 落在第 0 列（空串），值为 0，所以必须重置
            prev_diag = 0

            for j in range(1, n + 1):
                # 先抢救：此刻 dp[j] 还没被本行覆盖，它就是上边的 dp[i-1][j]
                cur = dp[j]

                if text1[i - 1] == text2[j - 1]:
                    # 左上角 + 1（左上角存在 prev_diag 里，早就被覆盖走了）
                    dp[j] = prev_diag + 1
                else:
                    # dp[j] 是上边（未覆盖前的值），dp[j-1] 是左边（本行刚算好）
                    dp[j] = max(dp[j], dp[j - 1])

                # 本轮的"上边"值，到下一列就变成"左上角"
                prev_diag = cur

        return dp[n]


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    assert s.longestCommonSubsequence("abcde", "ace") == 3, "示例1"
    assert s.longestCommonSubsequence("abc", "abc") == 3, "示例2"
    assert s.longestCommonSubsequence("abc", "def") == 0, "示例3"

    # 边界
    assert s.longestCommonSubsequence("a", "a") == 1
    assert s.longestCommonSubsequence("a", "b") == 0
    assert s.longestCommonSubsequence("aaaa", "aa") == 2, "重复字符"
    assert s.longestCommonSubsequence("abc", "cba") == 1, "顺序相反"
    assert s.longestCommonSubsequence("bsbininm", "jmjkbkjkv") == 1, "长串官方用例"

    # ---------- 与二维版对拍（一维版写错时最容易出的是"串行污染"） ----------
    def dp_2d(t1, t2):
        """二维参考实现：逻辑直白，用它当标尺"""
        r, c = len(t1), len(t2)
        table = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(1, r + 1):
            for j in range(1, c + 1):
                if t1[i - 1] == t2[j - 1]:
                    table[i][j] = table[i - 1][j - 1] + 1
                else:
                    table[i][j] = max(table[i - 1][j], table[i][j - 1])
        return table[r][c]

    import random
    random.seed(1143)
    for _ in range(500):
        a = "".join(random.choice("abcd") for _ in range(random.randint(1, 12)))
        b = "".join(random.choice("abcd") for _ in range(random.randint(1, 12)))
        assert s.longestCommonSubsequence(a, b) == dp_2d(a, b), f"与二维版不一致：{a} / {b}"

    # 极端尺寸：一边长度 1，一边长度 1000，验证下标没越界
    long_str = "a" + "b" * 999
    assert s.longestCommonSubsequence("b", long_str) == 1
    assert s.longestCommonSubsequence(long_str, "a") == 1

    print("全部用例通过 ✓（含 500 组二维版对拍）")


# 踩坑记录
# 【说明】本题为求助讲解后整理，以下为滚动数组写法的高频错误自查清单。
#
# 1. 【prev_diag 忘记每行重置】它必须写在外层循环**内部**、内层循环**之前**。
#    放到外层循环外面的话，第一行结束后它还残留着上一行的值，
#    第二行 j=1 就会拿到错误的数据。
#
# 2. 【顺序搞反：先算 dp[j] 再读 dp[j]】必须先把旧值存进 cur，
#    否则覆盖之后拿不到 dp[i-1][j]（上边）。这是滚动数组最容易静默出错的地方 ——
#    代码能跑、样例可能都过，只有长串才暴露出偏差，所以务必用对拍验证。
#
# 3. 【upper 和 left 认错】dp[j]（未覆盖时）是上边，dp[j-1] 是左边。
#    写成一维后没有 i、j 两个下标提示，很容易下意识把 dp[j-1] 当上边。
#
# 4. 【left 用 prev_diag 顶替】典型错误写法是 dp[j] = dp[j-1] + 1，
#    这用的是"左边"而不是"左上角"，结果会偏大。
#
# 5. 【空间其实只降到 O(n)】不是 O(1)。外层循环仍要 m 轮，
#    只是内层不再存整张表。想进一步省，可以让 text2 取较短的那个
#    （dp 数组长度只跟内层字符串有关）—— 交换参数不影响答案。
#
# 6. 【不推荐为了省空间牺牲可读性】面试/比赛里先写二维版说明白思路，
#    再提"可以压成一维"作为加分项。一维版是优化，不是主线。
