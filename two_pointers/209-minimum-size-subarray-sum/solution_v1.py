# LeetCode 209. 长度最小的子数组（中等）
# 套路：枚举左右端点 + 每步重新切片求和（暴力），O(n³) 时间 / O(n) 空间
# 2026-09-27
# 我的解答（初版：线上 AC 14/23，有一处致命逻辑错 + 一处性能坑）

class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        n = len(nums)
        min_len = 0                        # BUG②：拿 0 当「还没找到」的哨兵，
                                           #        逼出下面的 if/else 双分支，反而把 BUG① 藏得更深
        total = 0                          # 冗余：total 每轮都被 sum() 整体覆盖，这个初值没意义
        for L in range(n):                 # 左端点
            R = L + 1                      # 右端点，窗口是左闭右开 [L, R)
            while R < n + 1:               # 用 n+1 是因为右端开区间，得有机会取到 R == n
                total = sum(nums[L: R])    # BUG③：每步重新切片求和 O(n)，
                                           #        外面还套了两层循环 → 整体 O(n³)
                if total >= target:
                    if min_len == 0:
                        min_len = total    # BUG①【致命】：把「窗口和」当成了「窗口长度」！
                                           #                这里应该是 R - L
                    else:
                        min_len = min(min_len, R - L)
                R += 1
        return min_len                     # 一个都没命中时 min_len 仍是 0，这里恰好符合题意


if __name__ == "__main__":
    s = Solution()
    # 本版的实际输出——用 assert 把错误行为固化成反面证据
    assert s.minSubArrayLen(15, [1, 2, 3, 4, 5]) == 15     # 正确应为 5
    print("反面演示 ✓ 输出 15（把窗口和当成长度了），而正确答案是 5")

    # 有些用例它又会「侥幸」答对，这正是 14/23 而不是 0/23 的原因
    assert s.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2    # 侥幸正确
    assert s.minSubArrayLen(4, [1, 4, 4]) == 1             # 侥幸正确
    print("侥幸通过的用例 ✓ 所以「过了几个用例」完全不能当作正确性证明")


# 踩坑记录
# 1. 【致命】min_len = total —— 命中窗口时更新的是「和」，不是「长度」。
#    根因：把「判定条件里用的量」和「要维护的答案」搞混了。
#        total 是用来跟 target 比大小的中间量；答案是窗口宽度，即 R - L。
#    完整证据链（target=15, nums=[1,2,3,4,5]）：
#        L=0 扫到 R=5 时 total = 1+2+3+4+5 = 15 ≥ 15，这是「第一次命中」，
#        于是走 min_len == 0 分支 → min_len 被赋成 15；
#        之后 L=1..4 无论怎么扩，最大和都只有 14 < 15，else 分支永远没机会修正，
#        最后 return 15，而正确输出是 5。
# 2. 【隐患】min_len = 0 当哨兵，让「第一次命中」和「后续命中」走了两条不同分支
#    （一个赋值、一个取 min），逻辑重复。改用 min_len = n + 1 或 float('inf')，
#    写成一行 min_len = min(min_len, R - L) 就行，两条分支合并后这个 BUG 根本无处藏身。
# 3. 【性能】total = sum(nums[L: R]) 写在双层循环最里层：外层 L × 内层 R × 求和 O(n) ≈ O(n³)。
#    n = 10⁵ 时必然 TLE。正解是「一进一出」增量维护窗口和 —— 见 solution_v2.py。
# 4. 【认知】AC 14/23 是个陷阱。能过的那批用例，是因为 L 从 0 开始枚举时
#    「第一次命中的窗口」往往就是以 L 开头的最短窗口，而某些场景下 total 的数值
#    刚好等于长度（例如全 1 的数组）——数值凑巧相等，错误就看不出来。
#    教训：本地对拍（用最笨但正确的 O(n²) 暴力当标尺）比盯着用例通过率靠谱得多。
# 5. 【命名】R 在这里是开区间端点 [L, R)，必须 +1 才能表示长度；
#    和闭区间写法混用极易差 1。v2 统一改成闭区间 [L, R]，长度直接写 R - L + 1，歧义消失。
