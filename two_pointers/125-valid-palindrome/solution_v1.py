# LeetCode 125. 验证回文串（简单）
# 套路：对撞双指针 + 跳过非法字符，O(n) 时间 / O(1) 空间
# 2026-09-23
# 我的解答


class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()                       # 先统一小写，省掉后面逐字符比较时的大小写转换
        L = 0                               # 左指针
        R = len(s) - 1                      # 右指针 = 最大合法下标
        while L < R:
            # 左端不是「数字或小写字母」→ 跳过。continue 让本轮作废，回到 while 重新检查
            if not (48 <= ord(s[L]) <= 57 or 97 <= ord(s[L]) <= 122):
                L += 1
                continue
            # 右端同理（48-57 是 '0'-'9'，97-122 是 'a'-'z'，因为上面已经 lower 过了）
            if not (48 <= ord(s[R]) <= 57 or 97 <= ord(s[R]) <= 122):
                R -= 1
                continue
            # 走到这里说明两端都是合法字符，才允许比较
            if s[L] != s[R]:
                return False
            L += 1
            R -= 1
        return True                         # 空串 / 全非法字符 / 真回文都会落到这里


if __name__ == "__main__":
    sol = Solution()

    cases = [
        ("A man, a plan, a canal: Panama", True),   # 官方示例 1
        ("race a car", False),                      # 官方示例 2
        (" ", True),                                # 官方示例 3：去符号后是空串
        ("", True),                                 # 边界：空串
        ("a", True),                                # 边界：单字符
        (",", True),                                # 边界：单个非字母数字
        ("....", True),                             # 边界：全是非字母数字
        (",,a", True),                              # 连续两个非法字符（踩坑 3 的反例）
        ("!!!a", True),                             # 同上，换个符号
        ("a,,,a", True),                            # 两侧向中间收缩时空过一段符号
        ("ab_a", True),                             # 下划线算非字母数字，去掉后是 "aba"
        ("0P", False),                              # 经典反例：数字和小写比较，不相等
        ("ab", False),                              # 普通不回文
        ("Aa", True),                               # 大小写不敏感
    ]

    for src, want in cases:
        got = sol.isPalindrome(src)
        assert got == want, f"{src!r} 得到 {got}，期望 {want}"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【致命】`if ord(s[L]) not in range(48, 58) or range(97, 123):` 条件恒为真。
#    Python 的 or 把两侧当成彼此独立的条件：左边是 `not in range(...)`，右边是
#    `range(97, 123)`。range 对象非空，布尔值恒为 True，于是整个 if 永远成立
#    → 每轮 L 必 +1、R 必 -1，字符比较被完全跳过，官方示例 1 直接返回 false。
#    更隐蔽的变体：`not in range(48,58) or not in range(97,123)` 同样恒真 ——
#    一个字符不可能同时落在两个区间里，「不在 A 区」和「不在 B 区」至少一个为真。
#    正确写法要用 and（德摩根定律），或像我最后这样用数学区间 `48 <= o <= 57`。
# 2. 【致命】`s = lower()` 漏了 `s.`。lower 不是内置函数，直接 NameError；
#    而且字符串不可变，`s.lower()` 只返回新串，必须写成 `s = s.lower()` 接回来，
#    否则大小写没换，'A' 永远匹配不上 'a'。
# 3. 【致命】跳过非法字符后没有 continue。看 ",,a" 的执行过程：
#       L=0, R=2 → s[0] 是逗号，L += 1 变成 1
#       → 立刻执行比较 s[1] vs s[2]，即 ',' vs 'a' → 不等 → 误判 False
#    问题在于 L 刚挪到 1，而 s[1] 也是逗号、还没被检查过，就被当成有效字符拿去比了。
#    if 一次只能跳一格，遇到「连续两个非法字符」就会漏检。
#    实测对比 14 个用例，不带 continue 的版本挂掉 3 个（官方示例 1、",,a"、"!!!a"）。
#    根因一句话：指针移动之后，不能立刻用新指针做判断。
#    两种等效修法：① if + continue（一次跳一格，跳完回头重看）
#                  ② 内层 while 一次性跳到干净（见 solution_v2.py 的思路）
# 4. 【环境】LeetCode 报 `SyntaxError: invalid syntax`，但这一行语法其实完全合法
#    （本地 compile 验证通过，且不含任何非 ASCII 字符）。根因是粘贴代码时混入了
#    肉眼看不见的异体字符（全角括号 / 全角冒号 / 零宽空格）。
#    区分报错类型：`invalid character '（' (U+FF08)` 是异体字符；
#    `invalid syntax` 多为括号不配对或不可见字符。
#    最有效的解法：把整行删掉，切到英文输入法重新手打一遍。
# 5. 【写法建议】长布尔表达式建议拆成变量并给每段加括号，例如
#       o = ord(s[L]); is_alnum = (48 <= o <= 57) or (97 <= o <= 122)
#    可读性更好，也更容易一眼看出括号有没有配对。
# 6. 【复杂度】时间 O(n)（不回文时也必须扫完整个字符串，Ω(n) 是下界），
#    空间 O(1)（只有 L、R 两个下标变量）。这题在复杂度上已经到顶，
#    不存在时间或空间更优的解 —— 只有常数级更快的写法（见 solution_v3.py）。
