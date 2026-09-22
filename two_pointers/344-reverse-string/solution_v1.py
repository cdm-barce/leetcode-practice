# LeetCode 344. 反转字符串（简单）
# 套路：对撞双指针原地交换，O(n) 时间 / O(1) 空间
# 2026-09-22
# 我的解答


class Solution:
    def reverseString(self, s: list[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        left = 0                    # 左指针：指向待交换的首元素
        right = len(s) - 1          # 右指针：指向待交换的尾元素（是 len - 1，不是 len）
        while left <= right:        # 两指针相遇（奇数长度）或交错（偶数长度）前，一直换
            s[left], s[right] = s[right], s[left]   # 同时赋值，不用临时变量也不会互相覆盖
            left += 1               # 左指针向中间收
            right -= 1              # 右指针向中间收


if __name__ == "__main__":
    sol = Solution()

    cases = [
        (["h", "e", "l", "l", "o"], ["o", "l", "l", "e", "h"]),            # 官方示例 1
        (["H", "a", "n", "n", "a", "h"], ["h", "a", "n", "n", "a", "H"]),  # 官方示例 2
        ([], []),                                                          # 边界：空列表
        (["a"], ["a"]),                                                    # 边界：单元素（中间元素自己换自己）
        (["a", "b"], ["b", "a"]),                                          # 边界：偶数长度最小规模
        (["a", "b", "c"], ["c", "b", "a"]),                                # 边界：奇数长度最小规模
        ([" ", "!"], ["!", " "]),                                          # 特殊字符
    ]

    for src, want in cases:
        arr = list(src)
        ret = sol.reverseString(arr)
        assert ret is None, "题目要求原地修改，不应有返回值"
        assert arr == want, f"{src} 反转后得到 {arr}，期望 {want}"

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【指针初始化】right 必须写 len(s) - 1。「元素个数」和「最大合法下标」永远差 1，
#    写成 len(s) 就是经典的 off-by-one，一上循环体就 IndexError（167 题刚栽过这个跟头，
#    这次没再犯）。
# 2. 【交换不丢数据】s[left], s[right] = s[right], s[left] 之所以成立，是因为 Python
#    先把右侧整体求值打包成一个元组 (s[right], s[left])，再从左到右解包赋值。
#    右侧的读取全部发生在写入之前，所以两次读到的都还是旧值。
#    换成 C / Java 就必须开一个 temp 暂存，否则第一次赋值就把数据冲掉了。
# 3. 【循环条件】left <= right 正确，但奇数长度时两指针会在最中间相遇，
#    额外跑一轮 s[mid], s[mid] = s[mid], s[mid] 的「自己和自己换」，无害但白做。
#    写成 left < right 刚好，语义也更贴切：还没相遇就该换，相遇了就收工。
#    两种写法都能 AC（本次 0 ms / 击败 100%）。
# 4. 【为什么空间是 O(1)】全程只有 left、right 两个下标变量，额外内存不随 n 增长。
#    对比 s[:] = s[::-1]：切片 s[::-1] 会先造一个长度 n 的新列表，额外空间 O(n)；
#    虽然 s[:] = 让它看起来也是「原地修改」，但内存账单已经付了。
# 5. 【题面约束】必须原地改，所以不能写 return s[::-1] —— 题目明确
#    "Do not return anything, modify s in-place instead."，
#    返回新列表在原数组未被改动时判为 WA。
# 6. 【复杂度结论】时间 Ω(n) 是下界（每个字符至少要读写一次），空间要求 O(1)，
#    对撞双指针同时踩中两条下界 —— 这题不存在复杂度更优的解，只有常数级更快的写法
#    （见 solution_v2.py）。
