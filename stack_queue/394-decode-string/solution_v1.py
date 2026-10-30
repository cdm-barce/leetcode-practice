# LeetCode 394. 字符串解码（中等）
# 套路：双状态栈（栈里存「倍数 + 外层已拼好的前缀」元组）
# 2026-10-30
# 我的解答（结构全对，但数字累积写错，所有带数字的用例都返回空串）

class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        cur = ""
        num = 0

        for ch in s:
            if ch.isdigit():
                num = num * 10 + num        # 错：应该是 int(ch)，写成了 num 自己
            elif ch == '[':
                stack.append((num, cur))    # 存现场：倍数 + 外层前缀
                num, cur = 0, ""            # 同时重置，不能用两行分开写（易漏）
            elif ch == ']':
                k, prev = stack.pop()       # 恢复现场
                cur = prev + k * cur        # 外层前缀 + 本层结果×倍数
                num = 0                     # 防御性复位
            else:
                cur = cur + ch              # 普通字母直接追加

        return cur


if __name__ == "__main__":
    from itertools import repeat
    st = Solution()

    def d(n, c):
        return c * n

    # 下面断言的「是本版实际输出的错误结果」，用来保留 WA 证据
    assert st.decodeString("3[a]2[bc]") == ""
    print("反面演示 ✓ '3[a]2[bc]' 返回 ''，正确答案应为 'aaabcbc'")

    assert st.decodeString("3[a2[c]]") == ""
    print("反面演示 ✓ '3[a2[c]]' 返回 ''，正确答案应为 'accaccacc'")

    assert st.decodeString("2[abc]3[cd]ef") == "ef"
    print("反面演示 ✓ '2[abc]3[cd]ef' 返回 'ef'，正确答案应为 'abcabccdcdcdef'")

    assert st.decodeString("12[a]") == ""
    print("反面演示 ✓ '12[a]' 返回 ''，正确答案应为 'a' × 12")

    # 唯一能通过的：没有数字，压根不走累积分支
    assert st.decodeString("abc") == "abc"
    print("碰巧通过 ✓ 'abc' 返回 'abc'（没有数字，没触发 bug）")


# 踩坑记录：
# 1. 这一处写错就足以让整题全盘皆错：
#        num = num * 10 + num        # 错，num 永远等于 0
#        num = num * 10 + int(ch)    # 对
#    num 初值是 0，0 * 10 + 0 还是 0，所以不管读多少位数字，num 始终是 0。
# 2. 后果链条：num = 0 → 压栈的倍数是 0 → ']' 时 cur = prev + 0 * cur，
#    括号里的内容被乘成了空，只剩下括号外的字母。
#    '2[abc]3[cd]ef' 返回 'ef' 就是最直接的证据（两段括号全没了）。
# 3. 错误特征很好认：**凡是带数字的用例全错，纯字母的能过**。
#    出现这种「成片失败但又有少数通过」的情况，先怀疑某个分支的变量没更新对。
# 4. 自查方法：最小用例手算。'3[a]' 只走三步，
#    ch='3' 时 num 应该变成 3，实际是 0 —— 一眼就能抓到。
# 5. 除了这一处，其他全对：栈存元组、'[' 存现场+同时重置、']' 先弹出再拼接、
#    前缀在前（prev + ...）、返回值 cur。见 solution_v2.py。
