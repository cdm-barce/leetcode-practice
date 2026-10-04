# LeetCode 33. 搜索旋转排序数组（中等）
# 套路：一趟二分——每轮判断哪半有序，再用有序半的端点定位 target 去向，O(log n) 时间 / O(1) 空间
# 2026-10-04
# 最优代码

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # 闭区间 [l, r]，两端都是可取下标
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                return mid          # 命中，返回下标

            # 核心：旋转数组一刀切开，左右两半必有一半"完全有序"。
            # 先判断哪半有序（只看端点 nums[l] 和 nums[mid] 的大小关系），
            # 再用有序那半的端点范围判断 target 在不在里面，从而决定收缩方向。

            if nums[l] <= nums[mid]:
                # 左半 [l..mid] 有序。注意 <=：区间缩到只剩两元素时 l==mid，
                # 左半退化为单元素，仍算"有序"，等号不能丢。
                if nums[l] <= target < nums[mid]:
                    r = mid - 1     # target 落在有序左半里（右开，mid 已排除）
                else:
                    l = mid + 1     # 否则只能去右半
            else:
                # 右半 [mid..r] 有序。对称地判断。
                if nums[mid] < target <= nums[r]:
                    l = mid + 1     # target 落在有序右半里（左开，mid 已排除）
                else:
                    r = mid - 1     # 否则只能去左半
        return -1                   # 区间缩空，target 不存在


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert s.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert s.search([1], 0) == -1
    # 边界：target 在左段/右段/两端、未旋转、单元素、两元素旋转
    assert s.search([4, 5, 6, 7, 0, 1, 2], 6) == 2   # target 在有序左段
    assert s.search([4, 5, 6, 7, 0, 1, 2], 2) == 6   # target 在最右
    assert s.search([1, 3, 5], 3) == 1               # 未旋转（整体有序）
    assert s.search([1], 1) == 0                     # 单元素命中
    assert s.search([3, 1], 1) == 1                  # 两元素旋转，触发 l==mid 的坑
    print("全部用例通过 ✓")

# 踩坑记录：
# 1.【本次的核心 bug】最初只判断了"哪半有序"，却漏了"target 在不在有序半里"，
#    于是在"有序"分支里无条件跳去另一半。Case 1（[4,5,6,7,0,1,2] target=0）就挂在这：
#    第 2 轮左半 [0,1] 有序、target=0 明明在 [0,1) 里，代码却把它扔掉跳去了右边，最终 return -1。
#    → 教训："哪半有序"和"target 在哪半"是两个独立判断，缺一不可。
#      "哪半有序"只告诉你哪半能看端点；"target 在不在里面"才决定往哪跳。
# 2.【为什么必须先判断哪半有序，不能直接判断 target 在哪边】
#    旋转数组中间"塌"了一次（大数段→小数段），端点给不出可靠范围。
#    想"直接判断在哪边"，其实已经在心里偷用了"哪半大哪半小"这个事实——而它正是
#    "哪半有序"才告诉你的。所以判断有序不是目的，是获得"可信任范围"的工具。
# 3.【为什么总有一半有序】旋转数组是"有序数组砍成两截对调"，只有一个塌陷点。
#    任意一刀（mid）切下去，塌陷点只能落在一半里，所以必有一半干净有序。
# 4.【端点区间的开闭】两个判断区间都刻意排除了 mid：
#    左半用 nums[l] <= target < nums[mid]（右开），右半用 nums[mid] < target <= nums[r]（左开）。
#    因为 nums[mid] == target 在循环第一行就返回了，走到这里 mid 必非答案，可放心剔除。
# 5. 与 v1（两趟：先找旋转点再分段二分）相比，这版只扫一遍、判断更少，常数更小，
#    是 LC 的标准 0ms 解。渐进复杂度两者同为 O(log n)。
