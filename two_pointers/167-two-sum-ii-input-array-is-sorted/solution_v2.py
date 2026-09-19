# LeetCode 167. 两数之和 II - 输入有序数组（中等）
# 套路：对撞双指针 —— 反面教材，把「长度」当成了「下标」，运行时 IndexError
# 2026-09-19
# 我的解答（错误示范，保留以记录 bug）


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        L = 1
        R = len(numbers)                        # ← len(numbers) = 4 是「元素个数」，不是合法下标
        while L < R:
            sum = numbers[L] + numbers[R]       # ← 报错点：numbers[4] 不存在
            if sum == target:
                return [L, R]
            elif sum < target:
                L += 1
            else:
                R -= 1
        return []


if __name__ == "__main__":
    s = Solution()
    try:
        s.twoSum([2, 7, 11, 15], 9)
        print("居然没报错？（不应发生）")
    except IndexError as e:
        print("预期报错 ✓ IndexError:", e)
        print("根因：合法下标是 0 ~ len-1 = 3，而 R = 4 指向了「墙外」")

# 踩坑记录：
# 1. 【下标越界】R = len(numbers) 得到 4，那是「有几个元素」；合法下标只有 0 ~ 3，
#    于是 numbers[R] 等于问「第 5 个是谁」，抛 IndexError: list index out of range。
#    记牢这一对：长度 = 个数，最大下标 = 长度 - 1，两者永远差 1（经典的 off-by-one）。
# 2. 【坐标系混用】L = 1 是照题面 1-based 起的，R = len(numbers) 也是 1-based 的边界值，
#    可 numbers[L] / numbers[R] 走的是 Python 0-based 下标 —— 一段代码里塞了两套坐标系。
# 3. 【静默错误】就算把 R 改成 len(numbers) - 1，L = 1 依然会让左指针跳过 numbers[0]，
#    而示例 1 的答案之一恰好就是 numbers[0] = 2 —— 这一版即使不报错也是错的（WA）。
#    一个报错、一个不报错，两个都得改。
# 4. 正确写法见 solution_v3.py：指针统一 0-based，只在 return 时 +1 换回 1-based。
