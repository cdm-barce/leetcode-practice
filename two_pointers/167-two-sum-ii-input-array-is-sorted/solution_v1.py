# LeetCode 167. 两数之和 II - 输入有序数组（中等）
# 套路：对撞双指针 —— 反面教材，把 Python 的 len() 写成了 Java 式的 numbers.len，运行时 AttributeError
# 2026-09-19
# 我的解答（错误示范，保留以记录 bug）


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        L = 1
        R = numbers.len          # ← 报错点：list 没有 len 属性，Python 取长度是 len(numbers)
        while L < R:
            sum = numbers[L] + numbers[R]
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
    except AttributeError as e:
        print("预期报错 ✓ AttributeError:", e)
        print("根因：Python 取长度用内置函数 len(x)，没有 x.len 这种写法")

# 踩坑记录：
# 1. 【属性错误】写成 `numbers.len`，报 `'list' object has no attribute 'len'`。
#    Python 取长度一律用内置函数 len(x)；`x.len`（Java 数组）和 `x.length()`（Java 字符串）
#    都是 Java 的写法，不能带到 Python 里来，这是两门语言最典型的串味点。
# 2. 【潜在下标错误】这版 L = 1。就算把 len 写对了，L 仍然是错的：
#    本意是「题面第 1 个元素」，但 numbers[L] 认的是 Python 下标，
#    numbers[1] 拿到的是第 2 个数 —— 详见 v2 暴露出来的 IndexError。
# 3. 【命名】变量名 sum 遮蔽了内置函数 sum()。本题没有调用 sum() 所以无碍，
#    但养成习惯后换一道题（比如要算总和）就会踩坑。
# 4. 正确写法见 solution_v3.py。
