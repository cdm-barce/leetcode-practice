# LeetCode 567. 字符串的排列（中等）
# 套路：定长滑动窗口 + 26 位计数数组增量更新，O(n) 时间 / O(1) 空间
# 2026-09-26
# 我的解答（一次通过 0ms，LC438 模板直接复用）

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n, m = len(s1), len(s2)      # 注意：这里 n 是模板串长度（=窗口长），m 是长串，
                                     # 与 LC438 的 n 长串 / m 窗口 正好相反，复用模板时最易翻车

        need = [0] * 26              # s1 的字母计数，循环外只算一次（固定不变）
        for ch in s1:
            need[ord(ch) - ord('a')] += 1

        win = [0] * 26               # s2 初始窗口 s2[:n] 的计数，也只初始化一次
        for ch in s2[:n]:
            win[ord(ch) - ord('a')] += 1

        if need == win:              # 初始窗口（起点 0）就命中
            return True

        for i in range(n, m):        # 右端从 n 滑到 m-1，每步只做「一进一出」两次 O(1) 更新
            win[ord(s2[i]) - ord('a')] += 1       # 进来：s2[i]
            win[ord(s2[i - n]) - ord('a')] -= 1   # 出去：s2[i - n]
            if need == win:                       # 两个 26 长列表逐位比较，常数级
                return True
        return False


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.checkInclusion("ab", "eidbaooo") is True    # "ba" 是 "ab" 的排列
    assert s.checkInclusion("ab", "eidboaoo") is False   # 任何窗口都凑不齐 a+b
    # 边界用例
    assert s.checkInclusion("a", "a") is True            # 单字符，初始窗口即命中
    assert s.checkInclusion("abc", "ab") is False        # 模板串比长串还长（range(n,m) 为空）
    assert s.checkInclusion("abc", "abc") is True        # 等长且相等
    assert s.checkInclusion("ab", "ba") is True          # 等长但顺序相反（排列≠子串）
    assert s.checkInclusion("aaa", "aaaa") is True       # 全同字符
    assert s.checkInclusion("adc", "dcda") is True       # 命中在中间窗口 "cda"
    assert s.checkInclusion("hello", "ooolleoooleh") is False  # 反串陷阱："olleh" 并不真的存在
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 本题是 LC438（找到所有异位词）的近亲，模板 90% 相同：
#    need = 模板串计数（循环外算一次）、win = 窗口计数、一进一出增量更新、win == need 判命中。
#    唯一本质区别：438 命中后记录起点继续滑（收集全部），567 命中直接 return True（存在即可）。
# 2. n / m 的含义与 438 正好相反：438 里 n=len(s) 是长串、m=len(p) 是窗口长，出去的是 s[i-m]；
#    本题 n=len(s1) 是窗口长、m=len(s2) 是长串，出去的是 s2[i-n]。
#    两题代码对照着看极易看岔。改进习惯：窗口长统一叫 k，长串统一叫 n，形成肌肉记忆。
# 3. 可加显式剪枝 if n > m: return False（模板串比长串长必无排列）。
#    不加也正确——range(n, m) 为空 + 初始窗口计数凑不齐，自动落到 return False；
#    但写出来语义更清晰，面试是加分项。
# 4. 对比 labuladong 的 Java 版（HashMap<Character,Integer> + valid 计数器）：
#    HashMap + valid 是通用写法（字符集任意时用），小写字母限定下 26 数组 + win == need
#    更快更简洁。与 LC 242 的结论一致。
# 5. 同家族：LC 242（判断异位词）→ LC 438（找所有异位词起点）→ LC 567（判断排列存在）
#    → LC 76 最小覆盖子串（进阶：窗口长度可变）。这条线吃透，滑动窗口哈希计数基本通关。
