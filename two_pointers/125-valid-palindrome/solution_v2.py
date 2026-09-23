# LeetCode 125. 验证回文串（简单）
# 套路：对撞双指针 + str.isalnum() 跳过非法字符，O(n) 时间 / O(1) 空间
# 2026-09-23
# 最优代码


class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()                       # 统一小写
        L, R = 0, len(s) - 1
        while L < R:
            if not s[L].isalnum():          # 左端不是字母/数字 → 跳过
                L += 1
                continue                    # 指针动了就重来，绝不带着「未检查的位置」往下比较
            if not s[R].isalnum():          # 右端同理
                R -= 1
                continue
            if s[L] != s[R]:                # 两端都是合法字符了，可以放心比
                return False
            L += 1
            R -= 1
        return True


if __name__ == "__main__":
    sol = Solution()

    cases = [
        ("A man, a plan, a canal: Panama", True),   # 官方示例 1
        ("race a car", False),                      # 官方示例 2
        (" ", True),                                # 官方示例 3
        ("", True),                                 # 边界：空串
        ("a", True),                                # 边界：单字符
        (",", True),                                # 边界：单个非字母数字
        ("....", True),                             # 边界：全是非字母数字
        (",,a", True),                              # 连续两个非法字符
        ("!!!a", True),                             # 同上，换个符号
        ("a,,,a", True),                            # 两侧向中间收缩时空过一段符号
        ("ab_a", True),                             # 下划线不是字母数字，去掉后是 "aba"
        ("0P", False),                              # 经典反例：数字 vs 小写字母
        ("ab", False),
        ("Aa", True),
    ]

    for src, want in cases:
        got = sol.isPalindrome(src)
        assert got == want, f"{src!r} 得到 {got}，期望 {want}"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【isalnum 的 Unicode 陷阱】Python 的 str.isalnum() 认的是「所有 Unicode 字母数字」，
#    不只是 ASCII。实测：'中'.isalnum() → True，'一'.isalnum() → True，
#    '²'.isalnum() → True（上标数字也算），但 '_'.isalnum() → False（下划线不算）。
#    本题明确限定「s 仅由可打印的 ASCII 字符组成」，所以用 isalnum() 是安全的；
#    但如果以后遇到允许中文输入的题，'中' 会被当成合法字符留下，答案就错了，
#    那种场景必须老老实实写 `48 <= ord(c) <= 57 or 97 <= ord(c) <= 122`（见 solution_v1.py）。
# 2. 【内层 while 等效写法】不用 continue 也能写对，前提是「一次跳到干净为止」：
#       while L < R and not s[L].isalnum():
#           L += 1
#       while L < R and not s[R].isalnum():
#           R -= 1
#       if s[L] != s[R]: return False
#    本质和 if + continue 是同一个意思：把「挪指针」和「比较字符」严格分成两个阶段。
#    内层循环必须带 `L < R` 边界保护，否则 L 会冲出字符串范围。
# 3. 【为什么这版是算法最优】时间 O(n)、空间 O(1)，两条都踩在下界上：
#    不回文时也要扫完整个字符串，所以 Ω(n) 无法突破；空间只需要两个下标变量。
#    这题在复杂度层面没有更优解，剩下的只有常数级优化（见 solution_v3.py）。
