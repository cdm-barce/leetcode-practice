# LeetCode 3. 无重复字符的最长子串（中等）
# 套路：滑动窗口 + 哈希表记录字符最近下标，O(n) 时间 / O(min(n, 字符集)) 空间
# 2026-09-17
# 我的解答（滑动窗口最优解）

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}          # 字符 -> 它上一次出现的下标；用于判断「当前字符是否已在窗口内重复」
        left = 0           # 窗口左边界，闭区间 [left, right]
        ans = 0            # 遍历过程中遇到的最大窗口长度

        # 循环不变量：进入每一轮时，[left, right-1] 一定是一个「无重复」窗口
        for right, ch in enumerate(s):
            # ch 之前出现过，且上一次出现的位置还在当前窗口内（>= left）
            # 说明 ch 在窗口里重复了，左边界必须跳过那个旧位置
            if ch in last and last[ch] >= left:
                left = last[ch] + 1     # 关键：left 「跳」到重复字符的下一位，而非 +1 慢慢挪
            # 无论是否重复，都把该字符「最近出现位置」刷新为当前 right
            last[ch] = right
            # 当前窗口 [left, right] 的长度，尝试刷新最大值
            ans = max(ans, right - left + 1)

        return ans


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.lengthOfLongestSubstring("abcabcbb") == 3   # "abc"
    assert s.lengthOfLongestSubstring("bbbbb") == 1      # "b"
    assert s.lengthOfLongestSubstring("pwwkew") == 3     # "wke" / "kew"；曾因 set 不清旧字符错答 4
    # 边界用例
    assert s.lengthOfLongestSubstring("") == 0           # 空串
    assert s.lengthOfLongestSubstring(" ") == 1          # 单个空格
    assert s.lengthOfLongestSubstring("au") == 2         # 全不重复
    assert s.lengthOfLongestSubstring("abba") == 2       # 经典陷阱：必须跳多格，不能只 left+1
    assert s.lengthOfLongestSubstring("dvdf") == 3       # "vdf"
    assert s.lengthOfLongestSubstring("tmmzuxt") == 5    # "mzuxt"
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 【核心认知坑：窗口与 set 脱节】最初想用 set 维护窗口内字符：
#       seen = set()
#       left = 0
#       for right in range(len(s)):
#           if s[right] in seen:
#               left += 1          # ← 只把 left 右移一格，却没从 seen 里删掉被抛弃的字符
#           ans = max(ans, right - left + 1)
#       seen.add(s[right])
#    错在哪：set 是「只进不出」的，left 右移后 seen 还留着早已滑出窗口的旧字符。
#    于是再遇到该字符时会「误判为窗口内重复」，把 left 错误右推，窗口算短、ans 偏小。
#    例 "abba"：到结尾的 a 时 seen 里还残着下标 0 的 a（已离开窗口），a 被误判，
#       left 被推到 2，丢掉真实窗口 [1,3]="bba"，但 "bba" 本身还背着重复 b——怎么走都不可能得 3。
#    这版写法本质是「逐格收缩」，遇到重复字符离 left 很远时会露馅。
#    根因：left 只 +1 不够；重复字符若离 left 很远，left 必须直接跳到「上次出现位置 + 1」。
# 2. 【提交报错 TypeError】在 LeetCode 编辑器贴代码时忘了给方法加 self：
#       def lengthOfLongestSubstring(s: str) -> int:
#    调用 Solution().lengthOfLongestSubstring(param_1) 时，Python 会偷偷先把「实例自身」
#    作为第一个参数传进去，于是方法实际收到「实例 + param_1」两个参数，但定义只收 1 个，
#    报：takes 1 positional argument but 2 were given。类方法第一参数必须是 self。
# 3. 【知识点】enumerate(s) 一次给出 (下标, 字符)，等价 range(len(s)) + s[right]，但更清爽。
# 4. 【知识点】滑动窗口「跳格」写法：本解用 if 判断 last[ch] >= left 再跳，
#    保证 left 只增不减、不回退，整轮严格 O(n)，不会因 last[ch]+1 比当前 left 小而左移。
# 5. 复杂度：时间 O(n) 单遍扫描（每个字符最多被纳入/剔除窗口各一次）；
#    空间 O(min(n, 字符集大小))，最坏存满整个字符集。
