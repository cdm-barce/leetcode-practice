# LeetCode 438. 找到字符串中所有字母异位词（中等）
# 套路：26 位计数数组 + for...else 判负数（逻辑正确但 O(n·m) 超时）
# 2026-09-25
# 我的解答（迭代版：修好边界后逻辑全对，但每次重数窗口，TLE）

class Solution:
    def findAnagrams(self, s: str, p: str) -> list:
        n = len(s)
        m = len(p)
        ans = []
        p1 = 0

        while p1 <= n - m:                  # 边界改对：窗口起点不能越出 s
            cnt = [0] * 26                  # 每轮重置，干净开始
            for ch in p:                    # 循环变量不再遮蔽参数 s
                cnt[ord(ch) - ord('a')] += 1

            for ch in s[p1:p1 + m]:         # 窗口切对：左闭右开取满 m 格
                cnt[ord(ch) - ord('a')] -= 1

            for v in cnt:                   # for...else + break：有负数就不是异位词
                if v < 0:
                    break
            else:
                ans.append(p1)
            p1 += 1
        return ans


if __name__ == "__main__":
    s = Solution()
    # 逻辑已正确，官方 + 边界用例全部通过
    assert s.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert s.findAnagrams("abab", "ab") == [0, 1, 2]
    assert s.findAnagrams("ab", "abc") == []        # s 比 p 短
    assert s.findAnagrams("a", "a") == [0]          # 单字符
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 循环变量遮蔽（Python 特有）：早期版本写 `for s in list2` / `for s in list1`，
#    for 循环没有块级作用域，会把函数参数 s 就地覆盖成单个字符，
#    第二轮起 s[p1:p1+m] 切出空串 → 内层循环不进 → 直接走 else → 每轮都 append。
#    又因为 n = len(s) 在循环前就算好了，程序不崩，只给错误结果（报「解答错误」而非「执行错误」）。
#    修法：循环变量改名为 ch。
# 2. cnt 清零位置：cnt = [0]*26 必须放 while 里面，否则残留上一轮的值继续累加。
# 3. 复杂度仍是 O(n·m)：每轮都对窗口重新计数 + 遍历 cnt，n、m 到 3×10⁴ 时
#    约 27 亿次操作，Python 扛不住 → TLE（实测 33/65）。
#    优化关键：相邻窗口只差「一进一出」两个字符，不必整窗重数，见 v3。
