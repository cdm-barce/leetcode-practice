# LeetCode 239. 滑动窗口最大值（困难）
# 套路：单调队列（deque 存下标，值单调递减），O(n) 时间 / O(k) 空间
# 2026-09-30
# 最优代码

from typing import List
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()   # 存下标，保证 nums[dq[0]] >= nums[dq[1]] >= ... 单调递减，队头即最大值
        ans = []

        for R in range(len(nums)):
            # ① 踢队尾：新元素进来前，把队尾所有 <= 当前值的下标全弹出。
            #    理由：它们在窗口里既「比新元素小」又「比新元素更早过期」，
            #    所以只要新元素还在，它们就永远当不了最大值，留着是废的。
            while dq and nums[dq[-1]] <= nums[R]:
                dq.pop()

            # ② 当前下标入队（从队尾进）
            dq.append(R)

            # ③ 踢队头：队头下标若已滑出窗口左边界，弹出让它「过期」。
            #    R - k + 1 是当前窗口左边界 L。
            if dq[0] < R - k + 1:
                dq.popleft()

            # ④ 窗口凑满 k 个元素后（R >= k-1），队头就是当前窗口最大值
            if R >= k - 1:
                ans.append(nums[dq[0]])

        return ans


if __name__ == "__main__":
    s = Solution()
    # 官方示例 1
    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    # 官方示例 2
    assert s.maxSlidingWindow([1], 1) == [1]
    # 边界：k=1，每个窗口只有一个元素，输出即原数组
    assert s.maxSlidingWindow([1, -1], 1) == [1, -1]
    # 边界：含负数，窗口内全为负
    assert s.maxSlidingWindow([-7, -8, 7, 5, 7, 1, 6, 0], 4) == [7, 7, 7, 7, 7]
    # 边界：元素全相同，验证踢队尾用 <= 而非 < 的重要性（见踩坑记录）
    assert s.maxSlidingWindow([1, 1, 1, 1], 2) == [1, 1, 1]
    # 边界：递减数组，窗口最大值始终是左端点
    assert s.maxSlidingWindow([5, 4, 3, 2, 1], 3) == [5, 4, 3]
    print("单调队列版用例通过 ✓")

# 踩坑记录：
# - 队列里必须存「下标」而不是「值」：第③步判断「队头是否滑出窗口」需要
#   知道这个元素还在不在窗口内，只有下标能算出来（dq[0] < R - k + 1）。
# - 第①步踢队尾用 <= 而非 <：若用 <，遇到 [1,1,1,1], k=2 这种相等元素时，
#   旧元素不会被踢掉，队里堆满重复下标，可能把已过期的元素当最大值输出，导致 WA。
# - 顺序铁律：先①踢队尾 → ②入队 → ③踢队头 → ④记答案。①②不能反，否则新元素
#   会被自己（比较自身 <= 自身成立）直接踢掉。
# - Python 知识点：collections.deque 两头操作 O(1)；dq[-1] 是队尾（负索引），
#   只是「读」不删除，删除用 pop()/popleft()；deque 支持下标访问但不支持切片。
# - 复杂度关键：每个元素最多入队一次、出队一次，while 累计 O(n)，
#   均摊到每个 R 是 O(1)，所以整体 O(n)，比暴力 O(n·k) 快两个量级。
