# LeetCode 5. 最长回文子串（中等）
# 套路：枚举所有子串 + 切片反转判断回文，O(n³) 时间 / O(n) 空间 —— 能过但极慢
# 2026-09-22
# 我的解答（暴力版：144/144 通过，耗时 9375 ms，击败 4.97%）


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:                          # 长度 0 或 1，本身就是回文，直接返回
            return s

        seen = {}                               # {回文子串长度: 子串本身}
        for left in range(len(s) - 1):          # 枚举每个起点
            right = len(s) - 1                  # ← 必须写在 for 里面：每换一个 left 都要重置
            while right > left:                 # right > left ⇒ 子串长度至少为 2
                s0 = s[left:right + 1]          # 取出 [left, right] 这一段
                if s0[::-1] == s0:              # 反转后仍相等 ⇒ 是回文
                    seen[len(s0)] = s0
                right -= 1                      # 右端不断左移，枚举所有以 left 开头的子串

        # 兜底：整串里不存在长度 ≥ 2 的回文时（如 "ac"），seen 是空的，
        # 此时 max(seen) 会抛 ValueError。而单个字符本身一定回文，返回 s[0] 即可。
        if not seen:
            return s[0]                         # 题目保证 s 非空，所以 s[0] 一定存在

        return seen[max(seen)]                  # 以子串长度为 key，取最长的那个


if __name__ == "__main__":
    sol = Solution()

    # 注意：本题答案不唯一（special judge）。下面断言的是「本实现实际输出的那一个」，
    # 括号里注明另一个同样合法的答案。
    assert sol.longestPalindrome("babad") == "aba", "另一个合法答案是 bab"
    assert sol.longestPalindrome("cbbd") == "bb", "唯一解"
    assert sol.longestPalindrome("abcba") == "abcba", "整串就是回文"
    assert sol.longestPalindrome("aabca") == "aa", "最长的回文是 aa"
    assert sol.longestPalindrome("abacaba") == "abacaba", "整串就是回文"
    assert sol.longestPalindrome("aaaa") == "aaaa", "全相同字符"
    assert sol.longestPalindrome("aa") == "aa", "偶数长度边界"
    assert sol.longestPalindrome("ac") == "a", "没有任何长度≥2的回文，走兜底"
    assert sol.longestPalindrome("ab") == "a", "同上"
    assert sol.longestPalindrome("a") == "a", "单字符"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【泛型别名陷阱，最坑的一个】一开始写的是 `if list[::-1] == s0:`，本意是「反转 s0」，
#    但 `list` 是 Python 的内置类型，不是变量。更反直觉的是它**不报错** ——
#    Python 3.9+ 里 list[...] 走的是 __class_getitem__（泛型别名语法），切片照收不误，
#    返回一个 types.GenericAlias 对象（repr 是 `list[slice(None, None, -1)]`）。
#    拿它去和字符串比，结果恒为 False ⇒ seen 永远是空字典 ⇒ return seen[max(seen)]
#    报 ValueError: max() iterable argument is empty。
#    → 教训：切片反转的主语必须是那个字符串变量本身，写成 s0[::-1]。
#    → 附带教训：max() 报 "iterable is empty" 时，真正的问题几乎总在「上游没往容器里放东西」，
#      不要去研究 max，要往上游找「赋值语句为什么没执行」。
# 2. 【变量作用域】`right = len(s) - 1` 一开始写在了 for 外面，只初始化一次。
#    于是 left = 0 那轮把 right 一路减到 0，从 left = 1 开始 while 条件 `0 > 1` 直接为假，
#    内层循环一次都不进 —— 实际只检查了「以首字符开头」的子串。
# 3. 【边界缺失】内层 while 是 `right > left`，保证子串长度 ≥ 2，
#    所以长度 1 的子串从来没被枚举过。当输入是 "ac" / "ab" 这种没有任何长度 ≥ 2 回文的串时，
#    seen 为空 ⇒ 崩。必须单独兜底：单字符本身就是回文。
#    LeetCode 提交时 3/144 就挂在这里，而题目给的两个示例恰好都有长度 ≥ 2 的解，
#    所以「示例全绿」完全不等于正确 —— 一定要自己补边界用例。
# 4. 【复杂度】两层循环 O(n²) 个子串，每个子串还要 O(n) 做切片+反转+比较 ⇒ O(n³)。
#    n 上限 1000 时实测 9375 ms，击败 4.97% —— 能过纯粹是因为时限宽松。
# 5. 正确做法见 solution_v2.py：中心扩展，O(n²) 时间 / O(1) 空间，实测 45 ms。
