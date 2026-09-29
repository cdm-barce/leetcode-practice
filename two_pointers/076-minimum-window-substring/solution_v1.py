# LeetCode 76. 最小覆盖子串（困难）
# 套路：收缩式滑动窗口 + need 变量 O(1) 判覆盖，O(n) 时间 / O(|Σ|) 空间
# 2026-09-29
# 我的解答（初版踩坑后修正）

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        m = len(t)
        if m > len(s):
            return ""

        # cnt[c] 的语义：>0 表示窗口还缺 |cnt[c]| 个 c；<=0 表示窗口里 c 已够（含冗余）
        cnt = [0] * 58
        for ch in t:
            cnt[ord(ch) - ord('A')] += 1

        # need = 还缺几个 t 的字符，降到 0 即全覆盖（O(1) 判断，替代每步 max()）
        need = m
        L = 0
        best_start, best_len = 0, len(s) + 1  # len(s)+1 是“没找到”的哨兵

        for R in range(len(s)):
            c = ord(s[R]) - ord('A')
            # 先判断再消耗：cnt[c] > 0 说明这个字符是正缺的
            if cnt[c] > 0:
                need -= 1
            cnt[c] -= 1

            # 全覆盖后进入收缩：先记答案、再弹左端，顺序不能反
            while need == 0:
                if R - L + 1 < best_len:          # 和历史最优比，不是和 len(s)+1 比
                    best_start, best_len = L, R - L + 1
                lc = ord(s[L]) - ord('A')
                cnt[lc] += 1                       # 弹出 = 还回需求
                if cnt[lc] > 0:                    # 还回来变成正数 → 弹掉的是必需字符
                    need += 1
                L += 1

        return "" if best_len == len(s) + 1 else s[best_start : best_start + best_len]


if __name__ == "__main__":
    sol = Solution()
    # 官方用例
    assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert sol.minWindow("a", "a") == "a"
    assert sol.minWindow("a", "aa") == ""          # 数量不够
    # 边界用例
    assert sol.minWindow("ab", "b") == "b"         # 答案在末尾
    assert sol.minWindow("bba", "ab") == "ba"      # 需要收缩掉前面的冗余
    assert sol.minWindow("aa", "aa") == "aa"       # 重复字符按数量覆盖
    assert sol.minWindow("abcbbbbbbca", "abc") == "abc"  # 反例：答案不是最后一次覆盖的窗口
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 第一版（枚举起点 + max(seen) 判覆盖）输出 "d"（预期 "BANC"）：
#    `seen = cnt` 是引用不是拷贝，且窗口字符只减不恢复。第一轮扫完 cnt 全是负数，
#    第二轮循环一进来 max(seen) <= 0 就成立，程序误以为“1 个字符就覆盖了 t”，
#    把单个字符记进了答案。教训：复制列表要 cnt[:]，且每轮起点要还原计数——
#    但更根本的解法是别用“每个起点重扫”的 O(n²) 暴力，直接上收缩窗口。
# 2. 收缩版第 22 行 `best_start, best_len = L, min(R - L + 1, len(s) + 1)` 两个坑叠加：
#    ① min 的比较对象错——该和历史最优 best_len 比，和 len(s)+1 比 min 恒等于当前窗口长度；
#    ② best_start = L 无条件覆盖——只有当前窗口更短时才更新。
#    后果：记录的永远是“最后一次覆盖时的窗口”。反例 s="abcbbbbbbca", t="abc"：
#    最后一次覆盖收缩到 "bbca"(4)，而真正最短是开头的 "abc"(3)，这版输出 "bbca"。
#    正确写法：if R - L + 1 < best_len: best_start, best_len = L, R - L + 1
# 3. `cnt[s[L]] += 1`：s[L] 是字符串，不能拿去索引 list（TypeError），
#    必须和进窗时保持一致用 ord(s[L]) - ord('A')。
# 4. 学到的关键技巧：
#    ① need 变量把“是否覆盖 t”的判断从 O(58) 的 max() 降到 O(1)；
#    ② 收缩循环里必须“先更新答案再弹字符”——弹完窗口可能就不合法了；
#    ③ 判 cnt[c] > 0 必须在 cnt[c] -= 1 之前，顺序反了语义就错；
#    ④ 收缩式滑动窗口每个字符最多进窗一次、出窗一次，总复杂度 O(n)，
#       比枚举起点的 O(n²) 暴力（本题 n=1e5 必 TLE）质变。
