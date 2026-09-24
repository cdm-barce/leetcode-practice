# LeetCode 392. 判断子序列（简单）
# 套路：进阶解——位置表 + 二分（针对「大量 s、同一个 t」的批量查询场景）
# 预处理 O(n) 时间 / O(n) 空间，单次查询 O(len(s) · log n) 时间
# 2026-09-24
# 最优代码（进阶版，研究用）

from bisect import bisect_right


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # ---- 预处理：给 t 每个字母建「所有出现下标」的有序列表 ----
        # 遍历 t 时按下标从小到大 append，所以每个列表天然有序（这是能二分的前提）
        pos_map = {}
        for i, ch in enumerate(t):
            pos_map.setdefault(ch, []).append(i)

        # ---- 查询：维护 pos = 上一笔匹配到的 t 下标（初始 -1 表示还没匹配任何字符）----
        pos = -1
        for ch in s:
            lst = pos_map.get(ch, [])       # 该字母在 t 里的所有位置；不存在则为空列表
            idx = bisect_right(lst, pos)    # 第一个「严格大于 pos」的位置的下标
            if idx == len(lst):             # 后面再也没有这个字母了 → 失败
                return False
            pos = lst[idx]                  # 跳到这个位置，贪心取最早的合法匹配
        return True


if __name__ == "__main__":
    sol = Solution()

    cases = [
        ("abc", "ahbgdc", True),            # 官方示例 1
        ("axc", "ahbgdc", False),           # 官方示例 2
        ("", "ahbgdc", True),               # 空 s
        ("abc", "", False),                 # t 为空
        ("aa", "aca", True),                # 杀「单值版」的反例：a 出现两次，须保留 [0,2]
        ("aaaa", "a", False),               # s 比 t 长
        ("acb", "ahbgdc", False),           # 顺序错误
    ]

    for src, target, want in cases:
        got = sol.isSubsequence(src, target)
        assert got == want, f"{src!r} in {target!r} 得到 {got}，期望 {want}"

    print("全部用例通过 ✓")

# 踩坑记录 / 进阶要点：
# 1. 【为什么是列表而非单值】t 中同一字母可能多次出现。若用 dict[ch] = 下标 覆盖式赋值，
#    只会留下最后一次出现的位置。反例：t="aca", s="aa" 应返回 True（a 在 0 和 2），
#    但单值版只会记住 a=2，查第一个 a 用掉 2 后第二个 a 找不到 → 误判 False。
#    所以必须存「该字母的所有出现下标列表」，且按下标升序 append。
# 2. 【为什么要严格大于 pos】pos 是上一笔已用掉的下标，同一个 t 位置不能重复匹配
#    s 的两个字符，所以下一笔必须找 > pos 的。bisect_right 正好返回「第一个 > x 的下标」。
# 3. 【bisect_right 边界】返回值为 len(lst) 时代表「pos 之后没有更大的了」，
#    对应失败；否则 lst[idx] 就是下一次匹配位置。空列表 len==0，bisect_right 返回 0，
#    0==0 成立 → 自动判失败，无需单独写「字符不存在」分支。
# 4. 【dict.get(ch, [])】第二个参数是「key 不存在时返回的兜底值」，这里返回空列表，
#    避免直接 dict[ch] 抛 KeyError。get 的默认值每次调用都是新对象，不会跨调用污染
#    （区别于 def f(x=[]) 共享默认对象的坑）。
# 5. 【复杂度权衡】预处理 O(n)、单次查询 O(len(s)·log n)。当有大量 s 要查同一个 t 时，
#    比每次双指针重扫 t 的 O(len(s)+n) 更划算（s 很短时尤其明显）。
#    另一种更狠的做法是 next 自动机表（nxt[i][c]），单字符 O(1) 但空间 O(26n)，
#    是 LC 792「匹配子序列的单词数」的前置思想。
# 6. 【标准库彩蛋】单次查询还有 Pythonic 一行流：it = iter(t); return all(c in it for c in s)。
#    原理是 `c in it` 会消耗迭代器直到找到 c，等价于 p2 被迭代器协议自动维护。
#    面试甩出是加分项，但要能讲清「为何等价于双指针」。
