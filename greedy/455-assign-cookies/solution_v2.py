# LeetCode 455. 分发饼干（简单）
# 套路：排序 + 双指针贪心（最小饼干喂最小胃口）
# 2026-11-01
# 我的第二版（逻辑全对，但 sort 少了括号，排序根本没执行）

class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        s.sort()            # 原本写成 s.sort（缺括号），等于什么都没做
        g.sort()            # 同上
        ans = 0
        i = j = 0
        while i < len(g) and j < len(s):
            if g[i] <= s[j]:        # 这块饼干能喂饱当前孩子
                ans += 1
                i += 1
                j += 1
            else:                    # 饼干太小，换下一块更大的
                j += 1
        return ans


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1
    assert s.findContentChildren([1, 2, 3], [1, 1]) == 1

    # 官方示例 2
    assert s.findContentChildren([1, 2], [1, 2, 3]) == 2

    # 乱序输入（v1 会错，这版必须对）
    assert s.findContentChildren([1, 3], [3, 2]) == 2

    # 逆序输入
    assert s.findContentChildren([10, 9, 8, 7], [5, 6, 7, 8]) == 2

    # 饼干全太小
    assert s.findContentChildren([5], [1]) == 0

    # 一块大饼干喂一个小胃口
    assert s.findContentChildren([1], [5]) == 1

    # 空数组
    assert s.findContentChildren([], [1, 2]) == 0
    assert s.findContentChildren([1, 2], []) == 0

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 这版最大的坑不是逻辑，而是 `s.sort` 少了括号——它只是「取到方法对象」，
#    不会执行排序，而且**不报错不警告**，完全静默。
#    判断方法：看到没有括号的方法名，就说明没有被调用。
# 2. `sort()` 是原地排序并返回 None，所以 `s = s.sort()` 会让 s 变成 None。
#    要么用 `s.sort()`，要么用 `s = sorted(s)`。
# 3. 双指针的移动规则是这题的核心：
#    能喂饱 → 孩子和饼干都往后走（i++ 且 j++）
#    喂不饱 → 只换饼干（j++），孩子不动
# 4. 为什么这样贪心是对的：最小的饼干如果连胃口最小的孩子都喂不饱，
#    那它对任何孩子都没用，只能丢弃；如果喂得饱，用它是最省的选择，
#    因为更大的饼干还能留给胃口更大的孩子。
# 5. 更简洁的单指针写法见 solution_v3.py（省掉 j 和 ans，性能还快 15%）。
