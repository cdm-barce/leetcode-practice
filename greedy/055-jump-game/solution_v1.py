# LeetCode 55. 跳跃游戏（中等）
# 套路：贪心 —— 只维护「当前能到达的最远下标」，不关心具体怎么跳
# 2026-11-02
# 最优代码，O(n) 时间 / O(1) 空间（时间和空间都是理论下界）

class Solution:
    def canJump(self, nums: list[int]) -> bool:
        n = len(nums)
        far = 0                     # 当前能到达的最远下标
        for i in range(n):
            if far < i:             # 当前位置已经超出可达范围，说明中间断了
                return False
            far = max(far, i + nums[i])   # 站在 i 能摸到的最远点
        return True


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1：能到
    assert s.canJump([2, 3, 1, 1, 4]) is True

    # 官方示例 2：中间有 0 卡住，到不了
    assert s.canJump([3, 2, 1, 0, 4]) is False

    # 边界：只有一个元素，本来就在终点
    assert s.canJump([0]) is True
    assert s.canJump([1]) is True

    # 边界：第一步就跳不动
    assert s.canJump([0, 1]) is False

    # 边界：全 0（除第一个）
    assert s.canJump([1, 0, 0]) is False

    # 边界：一次跳到底
    assert s.canJump([5, 0, 0, 0, 0]) is True

    # 边界：刚好卡在最后一步
    assert s.canJump([2, 0, 0]) is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心认知：**不要模拟「怎么跳」**。枚举所有跳法是指数级爆炸
#    （nums=[5,5,5,...] 十来个元素就有上百万条路径）。
#    这题只问「能不能到」，信息需求少，所以只需要维护「最远能到哪」这一个变量。
# 2. far 的物理含义：**下标**，不是「还剩几步」。
#    写成「剩余步数」那种写法（每走一步 -1，遇到更大的就取较大值）也能过，
#    但容易把「步数」和「位置」搞混，用下标最不容易错。
# 3. 差一问题：`if far < i` 不能写成 `if far <= i`。
#    far == i 表示「恰好能站在 i 上」，是合法的；写成 <= 会误判。
# 4. 复杂度：每个元素访问一次，O(n)；只用两个变量，O(1)。
#    想更快只能靠提前退出（见 solution_v2.py），但那不是普遍更优。
# 5. 与 LC45（跳跃游戏 II，求最少步数）的关系：
#    45 要在这题基础上多维护一个「当前这一步的边界 end」，
#    每走到 end 就必须跳一次。55 只要判断能不能，45 才求最少几步。
# 6. 为什么不推荐 DFS/BFS/DP：
#    DFS 天真实现会指数爆炸；BFS 加 visited 能 O(n) 但要队列+数组，代码量三倍；
#    DP 是 O(n²)。贪心用一个变量办了同样的事。
