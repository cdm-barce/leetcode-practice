# LeetCode 242. 有效的字母异位词（简单）
# 套路：定长计数数组（字符映射下标），O(n) 时间 / O(1) 空间
# 2026-09-08
# 最优代码（面试首推：先写这版，再补一句实际工程会用 Counter）
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # 长度不同必然不是异位词，一次 O(1) 的廉价剪枝
        if len(s) != len(t):
            return False

        cnt = [0] * 26          # 26 个格子，cnt[0] 记 a 的个数，cnt[25] 记 z 的个数
        for c in s:
            # ord('a') = 97，小写字母 a~z 的码点连续（97~122），
            # 减掉 ord('a') 就把 97~122 平移到了下标 0~25
            cnt[ord(c) - ord('a')] += 1     # 进货

        for c in t:
            i = ord(c) - ord('a')
            cnt[i] -= 1                     # 出货
            # 出现负数说明 t 里这个字符比 s 多（或在 s 中根本没有），提前返回
            if cnt[i] < 0:
                return False

        # 长度相等 + 没有任何格子为负 = 所有格子恰好抵消为 0
        return True


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.isAnagram("anagram", "nagaram") is True
    assert s.isAnagram("rat", "car") is False
    # 边界用例
    assert s.isAnagram("", "") is True              # 两个空串
    assert s.isAnagram("a", "ab") is False          # 长度不等，走剪枝分支
    assert s.isAnagram("ab", "ba") is True          # 两字符互换
    assert s.isAnagram("aacc", "ccac") is False     # 长度相等但 c 的数量不同，靠 < 0 提前返回
    assert s.isAnagram("zzz", "aaa") is False       # 首尾字母边界：z 的下标 25 不越界
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 定长 26 数组只对 a~z 成立。若题目说「含 Unicode 字符」，
#    ord(c) - ord('a') 会算出负数或越界下标，必须改用 Counter（见 v3）。
#    面试时可以主动说出这个适用边界，是加分项。
#    实测：写 assert 时手滑加了 ("Aa", "aA")，直接
#      IndexError: list index out of range
#    因为 ord('A') - ord('a') = -32，cnt[-32] 对长度 26 的列表越界。
#    这版只覆盖小写字母，是刻意的取舍，不是漏判。
# 2. [0] * 26 是安全的，因为 int 不可变，26 个格子各自独立。
#    但 [[0] * 26] * 2 这种二维写法复制的是引用，改一行会污染所有行，
#    二维表必须用 [[0] * 26 for _ in range(2)]。
# 3. 第二个循环里的 `if cnt[i] < 0` 是提前剪枝，不是必须的
#    （末尾 all(v == 0 for v in cnt) 也能判），但能省掉无谓扫描。
# 4. 复杂度：时间 O(n)（两趟独立遍历），空间 O(1)（26 是常数，与 n 无关）。
#    相比 v1 的排序 O(n log n)，这是这题的最优解。
