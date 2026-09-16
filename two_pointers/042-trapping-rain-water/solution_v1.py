from typing import List

# LeetCode 42. 接雨水（中等）
# 套路：找全局最高点拆左右两段，各段用 running max 累加，O(n) 时间 / O(1) 空间
# 2026-09-16
# 我的解答

class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        max_h = max(height)
        mid = height.index(max_h)  # 全局最高点位置：把数组拆成左段 [0,mid) 和右段 (mid,end]
        res = 0

        # 左段：某位置能接的水 = 左侧出现过的柱子里的最高 - 自己
        # 右边界就是 mid 处那根全局最高，所以左段只需看 left_max 即可
        left_max = 0
        for i in range(mid):
            left_max = max(left_max, height[i])
            res += left_max - height[i]

        # 右段：从右往左，同样用右侧出现过的最高当作右边界
        right_max = 0
        for i in range(len(height) - 1, mid, -1):
            right_max = max(right_max, height[i])
            res += right_max - height[i]

        return res


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    # 空 / 单元素
    assert s.trap([]) == 0
    assert s.trap([0]) == 0
    assert s.trap([1]) == 0
    # 递增 / 递减：单边无凹陷，接不到水
    assert s.trap([1, 2, 3, 4, 5]) == 0
    assert s.trap([5, 4, 3, 2, 1]) == 0
    # 经典多坑
    assert s.trap([4, 2, 0, 3, 2, 5]) == 9
    # 中间最低
    assert s.trap([2, 0, 2]) == 2
    assert s.trap([2, 1, 0, 1, 2]) == 4
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 最初想“每个位置存左边最高、右边最高两个数组再相减”，空间 O(n)。其实用 running max
#    边扫边加就够，空间压到 O(1)，本版已是最简形态。
# 2. mid = height.index(max_h) 取的是「第一个」全局最高点：左段右边界就是它（全局最高），
#    右段左边界也是它，拆在第一个最高点完全正确；即便后面还有同样高的最高点也不影响结算。
# 3. max()/index() 会先整段扫一遍找峰值，等于“额外一趟”；对撞双指针版（v2）一趟扫完且
#    不必预知峰值位置。两者时间都 O(n)、空间都 O(1)，v2 是更顺手的写法。
