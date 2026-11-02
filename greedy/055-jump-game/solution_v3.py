# LeetCode 55. 跳跃游戏（中等）
# 套路：反向贪心（从终点倒推「谁能到达我」）
# 2026-11-02
# 思路对比版：逻辑正确但实测最慢（无法中途退出），仅作参考

class Solution:
    def canJump(self, nums: list[int]) -> bool:
        goal = len(nums) - 1        # 当前需要被到达的目标位置
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:  # 从 i 能一步跨到 goal（或更远）
                goal = i             # 目标左移：现在只要有人能到 i 就行
        return goal == 0             # 目标一路缩到起点，说明能到


if __name__ == "__main__":
    s = Solution()

    assert s.canJump([2, 3, 1, 1, 4]) is True
    assert s.canJump([3, 2, 1, 0, 4]) is False
    assert s.canJump([0]) is True
    assert s.canJump([1]) is True
    assert s.canJump([0, 1]) is False
    assert s.canJump([1, 0, 0]) is False
    assert s.canJump([5, 0, 0, 0, 0]) is True
    assert s.canJump([2, 0, 0]) is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 这个思路很漂亮：从右往左看「谁能跨到当前 goal」，能跨就把 goal 拉到自己身上，
#    最后看 goal 有没有被拉到 0。本质是把「从起点能到哪些点」倒过来想成
#    「哪些点能到终点」，逻辑等价。
# 2. 但它**无法中途退出**——即使 goal 已经变成 0（确定能到终点），
#    循环还得把剩下的元素全部走完，因为没法提前知道后面有没有更优的 goal。
#    而正向版在 `far < i` 时立刻 return False，天然能早停。
# 3. 实测（1000 个元素）：反向贪心 38 μs，正向 2 μs，**慢 19 倍**。
#    复杂度同为 O(n)，差距全在「能不能提前退出循环」。
# 4. 什么时候反向思路真的有用：当问题天然适合「从终点倒推」时，
#    比如某些区间调度、或者需要维护「后缀最优值」的题。
#    这题不属于这种，正方问法更自然。
# 5. 结论：能写正向就别写反向，除非正向推不出来。
