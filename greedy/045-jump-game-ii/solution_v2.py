# LeetCode 45. 跳跃游戏 II（中等）
# 套路：贪心（紧凑写法 —— 把 n==1 的边界内化到循环范围里）
# 2026-11-04
# 变体：省掉特判和 break，循环只到倒数第二个元素

class Solution:
    def jump(self, nums: list[int]) -> int:
        far = end = steps = 0
        for i in range(len(nums) - 1):      # 注意：-1，不遍历最后一个元素
            far = max(far, i + nums[i])
            if i == end:
                end = far
                steps += 1
        return steps


if __name__ == "__main__":
    s = Solution()

    assert s.jump([2, 3, 1, 1, 4]) == 2
    assert s.jump([2, 3, 0, 1, 4]) == 2
    assert s.jump([0]) == 0
    assert s.jump([1]) == 0
    assert s.jump([2, 1]) == 1
    assert s.jump([3, 0, 0, 0]) == 1
    assert s.jump([1, 1]) == 1
    assert s.jump([1, 2, 3]) == 2
    assert s.jump([1, 2, 1, 1, 1]) == 3
    assert s.jump([1, 1, 1, 1]) == 3

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 为什么循环到 len(nums)-1 而不是 len(nums)：
#    最后一个元素是终点，站上去就结束了，不存在「从它再跳一次」的情况。
#    少遍历一个，也顺便解决了 n == 1 的边界——
#    n=1 时 range(0) 一次都不执行，直接返回 0，不需要特判。
# 2. 因为没有 break，程序会一直走到 len-2 才停。
#    虽然多跑几次循环，但省掉了每轮的 break 判断，实际差别很小。
# 3. 这个版本比 v1 少 4 行（去掉特判 + 去掉 break + 去掉 n 变量），
#    但可读性略降——"为什么要减 1"需要想一下才明白。
#    v1 更显式，这个更紧凑，看个人偏好。
# 4. steps 用了复数命名（表示次数），比 v1 的 step 更贴切。
