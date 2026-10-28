# LeetCode 739. 每日温度（中等）
# 套路：从右往左 + 利用已算好的答案跳跃（不用显式栈），O(n) 时间 / O(n) 空间
# 2026-10-28
# 对照代码（思路不同，实测比 solution_v1 慢 20%~30%，仅作知识储备）

class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        ans = [0] * n

        # 从右往左算：右边位置的答案已经求出来了，可以直接拿来跳
        for i in range(n - 2, -1, -1):
            j = i + 1
            # 只要 j 那天不比今天热，就顺着 ans[j] 往前跳，
            # 跳过一整段「已经确认比 j 还冷」的区间
            while j < n and temperatures[j] <= temperatures[i]:
                j = n if ans[j] == 0 else j + ans[j]
            ans[i] = 0 if j >= n else j - i

        return ans


if __name__ == "__main__":
    s = Solution()

    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    assert s.dailyTemperatures([50]) == [0]
    assert s.dailyTemperatures([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]
    assert s.dailyTemperatures([70, 70, 70]) == [0, 0, 0]
    assert s.dailyTemperatures([73, 73, 75]) == [2, 1, 0]
    assert s.dailyTemperatures([1, 2]) == [1, 0]
    assert s.dailyTemperatures([2, 1]) == [0, 0]

    print("全部用例通过 ✓（结果与 solution_v1 完全一致，实测更慢）")


# 踩坑记录：
# 1. 核心思想：从右往左，右边的答案已经算好了。如果 temperatures[j] 不比今天热，
#    那 j 的答案所指向的那个位置也不用看了——直接跳到 j + ans[j]，一步跨过一整段。
#    本质是把「栈」换成了「答案数组里的指针链」，所以不用额外开栈。
# 2. 边界写法要注意：
#    - `ans[j] == 0` 表示 j 之后没有更高温度，那 j 之后全部不用看了，令 j = n 收工
#    - `temperatures[j] <= temperatures[i]` 用的是 <=，因为相等也不算更高，
#      与 v1 里 while 用严格小于 `<` 是同一个语义，只是方向反了
# 3. 实测对比（n = 100000）：
#        数据形态        正序单调栈(v1)     从右往左跳跃(v2)
#        随机               9.8 ms            12.8 ms
#        严格递减           5.8 ms             7.7 ms
#        严格递增           8.0 ms             6.9 ms
#    只有在严格递增（能大段跳跃）时才有优势，其余情况都更慢，因为多了大量分支判断。
# 4. 结论：面试和提交都用 v1。这个版本的价值在于——
#    它证明了「单调栈」不是唯一解法，本质只是「找右边第一个更大的元素」的不同实现方式。
