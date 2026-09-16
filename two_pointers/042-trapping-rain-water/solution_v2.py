from typing import List

# LeetCode 42. 接雨水（中等）
# 套路：对撞双指针，哪侧 running max 小就结算哪侧，O(n) 时间 / O(1) 空间
# 2026-09-16
# 最优代码

class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_left = max_right = 0   # 双指针各自扫过的真实最高
        res = 0

        while left < right:
            max_left = max(max_left, height[left])
            max_right = max(max_right, height[right])

            # 位置能接的水 = min(左max, 右max) - 自己高
            # 若 max_left < max_right：左指针这侧 min 必等于 max_left（瓶颈在左），
            #   右侧还没扫到也无所谓 → 直接结算左指针，右移
            if max_left < max_right:
                res += max_left - height[left]
                left += 1
            else:
                # 对称：瓶颈在右，结算右指针，左移
                res += max_right - height[right]
                right -= 1

        return res


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    # 空 / 单元素
    assert s.trap([]) == 0
    assert s.trap([0]) == 0
    assert s.trap([1]) == 0
    # 递增 / 递减
    assert s.trap([1, 2, 3, 4, 5]) == 0
    assert s.trap([5, 4, 3, 2, 1]) == 0
    # 经典多坑
    assert s.trap([4, 2, 0, 3, 2, 5]) == 9
    # 中间最低
    assert s.trap([2, 0, 2]) == 2
    assert s.trap([2, 1, 0, 1, 2]) == 4
    # 全平：一根柱也接不到
    assert s.trap([3, 3, 3, 3]) == 0
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 核心不变量：位置 i 接水量 = min(左侧真实最高, 右侧真实最高) - height[i]。
#    双指针只维护左右各自扫过的真实最高，不需要预知全局峰值。
# 2. 关键判断：当 max_left < max_right 时，左指针处的 min 一定是 max_left——
#    因为右指针右侧还有更高（或相等）的柱挡着，瓶颈已锁定在左侧，右侧轮廓无所谓。
#    这一步的推理正是把 O(n)+额外扫描替换成“一趟 + 边走边结算”的支点。
# 3. 等号放 else 分支（结算 right）即可，左右任一相等时先结算哪侧都不影响结果。
# 4. 相比 v1（找全局峰值拆分）：时间同 O(n)，空间同 O(1)，但 v2 单趟、不用 max()/index()
#    预扫峰值，写法更统一，是面试里最常被追认的“最优解”。
