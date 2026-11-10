# LeetCode 452. 用最少数量的箭引爆气球（中等）
# 套路：按右端点排序 + 贪心（直接数箭，语义更直观）
# 2026-11-10
# 最优代码，O(n log n) 时间（排序主导）/ O(1) 额外空间

class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        points.sort(key=lambda x: x[1])   # 按右端点排序：越早结束的气球越难伺候，先处理

        shots = 0
        end = float("-inf")               # 当前这支箭最远能射到哪

        for start, finish in points:
            if start > end:               # 当前箭够不到 → 必须再射一箭
                shots += 1
                end = finish              # 新箭放在这个气球的右端（最贪心的位置）
            # else: 当前箭能穿到，跳过

        return shots


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1：x=6 射一箭穿 [2,8][1,6]，x=11 穿 [10,16][7,12]
    assert s.findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2

    # 官方示例 2：四个完全分离，各需一箭
    assert s.findMinArrowShots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4

    # 官方示例 3：首尾相接，两支箭就够
    assert s.findMinArrowShots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2

    # 端点相接算重叠：x=2 一箭爆两个
    assert s.findMinArrowShots([[1, 2], [2, 3]]) == 1

    # 边界：单个气球 / 空数组
    assert s.findMinArrowShots([[1, 2]]) == 1
    assert s.findMinArrowShots([]) == 0

    # 大区间包住两个分离小区间：大区间能被任一箭打到，但两个小区间互不重叠，
    # 所以仍需 2 箭。注意和 435 的区别——435 同一个输入答案是 1（删掉大区间）。
    assert s.findMinArrowShots([[1, 100], [2, 3], [4, 5]]) == 2

    # 三个全重叠：一支箭在交集处即可
    assert s.findMinArrowShots([[1, 10], [2, 9], [3, 8]]) == 1

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 和 435 是同一个模型的两个问法，但判断条件不一样：
#      435 无重叠区间：start >= end（端点相接不算重叠）
#      452 引爆气球：  start >  end（端点相接算重叠，一箭爆两个）
#    依据：435 说「只在一点上接触的区间不重叠」；
#          452 说「x_start <= X <= x_end 则引爆」。
#    写成 >= 会少算，写成 > 在 435 会多算。**这两题一定要分开记。**
# 2. 箭放在哪里最划算：**放在当前气球的右端**（`end = finish`）。
#    因为排序后 finish 一定 >= 之前所有右端，放最右端能覆盖最多后续气球。
# 3. 为什么排序键是右端点：右端越小的气球越"早死"，必须先处理，
#    否则后面的箭射不到它。这和 435 的理由相同。
# 4. `float("-inf")` 而不是 `-inf`：后者不是 Python 内置名字，
#    在函数体里只会在调用时抛 NameError，非常隐蔽。
# 5. 用 `shots += 1` 而不是 `count = len(points)` 再递减：
#    前者读起来就是"再射一箭"，不需要在脑子里做减法转换。
#    两种等价，但前者的语义和题目问法一致。
# 6. 复杂度：排序 O(n log n) + 遍历 O(n) = O(n log n)，排序是下界。
#    空间 O(1)（原地排序）。
