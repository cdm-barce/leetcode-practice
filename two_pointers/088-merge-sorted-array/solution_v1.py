# LeetCode 88. 合并两个有序数组（简单）
# 套路：尾部填 nums2 + 原地 sort()，O((m+n)log(m+n)) 最坏 / 实测 Timsort 退化为 O(m+n)
# 2026-09-20
# 我的解答（改进版）：用切片赋值 nums1[m:] = nums2 替代手写 for 循环

class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        # nums1 的后 n 格（下标 m..m+n-1）本来就是预留的空闲区。
        # 把 nums2 整体塞进这一段，再用 sort() 把整段排好序即可。
        # 切片赋值 nums1[m:] = nums2 在 C 层执行，比手写 for 还快，也更符合 Python 惯例。
        # （原写法 for i in range(m, len(nums1)): nums1[i] = nums2[i-m] 多维护一个 j 变量，
        #  且依赖 "len(nums1) 恰好等于 m+n" 这个隐含约定，意图写得不如这里清楚。）
        nums1[m:] = nums2

        # 整段排序。输入是「nums1[:m] 有序」+「nums2 有序」两段，CPython 的 Timsort 会
        # 扫描出这两段连续有序 run，退化为一次归并 O(m+n)；但理论最坏复杂度仍是
        # O((m+n)log(m+n))，且 sort() 需要 O(min(m,n)) 的临时工作空间。
        nums1.sort()


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    nums1 = [1, 2, 3, 0, 0, 0]
    s.merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

    # 边界：nums2 为空（m 覆盖整个 nums1）
    nums1 = [1]
    s.merge(nums1, 1, [], 0)
    assert nums1 == [1]

    # 边界：nums1 有效部分为空（m=0），结果全来自 nums2
    nums1 = [0]
    s.merge(nums1, 0, [1], 1)
    assert nums1 == [1]

    # 边界：两数组单元素，nums1 末尾更大
    nums1 = [2, 0]
    s.merge(nums1, 1, [1], 1)
    assert nums1 == [1, 2]

    # 两数组元素有重复
    nums1 = [1, 2, 3, 0, 0, 0]
    s.merge(nums1, 3, [2, 2, 2], 3)
    assert nums1 == [1, 2, 2, 2, 2, 3]

    # 负数
    nums1 = [-1, 0, 0, 3, 0, 0, 0]
    s.merge(nums1, 4, [-1, -1, 2], 3)
    assert nums1 == [-1, -1, -1, 0, 0, 2, 3]

    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【多余变量】原写法的 for i in range(m, len(nums1)): nums1[i] = nums2[j]; j += 1，
#    里 j 完全冗余：nums2 的下标就是 i - m，可写成 nums1[i] = nums2[i - m]，少维护一个变量。
# 2. 【隐含约定】循环上界用 len(nums1) 依赖「len(nums1) 恰好等于 m+n」这一题目保证的约定，
#    换成 m + n 把意图显式写出来，更稳也更好读（题目确实保证，但写出来不亏）。
# 3. 【切片替代 for】nums1[m:] = nums2 一行即可完成「填尾部」，
#    切片赋值在 C 层执行，比手写 for 更快，是 Python 惯例写法。
# 4. 【思路层面】这版的真正短板不是写法，而是用 sort() 把「输入已有序」这个免费条件浪费了：
#    理论最坏 O((m+n)log(m+n))，且额外吃 O(min(m,n)) 空间。
#    —— 真正的最优解见 solution_v2.py（三指针从后往前，O(m+n)/O(1)）。
# 5. 【反直觉实测】在 CPython 上本版因 Timsort 识别两段有序 run + C 层执行，
#    实际比 v2 的三指针（200 万次 Python 解释器循环）还快 3 倍左右。
#    但这是实现细节：换 Java 的 Arrays.sort（双轴快排）会直接退回 O(n log n)，且空间更亏。
#    面试官问「你这不还是排序吗」时能答出 Timsort 识别有序 run 是加分项；但只写这版、答不出三指针就是减分。
