# LeetCode 5. 最长回文子串（中等）
# 套路：中心扩展 —— 枚举 2n-1 个中心向两侧扩，O(n²) 时间 / O(1) 额外空间
# 2026-09-22
# 最优代码


class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        best = ""                               # 到目前为止最长的回文

        for i in range(n):                      # 每个下标当一次「中心锚点」
            # ① 奇数长度：s[i] 自己是中心，从它两侧起步
            odd = self.expand(s, i - 1, i + 1)
            # ② 偶数长度：中心落在 s[i] 和 s[i + 1] 之间的「缝」上
            even = self.expand(s, i, i + 1)
            # ③ 三个候选一起比长度 —— best 必须参与，否则每轮都会被覆盖掉
            best = max(best, odd, even, key=len)

        return best

    def expand(self, s: str, L: int, R: int) -> str:
        # 左没越界 + 右没越界 + 两端字符相同 ⇒ 继续往外扩
        while L >= 0 and R < len(s) and s[L] == s[R]:
            L -= 1
            R += 1
        # 循环是「先判断、再移动」，所以退出时 L 已越过回文左端 1 格，R 也越过了右端 1 格。
        # 而切片右端本来就不含，因此左端补 1、右端直接写 R，两个 1 正好抵消。
        return s[L + 1:R]


if __name__ == "__main__":
    sol = Solution()

    # 本题答案不唯一（special judge）：断言写本实现的实际输出，另注合法替身。
    assert sol.longestPalindrome("babad") == "bab", "另一个合法答案是 aba"
    assert sol.longestPalindrome("cbbd") == "bb", "唯一解"
    assert sol.longestPalindrome("abcba") == "abcba", "整串就是回文（奇数长度中心）"
    assert sol.longestPalindrome("abacaba") == "abacaba", "整串就是回文"
    assert sol.longestPalindrome("aabca") == "aa", "版本演进中的中间版会在这里答错成 aabca（见踩坑 5）"
    assert sol.longestPalindrome("aa") == "aa", "偶数长度，靠双字符中心"
    assert sol.longestPalindrome("aaaa") == "aaaa", "全相同字符"
    assert sol.longestPalindrome("aacabdkacaa") == "aca", "两个同长回文，取任意一个"
    assert sol.longestPalindrome("ac") == "a", "没有任何长度≥2的回文"
    assert sol.longestPalindrome("ab") == "a", "同上"
    assert sol.longestPalindrome("a") == "a", "单字符"
    assert sol.longestPalindrome("a" * 1000) == "a" * 1000, "最坏情况：1000 个 a"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【best 被覆盖，最难发现的一个】写成了
#        best = odd if len(odd) > len(even) else even
#    这一行只在「odd 和 even 之间」挑，等号右边**根本没有出现 best**，
#    于是每一轮都把前面攒下的成果无条件丢掉，循环结束时 best 里只剩下
#    最后一个中心（i = n-1）扩出来的东西。实测指纹非常明显：
#        "babad" → 'd'、"cbbd" → 'd'、"abcba" → 'a'
#    —— 答案永远落在字符串末尾附近，就是这个 bug 的特征。
#    → 正确写法是让 best 也参加比较：max(best, odd, even, key=len)。
#    → 教训：写 `x = ...` 这种「累加/累积」语义的语句时，先检查等号右边有没有 x 自己。
# 2. 【作用域】expand 里如果直接写 `R < n` 会抛 NameError: name 'n' is not defined ——
#    n 是 longestPalindrome 的局部变量，另一个方法看不到它。要么写 len(s)，要么把 n 传进来。
# 3. 【off-by-one】`return s[L + 1:R]` 里的不对称边界：左端要 +1、右端不用 -1。
#    想不通就画一次 "abcba"、中心 i=2 的推演：L 从 1 走到 -1，R 从 3 走到 5，
#    真正的回文是 s[0:5]，恰好等于 s[L+1:R]。长度也可以用 R - L - 1 算。
# 4. 【while 的三个条件顺序】把两个边界判断放在 s[L] == s[R] 前面，靠 and 的短路特性
#    保证越界时不会去取 s[L] / s[R]，既省一次下标运算又避免索引越界。
# 5. 【为什么不相等必须停】v2 之前的中间版本把 R += 1 / L -= 1 写在了 if 外面，
#    于是「这一对不相等」时还在继续往外扩，会跳过中间不匹配的字符、在外层碰上恰好相等的一对，
#    从而把假回文记下来。实测 "aabca" 会返回 'aabca'（正确答案是 "aa"）。
#    → 回文要求**每一对**都对称，只要有一对不等，更长的子串就全都不是回文，必须立刻停止。
# 6. 【复杂度对比】v1 枚举所有子串 O(n³)，n=1000 实测 9375 ms（击败 4.97%）；
#    本版枚举 2n-1 个中心、每个最多扩 n/2 步 ⇒ O(n²)，同样 n=1000 实测 45 ms，快 200 多倍。
#    关键差别：扩展时每一步只比较**一对新字符**，不像 v1 那样把整个子串重新反转验证一遍。
# 7. 【中心为什么是 2n-1 个】奇数长度回文的中心是一个字符（n 个），
#    偶数长度回文的中心落在两个字符之间（n-1 个），合起来 2n-1 个，一个不漏。
#    只枚举单字符中心会漏掉所有偶数长度回文 —— 当时 "cbbd" / "aa" 就是这么崩的。
