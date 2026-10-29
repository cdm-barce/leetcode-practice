# LeetCode 84. 柱状图中最大的矩形（困难）
# 套路：单调栈（初版：漏收尾 + 宽高都算错），O(n) 时间 / O(n) 空间
# 2026-10-29
# 我的解答（未通过：7 个用例错 4 个）

class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        res = 0

        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                mid = stack.pop()
                if not stack:            # 错 1：栈空直接 break，这块矩形永远算不到
                    break
                left = stack[-1]
                w = i - left             # 错 2：少减 1，右边界 i 不能算进宽度
                sh = max(heights[left], h)   # 错 3：高度应该取 heights[mid]
                res = max(res, sh * w, heights[mid])
            stack.append(i)
        # 错 4：遍历结束后栈里还有元素，全都没结算
        return res


if __name__ == "__main__":
    s = Solution()

    # 下面断言的「是本版实际输出的错误结果」，用来保留 WA 证据
    assert s.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10   # 碰巧对，掩盖了问题
    print("碰巧通过: [2,1,5,6,2,3] -> 10")

    assert s.largestRectangleArea([2, 4]) == 0
    print("反面演示 ✓ [2,4] 返回 0，正确答案应为 4（栈里元素从未被结算）")

    assert s.largestRectangleArea([1, 1]) == 0
    print("反面演示 ✓ [1,1] 返回 0，正确答案应为 2")

    assert s.largestRectangleArea([2, 1, 2]) == 0
    print("反面演示 ✓ [2,1,2] 返回 0，正确答案应为 3")

    assert s.largestRectangleArea([4, 2, 0, 3, 2, 5]) == 4
    print("反面演示 ✓ [4,2,0,3,2,5] 返回 4，正确答案应为 6")


# 踩坑记录：
# 1. 「全是 0」是最明显的信号：说明一次面积都没算出来过。
#    根因是递增序列（或末尾递增）时栈里元素从未被弹出，而循环结束后没有收尾结算。
#    [2,4] 走一遍就清楚：i=0 入栈，i=1 时 4>2 不弹，循环直接结束，栈 [0,1] 原封不动。
# 2. 宽度公式错。弹出 mid 时，右边界是 i（比 mid 矮，不含），左边界是新的栈顶 left（也矮，不含），
#    所以宽度 = i - left - 1。写成 i - left 会把右边界那根矮柱子也算进去。
# 3. 高度取错了。写 max(heights[left], h) 是想取「两边更高的那个」，
#    但矩形要铺满 (left, i) 整段，高度被区间内最矮的那根卡住——就是 mid 自己。
#    真相是：mid 被弹出，正因为它左右都比它矮，所以它在区间内必然最矮。
#    栈里它是最高（栈递增、它是栈顶），区间里它最矮，两个「最」说的是不同范围，不矛盾。
# 4. `if not stack: break` 白白丢掉了栈空这种情况。
#    栈空说明 mid 左边没有更矮的了，矩形可以从下标 0 起算，宽度就是 i。
# 5. 正确解法见 solution_v2.py：把左边界统一成 `stack[-1] if stack else -1`，
#    再补末尾哨兵 0 自动收尾，两个问题一起解决。
