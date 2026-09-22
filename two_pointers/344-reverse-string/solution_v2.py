# LeetCode 344. 反转字符串（简单）
# 套路：调用 list.reverse() —— 同样 O(n) / O(1)，但翻转在 C 层完成，常数更小
# 2026-09-22
# 最优代码


class Solution:
    def reverseString(self, s: list[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        s.reverse()     # list 内置方法：原地翻转，不产生新列表


if __name__ == "__main__":
    sol = Solution()

    cases = [
        (["h", "e", "l", "l", "o"], ["o", "l", "l", "e", "h"]),            # 官方示例 1
        (["H", "a", "n", "n", "a", "h"], ["h", "a", "n", "n", "a", "H"]),  # 官方示例 2
        ([], []),                                                          # 边界：空列表
        (["a"], ["a"]),                                                    # 边界：单元素
        (["a", "b"], ["b", "a"]),                                          # 边界：两元素
        (["a", "b", "c"], ["c", "b", "a"]),                                # 边界：三元素
        ([" ", "!"], ["!", " "]),                                          # 特殊字符
    ]

    for src, want in cases:
        arr = list(src)
        ret = sol.reverseString(arr)
        assert ret is None, "题目要求原地修改，不应有返回值"
        assert arr == want, f"{src} 反转后得到 {arr}，期望 {want}"

    print("全部用例通过 ✓")

# 说明：
# 1. 复杂度与 solution_v1 完全一致：时间 O(n)、额外空间 O(1)。
#    差别只在实现层——s.reverse() 由 CPython 用 C 写，翻转过程不经过 Python 解释器，
#    省掉了每轮双指针的 while 判空、下标读写与元组解包开销，所以常数因子更小。
#    这也是为什么同一份双指针代码在 LeetCode 上 0 ms 就顶到了 100%（Python 计时精度不够）。
# 2. 面试取舍：面试官想看的是你能否手写对撞双指针（solution_v1），
#    s.reverse() 属于「知道有这个内置就够」的工程写法。
# 3. 注意 s.reverse() 只对可变序列（list）有效。如果题目给的是 str，
#    str 不可变、没有 reverse()，只能靠切片或 join(reversed(s)) 生成新字符串。
