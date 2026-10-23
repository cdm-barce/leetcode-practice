# LeetCode 1094. 拼车（中等）
# 套路：差分数组（初版：站点上界取错，全部越界），O(n) 时间 / O(max_from) 空间
# 2026-10-23
# 我的解答（解答错误 67/81，含 to 的用例全部 IndexError）

from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        n = max(row[1] for row in trips)    # 致命点：只看了上车点 from，没看下车点 to
        diff = [0] * (n + 1)
        for k, L, R in trips:
            diff[L] += k
            diff[R] -= k                    # R 超过 n 就 IndexError
        for i in range(1, n):               # 顺带：range 到 n 为止，最后一站没检查
            diff[i] += diff[i - 1]
            if diff[i] > capacity:
                return False
        return True


if __name__ == "__main__":
    s = Solution()

    # 只要存在 to > max(from) 的订单，这一版必然越界
    try:
        s.carPooling([[2, 1, 5], [3, 3, 7]], 4)
        assert False, "本版本应抛 IndexError"
    except IndexError as e:
        print("反面演示 ✓ 抛 IndexError:", e)

    try:
        s.carPooling([[7, 5, 6], [6, 7, 8], [10, 1, 6]], 16)
        assert False, "本版本应抛 IndexError"
    except IndexError as e:
        print("反面演示 ✓ 抛 IndexError:", e)

    print("根因：n = max(from)，但数组还要装 diff[to]，to 比 from 大")


# 踩坑记录：
# 1. 越界根因：n 只取了 row[1]（from），而代码里要写 diff[R]，R 是 to。
#    [[2,1,5],[3,3,7]] 中 max(from)=3、max(to)=7，数组只有 4 格，diff[7] 直接崩。
#    正确应该取「所有出现过的站点」的最大值，或者干脆用题目给的上界 1000。
# 2. 第二个小问题：for i in range(1, n) 右端不含 n，最后一站没被检查。
#    虽然最后一站通常是 0 人，但逻辑上漏了。
# 3. 好消息是差分的主体思路完全正确，只是边界算错——改进见 solution_v2.py。
