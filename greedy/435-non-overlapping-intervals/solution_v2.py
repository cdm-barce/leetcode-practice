# LeetCode 435. 无重叠区间（中等）
# 套路：按右端点排序 + 贪心（优先保留结束最早的区间）
# 2026-11-09
# 最优代码，O(n log n) 时间（排序主导）/ O(1) 额外空间

class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        # 关键：按「右端点」排序，不是左端点
        intervals.sort(key=lambda x: x[1])

        count = 0
        end = float("-inf")      # 最后一个「保留下来」的区间的右端点

        for start, finish in intervals:
            if start >= end:     # 不重叠（注意是 >=，端点相接不算重叠）
                end = finish     # 保留它，边界更新成它的右端（不是 max）
            else:                # 重叠
                count += 1       # 丢掉它，边界不动

        return count


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1：去掉 [1,3]，剩 [1,2][2,3][3,4]
    assert s.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1

    # 官方示例 2：去掉两个 [1,2]
    assert s.eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2

    # 官方示例 3：本来就无重叠
    assert s.eraseOverlapIntervals([[1, 2], [2, 3]]) == 0

    # 构造用例：大区间排前面也不能出错
    assert s.eraseOverlapIntervals([[1, 100], [2, 3], [4, 5]]) == 1

    # 构造用例：被丢弃的区间不能污染后续判断
    assert s.eraseOverlapIntervals([[1, 5], [2, 3], [4, 6]]) == 1

    # 边界：只有一个区间
    assert s.eraseOverlapIntervals([[1, 2]]) == 0

    # 边界：一个大区间包住两个小区间，只需丢掉大区间
    assert s.eraseOverlapIntervals([[1, 10], [2, 3], [4, 5]]) == 1

    # 边界：端点相接不算重叠
    assert s.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4]]) == 0

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心：**按右端点排序**，然后「能留就留，留不下就丢」。
#    为什么按右端点：区间结束越早，给后面留的空间越大。
#    按左端点排是错的——[[1,100],[2,3],[4,5]] 会让大区间排在最前，
#    把两个本来互不冲突的小区间都挤掉。
# 2. 为什么 `end = finish` 而不是 `end = max(end, finish)`：
#    排过序后，新的 finish 一定 >= 当前的 end，所以直接赋值即可。
#    写成 max 虽然结果一样，但会让人误以为"边界在扩张"，
#    而"扩张边界"正是 v1 那种错误思路的特征。
# 3. 判断用 `start >= end` 而不是 `start > end`：
#    题目明确说「只在一点上接触的区间是不重叠的」，
#    [1,2] 和 [2,3] 可以共存，所以要用 >=。
# 4. `end` 必须记录「最后保留的那个区间的右端」，
#    不能退化成「上一个区间的右端」——因为被丢弃的区间会污染判断。
#    反例：[[1,5],[2,3],[4,6]] 排序后 [[2,3],[1,5],[4,6]]，
#    如果用相邻比较：[4,6] 的起点 4 < [1,5] 的右端 5，会误判成重叠（多算 1）。
#    见 solution_v3.py 的错误示范。
# 5. 复杂度：排序 O(n log n) + 遍历 O(n) = O(n log n)，这是下界
#    （必须排序才能保证贪心正确）。空间 O(1)（原地排序，不算排序内部开销）。
# 6. 与 LC452（用最少数量的箭引爆气球）几乎同题，区别是 452 问「最少箭数」，
#    这题问「最少移除数」。核心都是「按右端点排序 + 贪心保留」。
