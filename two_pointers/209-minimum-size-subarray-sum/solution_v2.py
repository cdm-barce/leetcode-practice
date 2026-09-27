# LeetCode 209. 长度最小的子数组（中等）
# 套路：滑动窗口（同向双指针）+ 窗口和「一进一出」增量维护，O(n) 时间 / O(1) 空间
# 2026-09-27
# 我的解答（二次提交，一次通过 23/23，19ms 击败 72.83%，29.91MB 击败 88.12%）

class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        n = len(nums)
        best = n + 1                 # 哨兵：合法长度最大就是 n，比它大即代表「一次都没命中过」
                                     # 特意不用 0 当哨兵——0 会逼出 if/else 双分支（见 v1 的 BUG①）
        total = 0                    # 窗口 [L, R] 内元素之和，全程增量维护，不再切片重算
        L = 0                        # 左指针：只向右走，永不回头
        for R in range(n):           # 右指针：每个元素只会被「纳入窗口」一次
            total += nums[R]         # 扩张：把 nums[R] 收进窗口

            while total >= target:   # 只要还达标，就继续试探能不能缩得更短
                                     # 题目要求「大于等于」，所以是 >= 不是 >
                best = min(best, R - L + 1)   # 闭区间 [L, R] 的长度 = R - L + 1
                total -= nums[L]     # 收缩：把 nums[L] 踢出窗口
                L += 1               # 左指针右移

        return 0 if best == n + 1 else best   # 全程没命中过 → 按题意返回 0


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2           # 最短是 [4, 3]
    assert s.minSubArrayLen(4, [1, 4, 4]) == 1                   # 单个 4 就够
    assert s.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0    # 全加起来才 8 < 11 → 无解返回 0
    # 边界用例
    assert s.minSubArrayLen(15, [1, 2, 3, 4, 5]) == 5             # v1 就是在这条挂的（错答 15）
    assert s.minSubArrayLen(1, [1]) == 1                          # 单元素刚好达标
    assert s.minSubArrayLen(100, [1, 2, 3]) == 0                  # 总和小于 target
    assert s.minSubArrayLen(3, [1, 1, 1]) == 3                    # 必须整个数组才够
    assert s.minSubArrayLen(6, [10, 2, 3]) == 1                   # 首个元素单独达标（答案 = 1 的极端）
    assert s.minSubArrayLen(1000000000, [1000000000]) == 1        # target 取到上界
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 这版相对 v1 改掉了三件事：
#    ① min_len = total → best = R - L + 1（和 ≠ 长度，v1 的致命错）；
#    ② 哨兵从 0 换成 n + 1，一举干掉 if/else 双分支；
#    ③ 窗口和改成增量维护，砍掉 sum(nums[L:R]) 这个 O(n) 的重复劳动。
# 2. 为什么是 O(n)（这是滑动窗口最该讲清楚的一句）：
#    R 从 0 走到 n-1，L 总共也只从 0 走到 n-1（内层 while 里 L 只加不减）。
#    也就是说每个元素最多被 total += 一次、被 total -= 一次 —— 总操作次数 ≤ 2n。
#    对比 v1 的「枚举所有 (L, R) 组合」：那里是 n² 个窗口 × 每个窗口 O(n) 求和 = O(n³)。
# 3. 顺手做的对照实验（实测 n = 200000 随机数据）：
#      本版滑动窗口 O(n)              → 36 ms
#      前缀和 + 二分 O(n log n)        → 74 ms  ← 反而慢一倍
#    「复杂度更低一定更快」是错觉：二分每轮的函数调用 + 额外建一个前缀和数组，
#    常数开销直接把 n log n 的优势吃光了。Python 里这种纯线性扫描几乎打不过。
# 4. 可选微优化：while 里加 if best == 1: return 1（长度不可能比 1 更小，直接收工）。
#    实测只在「答案正好是 1」的数据上有意义（26.55 ms → 0 ms），
#    其余数据（随机数据、无解数据）毫无差别。属于看数据吃饭的优化，不加完全没问题。
# 5. 「大于等于」的边界必须写 >= ：写成 > 会在 target 恰好等于某段窗口和时漏掉最短窗口。
# 6. 正确性用对拍验：拿最笨但正确的暴力 O(n²) 当标尺，随机跑 3000 组小数据，0 处不一致。
#    （暴力版要点：对每个起点 i 向右累加，一旦 s >= target 就 break —— 后面只会更长。）
