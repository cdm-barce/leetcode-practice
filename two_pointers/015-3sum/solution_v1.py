from typing import List

# LeetCode 15. 三数之和（中等）
# 套路：排序 + 双指针，O(n²) 时间 / O(1) 额外空间
# 2026-09-15
# 最优代码


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        res = []

        # 外层固定第一个数 nums[i]；i 最多到 n-3，后面要留两个位置给 L、R
        for i in range(n - 2):
            # 去重①：当前固定值和上一轮一模一样，则上一轮已把以它为起点的解找全，直接跳过
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            L, R = i + 1, n - 1  # 左右指针从 i 之后的两端向中间夹
            while L < R:
                s = nums[i] + nums[L] + nums[R]
                if s == 0:
                    res.append([nums[i], nums[L], nums[R]])
                    L += 1
                    R -= 1
                    # 去重②：跳过与刚用过的值相同的元素，避免重复三元组
                    while L < R and nums[L] == nums[L - 1]:
                        L += 1
                    while L < R and nums[R] == nums[R + 1]:
                        R -= 1
                elif s < 0:
                    L += 1  # 和偏小，需要更大的数 → 左指针右移
                else:
                    R -= 1  # 和偏大，需要更小的数 → 右指针左移

        return res


if __name__ == "__main__":
    s = Solution()
    # 官方示例 1
    assert sorted(s.threeSum([-1, 0, 1, 2, -1, -4])) == sorted([[-1, -1, 2], [-1, 0, 1]])
    # 官方示例 2：空数组
    assert s.threeSum([]) == []
    # 官方示例 3：元素不足 3 个
    assert s.threeSum([0]) == []
    # 全零：只能有一个 [0,0,0]，验证去重①
    assert s.threeSum([0, 0, 0]) == [[0, 0, 0]]
    # 多个 0 同样只出一组，验证去重②
    assert s.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
    # 同轮 i 有多组解：命中后不能 break，否则漏掉 [-2,1,1]
    assert sorted(s.threeSum([-2, 0, 1, 1, 2])) == sorted([[-2, 0, 2], [-2, 1, 1]])
    # 最短重复用例
    assert s.threeSum([-1, -1, 2]) == [[-1, -1, 2]]
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 第一版三层暴搜（x/y/z 三指针嵌套 while），找到解后 z 不前进、靠 continue 原地打转，
#    seen 被无限 append 同一组解 → Memory Limit Exceeded。根因：收录解后指针必须前进。
# 2. 第二版加了 break 跳出 while，但仍有两个坑：
#    a) 固定位 i 未去重 → [0,0,0] 被记录两次（57/316 用例失败）。
#       修复：i>0 且 nums[i]==nums[i-1] 时 continue。
#    b) 命中后直接 break 会漏解：同一轮 i 的固定值只决定「另两数之和」，
#       可能有多个 (L,R) 对（如 [-2,0,1,1,2] 漏掉 [-2,1,1]）。
#       修复：命中后 L++ 且 R-- 继续向中间夹，再双向跳重。
# 3. 学到的：排序后固定一个数 + 双指针，把 O(n³) 降到 O(n²)；去重有两处（i 层与 L/R 层），
#    且都在「移动指针之后」用「和上一个/下一个比」的方式滑过重复值，顺序不能反。
