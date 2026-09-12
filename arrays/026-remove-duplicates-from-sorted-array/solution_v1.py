# LeetCode 26. 删除有序数组中的重复项（简单）
# 套路：相邻比较 + len(set) 交差 —— 反面教材，运行时 IndexError，且从未真正搬移元素
# 2026-09-12
# 我的解答（错误示范，保留以记录 bug）
from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        :param nums: 非严格递增排列的数组（原地删除重复元素）
        :return k: 去重后数组的长度
        """
        if not nums:
            return 0
        for i in range(len(nums)):            # 崩点：i 会一直走到 len(nums) - 1
            if nums[i] > nums[i + 1]:         # 此时 nums[i + 1] 越界 → IndexError
                j = i + 1
                nums[i + 1] = nums[j]         # 就算真执行了，也是自己赋值给自己
        return len(set(nums))                 # 只算出了「数量」，数组内容一个都没动


def safe_variant(nums: List[int]) -> int:
    """只把越界修掉（range 减 1），其余原样保留，用来暴露第二个问题"""
    if not nums:
        return 0
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            j = i + 1
            nums[i + 1] = nums[j]
    return len(set(nums))


if __name__ == "__main__":
    s = Solution()

    # 问题一：官方用例直接崩
    try:
        s.removeDuplicates([1, 1, 2])
        raise AssertionError("本应抛 IndexError")
    except IndexError as e:
        print("反例 1 ✓ 官方用例直接崩溃：IndexError:", e)

    # 问题二：就算修掉越界，也只改对了数量，内容没去重
    n = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = safe_variant(n)
    assert k == 5                              # 数量确实是 5
    assert n[:k] == [0, 0, 1, 1, 1]            # 但前 k 个元素根本没有去重
    print("反例 2 ✓ 修掉越界后 k =", k, "，nums 前 k 个却是", n[:k], "，判题要求 [0, 1, 2, 3, 4]")


# 踩坑记录
# 1. 【越界】for i in range(len(nums)) 里访问 nums[i + 1]，i = len(nums)-1 时必然越界。
#    只要写「和下一个元素比」的循环，上界就要写成 len(nums) - 1，
#    或者干脆用 range(1, len(nums)) 让下标从 1 开始、跟前一个比（见 solution_v2.py）。
# 2. 【条件恒假】数组是「非严格递增」的，nums[i] > nums[i+1] 永远不会成立，
#    所以循环体一次都没执行。想找重复应该用 != 或者 < 以外的判断方向想清楚。
# 3. 【自赋值】j = i + 1 之后写 nums[i + 1] = nums[j]，等价于把元素赋给它自己，
#    这行从头到尾没有任何效果——典型的「写了但没做」。
# 4. 【最关键的认知错误】return len(set(nums)) 只回答了「有几个不重复的数」，
#    但这道题的判题器除了检查 k，还会检查 nums 的前 k 个元素是不是去重后的有序结果。
#    原地删除类题目的交付物有两个：返回值 k + 被真实修改过的数组，缺一不可。
# 5. 【截图误导】LeetCode 页面右下角显示的「通过」是历史提交留下的结果，
#    编辑器里改了代码不会立刻重跑。判断代码好坏要以实际运行为准，别信残留状态。
# 6. 正确写法见 solution_v2.py：快慢双指针，一趟扫描，O(n) 时间 / O(1) 空间。
