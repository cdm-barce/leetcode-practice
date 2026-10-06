# LeetCode 162. 寻找峰值（中等）
# 套路：二分「峰在哪半边」只比右邻，严格 O(log n) 时间 / O(1) 空间
# 2026-10-06
# 最优代码

from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        # 不变量：[l, r] 区间内必存在峰值。
        # 初始全区间必有（两端外是虚拟 -∞）；每轮都朝「必有峰」的那半边收缩，
        # 所以收敛到 l == r 时，这个唯一的元素就是峰。
        while l < r:
            mid = (l + r) // 2  # 左中位；有 r = mid 分支，必须下取整，否则死循环
            if nums[mid] < nums[mid + 1]:
                # 上坡：站在上坡往右走，要么一路涨到末尾（末尾外是 -∞，末尾即峰），
                #       要么中途拐头下降（拐点即峰）→ 峰必在右半边 [mid+1, r]
                l = mid + 1
            else:
                # 下坡：峰必在左半边（mid 本身也可能是峰，故保留 mid）
                r = mid
        return l


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.findPeakElement([1, 2, 3, 1]) == 2
    assert s.findPeakElement([1, 2, 1, 3, 5, 6, 4]) in (1, 5)
    # 边界用例
    assert s.findPeakElement([1]) == 0          # 单元素
    assert s.findPeakElement([1, 2]) == 1       # 递增
    assert s.findPeakElement([2, 1]) == 0       # 递减
    assert s.findPeakElement([1, 2, 1, 2, 1]) in (1, 3)  # 锯齿形双峰，返回任意一个合法峰
    assert s.findPeakElement([6, 5, 4, 3, 7]) in (0, 4)  # 双峰，不再依赖兜底
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 思维转换：不要问「mid 是不是峰」（查两个邻居、3 次比较、还得处理边界），
#    要问「峰在哪半边」（只查 1 个邻居 nums[mid] vs nums[mid+1]）。
# 2. 虚拟边界 nums[-1]=nums[n]=-∞ 不需要显式判断，它藏在「区间内必有峰」这个不变量里。
# 3. mid+1 永不越界：while l < r 保证 mid <= r-1，故 mid+1 <= r。
# 4. mid 必须取左中位 (l+r)//2：因为有 r = mid 分支，取右中位会在 l==r-1 时 mid==r、
#    r=mid 原地不动导致死循环。
# 5. 题目只要求返回任意一个峰的下标，不保证是全局最高峰；二分保证返回一个合法峰。
