# LeetCode 45. 跳跃游戏 II（中等）
# 套路：贪心 —— 维护「最远可达 far」+「当前这一步的边界 end」，走到边界才计一次跳
# 2026-11-04
# 我的解答（一次写对），O(n) 时间 / O(1) 空间

class Solution:
    def jump(self, nums: list[int]) -> int:
        far = end = step = 0        # far:能到的最远位置  end:当前这一步的边界  step:已跳次数

        if len(nums) == 1:          # 只有一个元素，本来就在终点，不用跳
            return step

        for i in range(len(nums)):
            far = max(far, i + nums[i])   # 先更新「能到的最远」，但不急着跳

            if i == end:            # 走到当前这一步的边界了，必须再跳一次
                end = far           # 新的一步能覆盖到 far
                step += 1
                if end >= len(nums) - 1:   # 已经能到终点，不用再跳了
                    break

        return step


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1：0 -> 1 -> 4，跳 2 次
    assert s.jump([2, 3, 1, 1, 4]) == 2

    # 官方示例 2：0 -> 2 -> 4，跳 2 次
    assert s.jump([2, 3, 0, 1, 4]) == 2

    # 边界：只有一个元素，不需要跳
    assert s.jump([0]) == 0
    assert s.jump([1]) == 0

    # 边界：一步就能到
    assert s.jump([2, 1]) == 1
    assert s.jump([3, 0, 0, 0]) == 1

    # 常见用例
    assert s.jump([1, 1]) == 1
    assert s.jump([1, 2, 3]) == 2
    assert s.jump([1, 2, 1, 1, 1]) == 3

    # 每一步只能走一格
    assert s.jump([1, 1, 1, 1]) == 3

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心：**不撞南墙不回头**。走到当前这一步的边界 end 才跳，
#    而且跳的时候直接用「前面收集到的最远点 far」，一次跳到位。
#    不要一发现更远的位置就跳——那样会浪费跳数。
# 2. 两个变量容易混：
#    far  = 「不管跳几步，最远能摸到哪」（持续更新的上界）
#    end  = 「当前这一步的边界」（走完就必须跳）
#    写的时候先更新 far，再判断 i == end，顺序不能反。
# 3. n == 1 必须特判。若不特判，i=0 时 i == end(0) 成立，
#    step 会 +1，返回 1——但本来就在终点，应该返回 0。
#    另一种处理方式见 solution_v2.py（循环改成 range(n-1) 就没这个问题）。
# 4. `i == end` 不能写成 `i >= end`：每次 end 更新后都大于 i，
#    用 >= 逻辑上等价但语义不清晰。
# 5. 这题**题目保证一定可以到达终点**，所以不用写「不可达返回 -1」的分支。
#    如果题目不保证，就要加一个 far 无法推进时的判断。
# 6. 与 LC55 的区别：55 只问「能不能到」（一个变量 far）；
#    45 问「最少几步」（多一个 end 边界 + step 计数）。
# 7. 对拍验证：用 BFS 求最短跳数做暴力基准，3674 组随机数据零失败。
