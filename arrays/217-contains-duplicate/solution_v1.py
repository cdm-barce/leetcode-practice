# LeetCode 217. 存在重复元素（简单）
# 套路：list 判重 —— 反面教材，O(n²)，LeetCode 提交「超出时间限制」
# 2026-09-07
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        num = []
        for x in nums:
            if x in num:        # 关键问题：list 的 in 是逐个比对的线性扫描，O(n)
                return True
            else:
                num.append(x)
        return False


if __name__ == "__main__":
    s = Solution()
    assert s.containsDuplicate([1, 2, 3, 1]) is True
    assert s.containsDuplicate([1, 2, 3, 4]) is False
    assert s.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 本地 assert 全过，但 LeetCode 提交直接「超出时间限制」。原因不是死循环，是复杂度。
#    提示里 n 最大 10^5，O(n²) 就是 10^10 次操作，远超 1 秒能跑完的量级。
# 2. 根因：把 list 当成了哈希集合用。list 的 `x in num` 会从头扫到尾，O(n)；
#    外面再套一层 for，整体 O(n²)。正确做法见 solution_v2.py（换 set）。
# 3. 教训：做题前先看「提示」里的数据范围，倒推允许的复杂度再动手写。
#    判存在性（在不在）一律优先考虑 set / dict，不要顺手写 list。
