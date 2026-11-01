# LeetCode 455. 分发饼干（简单）
# 套路：排序 + 单指针贪心（i 同时兼任「计数器」和「孩子指针」）
# 2026-11-01
# 最优代码，O(n log n) 时间 / O(1) 额外空间（排序占主导）

class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        g.sort()        # 孩子胃口从小到大
        s.sort()        # 饼干大小从小到大

        i = 0           # 已喂饱的孩子数 == 下一个待喂孩子的下标 g[i]
        for cookie in s:
            # i < len(g) 是防越界：孩子全喂饱后 g[i] 会下标越界
            # 必须写在前面，靠短路求值挡住后面的 g[i]
            if i < len(g) and cookie >= g[i]:
                i += 1

        return i


if __name__ == "__main__":
    sol = Solution()

    # 官方示例 1
    assert sol.findContentChildren([1, 2, 3], [1, 1]) == 1

    # 官方示例 2
    assert sol.findContentChildren([1, 2], [1, 2, 3]) == 2

    # 乱序（不排序会错）
    assert sol.findContentChildren([1, 3], [3, 2]) == 2

    # 逆序
    assert sol.findContentChildren([10, 9, 8, 7], [5, 6, 7, 8]) == 2

    # 边界：饼干全太小 / 一块大饼干喂一个孩子
    assert sol.findContentChildren([5], [1]) == 0
    assert sol.findContentChildren([1], [5]) == 1

    # 边界：空数组
    assert sol.findContentChildren([], [1, 2]) == 0
    assert sol.findContentChildren([1, 2], []) == 0

    # 边界：完全匹配
    assert sol.findContentChildren([1, 2, 3], [3, 2, 1]) == 3

    # 边界：饼干远多于孩子
    assert sol.findContentChildren([1, 1], [1, 1, 1, 1]) == 2

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心简化：**i 同时是「计数器」和「指针」**。
#    v2 里 ans 和 i 永远同时 +1，所以它们恒等，可以合并成一个变量。
#    合并后省掉 j（for 自动遍历饼干），代码从 8 行降到 6 行。
# 2. `i < len(g)` 必须写在 `and` 前面。
#    如果写成 `cookie >= g[i] and i < len(g)`，孩子喂完时 g[i] 先求值就 IndexError 了。
#    短路求值的顺序是有实际意义的，不是随便排。
# 3. 实测（3000×3000 随机数据）：
#    while 双指针 + ans  1.617 ms
#    for 单指针          1.368 ms  ← 快 15%
#    原因：for 的迭代在 C 层完成，比 while 每轮比较 len 快；而且少一个变量自增。
# 4. 复杂度：排序 O(n log n) + 遍历 O(n) = O(n log n)，这是理论下界。
#    想降到 O(n) 只能靠计数排序，但这题 g[i] 最大到 2^31，数组开不出来。
# 5. 这是「排序 + 单指针贪心」模板的入门题，同族还有：
#    - LC392 判断子序列：条件从 >= 改成 ==（你之前做过，双指针版就是这题的变体）
#    - LC524 最长子序列：同上，逐个字符串查
#    - LC881 救生艇：同样排序，但双指针从两端向中间走（方向相反）
