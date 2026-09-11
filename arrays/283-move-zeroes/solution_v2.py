# LeetCode 283. 移动零（简单）
# 套路：sort + 边遍历边 append/remove —— 反面教材，LeetCode 提交「解答错误」
# 2026-09-11
# 我的解答（错误示范，保留以记录 bug）
from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        nums.sort()                    # 致命错误：排序改变了非零元素的相对顺序
        for x in nums:                 # 高危写法：遍历列表的同时还在 append/remove 修改它
            if x == 0:
                nums.append(x)         # 尾部再加一个 0
                nums.remove(x)         # 删掉「第一个」值为 0 的元素


if __name__ == "__main__":
    s = Solution()
    nums = [2, 1, 0, 3, 12]
    s.moveZeroes(nums)
    assert nums == [1, 2, 3, 12, 0]    # 这是本版的实际输出，也正是它 WA 的证据
    print("反面演示 ✓ 输出", nums, "，而正确答案应为 [2, 1, 3, 12, 0]")


# 踩坑记录
# 1. 【WA 根因】题目要的是「把 0 挪到末尾，同时保持非零元素的相对顺序」，
#    不是「排序」。sort 会把 2 和 1 排成 1、2，顺序当场就毁了。
#    示例 [0,1,0,3,12] 恰好非零部分已经有序，所以样例能过、隐藏用例挂掉，
#    这是最难自查的一类错：本地测试全绿，提交爆红。
# 2. 【第二个隐患】for x in nums 遍历的同时 append / remove 修改列表，
#    会让迭代器继续往后读却读到已经错位的数据（Python 列表迭代按索引推进）。
#    行为难以预测，属于必须避免的写法。真要边遍历边改，用 while + 显式下标，
#    或者保证只用 nums[:] 遍历副本。
# 3. 教训：看到「移动」「保持顺序」这类词，先问自己——我要做的是排序吗？
#    只有题目明确要求有序才排。移动类问题优先想双指针。
# 4. 正确写法见 solution_v3.py。
