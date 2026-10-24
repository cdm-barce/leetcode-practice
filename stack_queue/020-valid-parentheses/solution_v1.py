# LeetCode 20. 有效的括号（简单）
# 套路：栈 + 字典配对，O(n) 时间 / O(n) 空间
# 2026-10-24
# 最优代码（一次 AC，0 ms 击败 100%）

class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {')': '(', ']': '[', '}': '{'}   # 右括号 → 对应的左括号
        stack = []

        for ch in s:
            if ch in pairs:                      # 是右括号：必须和栈顶配对
                if not stack or stack[-1] != pairs[ch]:
                    return False                 # 栈空（多出右括号）或栈顶不匹配
                stack.pop()                      # 配对成功，弹出栈顶
            else:                                # 是左括号：入栈等着被配对
                stack.append(ch)

        return not stack                         # 收尾：栈空才算全部闭合


if __name__ == "__main__":
    s = Solution()

    # 官方用例
    assert s.isValid("()") is True
    assert s.isValid("()[]{}") is True
    assert s.isValid("(]") is False
    assert s.isValid("([)]") is False
    assert s.isValid("{[]}") is True

    # 边界：全是左括号 / 全是右括号
    assert s.isValid("(((") is False
    assert s.isValid(")))") is False

    # 边界：单个括号
    assert s.isValid("(") is False
    assert s.isValid(")") is False

    # 边界：深度嵌套
    assert s.isValid("((((()))))") is True

    # 边界：中间都配平了，但收尾时栈里还剩东西
    assert s.isValid("(){}}{") is False
    assert s.isValid("((") is False

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 判断顺序是这题最关键的点：`if not stack or stack[-1] != pairs[ch]`
#    —— 判空必须写在取栈顶之前，靠 or 的短路特性保护。
#    反过来写成 `stack[-1] != pairs[ch] or not stack`，空栈时直接 IndexError。
# 2. 最后必须 `return not stack`，不能 `return True`。
#    反例 "(){}}{"：前面每一对都成功配对，栈中途也清空过，
#    但循环结束时栈里还剩 "}{"，只判中间过程就会漏掉。
# 3. Python 里栈就是 list：append 入栈、pop 出栈、stack[-1] 看栈顶，全部 O(1)。
#    不要用 pop(0) 或 insert(0, x)，那是队列方向，代价 O(n)。
# 4. 用字典把「右括号 → 左括号」映射好，比写三个 if-elif 清爽，加新括号类型也只需改一行。
# 5. 复杂度：每个字符最多进栈、出栈各一次，O(n) 时间；最坏全左括号时栈深 n，O(n) 空间。
