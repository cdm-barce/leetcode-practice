# LeetCode 739. 每日温度（中等）
# 套路：单调栈（栈存下标，遇到更高温度就弹出并结算距离），O(n) 时间 / O(n) 空间
# 2026-10-28
# 最优代码

class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        index_stack = []                    # 只存下标，不存温度值
        n = len(temperatures)
        answer = [0] * n                    # 默认 0：之后没有更高温度的位置保持 0

        for i in range(n):
            # 当前温度比栈顶那天高，说明栈顶那天「等到了」
            # 用严格小于：相等不算「更高」，不能写成 <=
            while index_stack and temperatures[index_stack[-1]] < temperatures[i]:
                j = index_stack.pop()
                answer[j] = i - j           # 相隔天数 = 当前下标 - 那天的下标
            index_stack.append(i)           # 自己也要入栈，等着后面更高的温度

        return answer


if __name__ == "__main__":
    s = Solution()

    # 官方用例 1
    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]

    # 官方用例 2：单调递增，每天都等一天
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]

    # 官方用例 3
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]

    # 边界：单元素
    assert s.dailyTemperatures([50]) == [0]

    # 边界：严格递减，全都等不到
    assert s.dailyTemperatures([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]

    # 边界：全部相同（验证严格小于，相等不算更高）
    assert s.dailyTemperatures([70, 70, 70]) == [0, 0, 0]

    # 边界：连续相同后突然升高，前面的相同值都要等到那一天
    assert s.dailyTemperatures([73, 73, 75]) == [2, 1, 0]

    # 边界：两元素
    assert s.dailyTemperatures([1, 2]) == [1, 0]
    assert s.dailyTemperatures([2, 1]) == [0, 0]

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. while 的条件必须是严格小于 `<`。题目要「更高的温度」，相等不算。
#    写成 `<=` 的话 [73, 73, 75] 会被算成 [1, 1, 0]，正确答案是 [2, 1, 0]。
# 2. 栈里必须存「下标」而不是「温度值」。存值的话虽然能判断谁更高，
#    但算不出相隔几天——答案要的是距离，不是温度本身。
# 3. 复杂度为什么是 O(n) 而不是 O(n²)：虽然代码里是两层循环，但每个下标
#    最多进栈一次、出栈一次，while 内部总共执行不超过 n 次，均摊下来是线性的。
# 4. answer 初始化为 0，末尾那些始终没被弹出的位置正好就是「后面没有更高温度」，
#    不用额外处理。
# 5. 微优化：把 `for i in range(n)` + `temperatures[i]` 换成
#    `for i, cur in enumerate(temperatures)` 可以少一次索引查找，实测快约 2%，
#    量大时可以考虑，但可读性差不多，用哪个都行。
# 6. 这题和 LC239（滑动窗口最大值）同属单调栈/单调队列家族：
#    239 维护的是「窗口内的最大值」，739 维护的是「尚未找到更高温度的那批下标」。
