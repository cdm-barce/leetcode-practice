# LeetCode 452. 用最少数量的箭引爆气球（中等）
# 套路：按右端点排序 + 贪心（一支箭尽量多穿几个）
# 2026-11-10
# 我的解答（逻辑正确，但 `-inf` 会 NameError）

class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        points.sort(key=lambda x: x[1])   # 按右端点排序
        count = len(points)               # 初始当成「每个气球各一箭」
        end = -inf                        # 错：-inf 不是 Python 内置名

        for start, finish in points:
            if start > end:               # 和当前箭的位置不重叠，需要新的一箭
                end = finish
            else:                         # 能被这支箭穿到，省下一箭
                count -= 1
        return count


if __name__ == "__main__":
    # 这行会直接报错，保留下来作为证据
    try:
        Solution().findMinArrowShots([[1, 2], [2, 3]])
        print("意外：没有报错")
    except NameError as e:
        print(f"直接运行会报错：{e}")
        print("  原因：`inf` 不是 Python 内置变量，要写 float('-inf')")

    print()
    print("把 -inf 换成 float('-inf') 后，逻辑完全正确：")
    print("  if start > end  →  需要新的一箭，end 更新")
    print("  else            →  能被穿到，count -= 1")


# 踩坑记录：
# 1. 逻辑完全正确：排序键是右端点、count 初始为总数、重叠时递减，
#    本质是「数不重叠的组数」= 「需要的箭数」。
# 2. `-inf` 不是 Python 内置名字，必须写 `float('-inf')`
#    或者 `from math import inf` 之后再用 `-inf`。
#    这行在函数体里，所以导入时不报错，**只有调用时才 NameError**——
#    比语法错误更隐蔽。
# 3. `start > end` 而不是 `start >= end`，这是这题和 435 最大的区别：
#    题目要求「x_start <= X <= x_end 则引爆」，所以端点相接算重叠。
#    [[1,2],[2,3]] 在 x=2 射一箭就能同时引爆，答案 1。
#    如果写成 >= 会得到 2，错。
# 4. 修正版见 solution_v2.py（顺便把「总数减」换成「直接数箭」，语义更直观）。
