# LeetCode 84. 柱状图中最大的矩形（困难）
# 套路：单调栈 + 末尾哨兵（每根柱子轮流当「最短板」，结算它能撑起的最大宽度）
# 2026-10-29
# 最优代码，O(n) 时间 / O(n) 空间

class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []          # 存下标，对应高度从栈底到栈顶严格递增
        res = 0

        # 末尾补一个高度 0 的哨兵：它比所有柱子都矮，会把栈里剩下的元素全部逼出来，
        # 于是「收尾结算」那段循环就不需要单独写了
        for i, h in enumerate(heights + [0]):
            # 当前柱子比栈顶矮，说明栈顶那根柱子的右边界到了
            while stack and heights[stack[-1]] > h:
                mid = stack.pop()                    # 被左右夹住的那根，它是区间内最矮的
                left = stack[-1] if stack else -1    # 左边界；栈空说明左边没有更矮的，视为 -1
                width = i - left - 1                 # 右边界 i 与左边界 left 都不含
                res = max(res, heights[mid] * width) # 高度只能取 mid 自己，它是短板
            stack.append(i)

        return res


if __name__ == "__main__":
    s = Solution()

    # 官方用例
    assert s.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10

    # 官方示例 2
    assert s.largestRectangleArea([2, 4]) == 4

    # 边界：两等高的柱子拼起来
    assert s.largestRectangleArea([1, 1]) == 2

    # 边界：中间夹一个 0，把柱子切成两段
    assert s.largestRectangleArea([4, 2, 0, 3, 2, 5]) == 6

    # 边界：两端各高中间低
    assert s.largestRectangleArea([2, 1, 2]) == 3

    # 边界：单根柱子
    assert s.largestRectangleArea([6]) == 6

    # 边界：全是 0
    assert s.largestRectangleArea([0, 0]) == 0

    # 边界：严格递增（最容易漏掉收尾的情况）
    assert s.largestRectangleArea([1, 2, 3, 4, 5]) == 9

    # 边界：严格递减
    assert s.largestRectangleArea([5, 4, 3, 2, 1]) == 9

    # 边界：全等高，整排一起撑
    assert s.largestRectangleArea([2, 2, 2, 2]) == 8

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心模型：每个矩形一定以某根柱子的高度为高（再高就会被更矮的柱子挡住）。
#    所以只需枚举「每根柱子作为最矮那根时，能向右向左延伸多远」，取最大面积。
#    单调栈维护的就是这批「还没找到右边更矮柱子」的候选，按高度递增排列。
# 2. 宽度的统一写法：`left = stack[-1] if stack else -1`，然后 `width = i - left - 1`。
#    栈空时 left = -1，宽度正好等于 i，不用 if/else 分两套算法。
# 3. 末尾加 0 当哨兵，是最省事的收尾方式。不加的话必须再写一个 while 循环
#    把栈里剩余下标逐个弹出结算（宽度延伸到数组末尾）。
# 4. 判断条件用 `>`（严格大于）而不是 `>=`。用 `>=` 遇到等高柱子会提前弹出，
#    虽然多数情况结果不变，但会多算重复矩形，逻辑不够干净。
# 5. 最容易绕晕的概念：mid 在**栈里**是最高（栈递增、它是栈顶），
#    在**它负责的区间**里却是最矮（左右边界都比它矮，否则不会被夹住弹出）。
#    两个「最」说的是不同范围——栈是候选集，区间是实际可铺开的范围。
# 6. 与 LC739（每日温度）同族：都是「找右边第一个更矮/更高」的模板。
#    739 是求距离，84 是求面积，骨架只差结算方式。
# 7. 复杂度：每个下标进栈一次、出栈一次，while 内部总计不超过 n 次，所以是 O(n) 而非 O(n²)。
