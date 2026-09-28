# LeetCode 1004. 最大连续 1 的个数 III（中等）
# 套路：滑动窗口（count0 计数 + while 收缩到合法），O(n) 时间 / O(1) 空间
# 2026-09-28
# 我的解答（AC：63/63，64ms 击败 55.21%）

from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        # 滑动窗口求「最长」，满足条件的子数组（最多翻 k 个 0）
        n = len(nums)
        L = 0
        best = 0
        count0 = 0  # 窗口 [L, R] 内 0 的个数

        # 特判：k 不小于数组长度时，可以把所有 0 都翻成 1
        if n <= k:
            return n

        for R in range(n):
            # 1. 右指针扩张：新元素进窗口
            if nums[R] == 0:
                count0 += 1

            # 2. 收缩：窗口内 0 的个数超过 k 时（多了翻不过来）
            #    注意条件是 count0 > k，而非 >= k：恰好 k 个 0 是合法的（全翻掉即可）
            while count0 > k:
                # 移出左边界的元素；只有移出的是 0 才减计数
                if nums[L] == 0:
                    count0 -= 1
                L += 1  # 左指针无条件右移

            # 3. 出了 while，窗口保证合法，此时才更新答案
            #    （若把 best 更新放在 while 里，会把「正在吐出多余 0」的中间态长度记进去 → WA）
            best = max(best, R - L + 1)

        return best


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert s.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
    # 边界用例
    assert s.longestOnes([0, 0, 1, 1, 1, 0, 0], 0) == 3  # 之前判题失败的用例：k=0
    assert s.longestOnes([1, 1, 1, 1], 0) == 4           # 全 1，k=0
    assert s.longestOnes([0, 0, 0], 5) == 3              # k 超过数组长度
    assert s.longestOnes([1], 0) == 1                    # 单元素
    assert s.longestOnes([0], 0) == 0                    # 单 0，k=0
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 【WA】best 更新写在了收缩的 while 循环里 → 失败用例 [0,0,1,1,1,0,0], k=0 输出 4（期望 3）。
#    根因：while 收缩过程是「正在吐出多余 0」的中间态，窗口此时还不合法，长度是脏数据。
#    正确做法：best 更新放在 while 之后，保证此时窗口一定合法。
# 2. 【WA】收缩条件误用 count0 >= k → k=0 时 count0 >= 0 恒为真，条件直接失真。
#    正确：count0 > k（恰好 k 个 0 合法，全翻掉即可，只有超过才需收缩）。
# 3. 【多余】用 nums[R+1] 预判 + R+1==n 特判：滑动窗口不需要偷看未来，
#    0 真进了窗口、真超标了再收缩即可，这些特判全是预判带来的复杂性。
# 4. 【危险】在 while 里放 break 让「循环收缩」退化成只收一次；在 for 里放 break
#    会直接跳出主循环 → 全数组只算第一个窗口，返回错误小值。
# 5. 【进阶】本题还有「非收缩滑动窗口」写法（见 solution_v2.py）：窗口只平移不缩小，
#    直接消耗 k，答案 = len - L，省掉逐轮 max 调用，实测快约 1.74x。
