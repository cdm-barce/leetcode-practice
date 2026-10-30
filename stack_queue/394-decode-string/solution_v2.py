# LeetCode 394. 字符串解码（中等）
# 套路：双状态栈 —— 栈里存 (倍数, 外层已拼好的前缀) 元组，遇 [ 存现场、遇 ] 恢复现场
# 2026-10-30
# 最优代码，O(n) 时间 / O(n) 空间

class Solution:
    def decodeString(self, s: str) -> str:
        stack = []          # 元素形如 (倍数 k, 进栈那一刻的外层前缀)
        cur = ""            # 当前这一层正在拼的字符串
        num = 0             # 当前累积的倍数（可能是多位数）

        for ch in s:
            if ch.isdigit():
                # 累积成多位数：'12' 要变成 12，不能只看单个字符
                num = num * 10 + int(ch)
            elif ch == '[':
                # 存现场：把外层的倍数和前缀一起压栈，然后从零开始拼内层
                stack.append((num, cur))
                num, cur = 0, ""
            elif ch == ']':
                # 恢复现场：弹出外层的倍数和前缀
                k, prev = stack.pop()
                # 内层结果重复 k 次，接在外层前缀后面（前缀在前，顺序不能反）
                cur = prev + k * cur
                num = 0
            else:
                cur = cur + ch      # 普通字母直接追加到当前层

        return cur                  # 遍历结束时 cur 就是完整结果


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1
    assert s.decodeString("3[a]2[bc]") == "aaabcbc"

    # 官方示例 2：两层嵌套
    assert s.decodeString("3[a2[c]]") == "accaccacc"

    # 官方示例 3：多段并列 + 尾部裸字母
    assert s.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"

    # 边界：没有编码，原样返回
    assert s.decodeString("abc") == "abc"

    # 边界：多位数
    assert s.decodeString("12[a]") == "a" * 12
    assert s.decodeString("10[b]") == "b" * 10

    # 边界：三层嵌套
    assert s.decodeString("2[2[2[a]]]") == "a" * 8

    # 边界：倍数为 1
    assert s.decodeString("1[a]") == "a"

    # 边界：单字符
    assert s.decodeString("x") == "x"

    # 边界：嵌套里带多位数
    assert s.decodeString("2[ab3[c]]") == "abcccabccc"

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心心智模型：把 [ ] 看成函数调用。
#    '[' 相当于「进入子函数」——先把上下文（num、cur）压栈保存，再用全新的变量干活；
#    ']' 相当于「return」——把内层结果乘倍数后接回外层的 cur。
#    所以 cur 在任何时刻**只代表它所在那一层**，不包含外层内容。
# 2. num 的累积必须写成 num * 10 + int(ch)。多位数是这题的第一个陷阱：
#    '12[a]' 里的 12 是两位数，逐位累积才能得到 12。
# 3. '[' 那两支赋值必须成对：`num, cur = 0, ""`。只清一个会导致内层内容混进外层，
#    实测如果不清 cur，'3[a2[c]]' 会算成 'aacacaacacaacac'（外层 'a' 被重复计算）。
# 4. ']' 拼接顺序：`prev + k * cur`，前缀必须在前。
#    写成 `k * cur + prev` 的话 '2[a]b' 会变成 'baa'。
# 5. ']' 里的 `num = 0` 严格说不是必需的（'[' 时已清零），但写上更防御，
#    也让人读起来知道「这一层结束了，倍数归零」。
# 6. 栈里存元组而不是开两个栈，好处是弹一次就同时拿到两样，不容易错位。
# 7. 与 LC20（有效括号）同族：都是「遇左括号压栈、遇右括号出栈」，
#    区别是这题除了配对，还要在栈里保存**两个**业务状态。
# 8. 复杂度：每个字符处理一次，'[' ']' 各进栈出栈一次，所以是 O(n)；
#    空间最坏是嵌套深度层栈，也是 O(n)。
