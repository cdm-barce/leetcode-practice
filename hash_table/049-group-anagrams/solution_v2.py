# LeetCode 49. 字母异位词分组（中等）
# 套路：26 位计数数组转字符串当哈希键，O(n·k) 时间 / O(n·k) 空间
# 2026-09-09
# 最优代码（进阶：免排序）
# 思路：不排序，统计每个字符串里 a~z 各出现几次。两个异位词的
#       计数完全相同，所以计数结果就是分组键。每组 O(k) 而非 O(k·log k)
class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = {}
        for s in strs:
            cnt = [0] * 26                        # 26 个字母的计数器
            for ch in s:
                cnt[ord(ch) - ord('a')] += 1      # 字母 -> 下标 0~25（'a' 的 ASCII 是 97）
            key = '#'.join(map(str, cnt))          # 计数数组转字符串键
            groups.setdefault(key, []).append(s)
        return list(groups.values())


if __name__ == "__main__":
    s = Solution()

    def norm(res: list[list[str]]) -> list[list[str]]:
        return sorted(sorted(g) for g in res)

    assert norm(s.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
        norm([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert norm(s.groupAnagrams([""])) == [[""]]
    assert norm(s.groupAnagrams(["a"])) == [["a"]]
    assert norm(s.groupAnagrams(["aa", "a"])) == norm([["aa"], ["a"]])   # 计数不同则不同组
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 为什么用 '#' 分隔而不是直接 ''.join(map(str, cnt))？
#    计数可能超过一位数（如 "aa" -> [2,0,...]），不分隔会让不同计数
#    撞成同一个键（[1,0,0] vs [10,0]），'#' 隔开即可消除歧义
# 2. map(str, cnt) 返回惰性迭代器，join 会消费它，一次性使用没问题
# 3. 也可用 key = tuple(cnt) 当键（元组可哈希），省掉 map+join，
#    但可读性更差，一般不用
# 4. 与排序版取舍：本题单词短，两版实际差距微小；面试先写排序版保底，
#    再提计数版优化到 O(n·k)。计数版真正价值场景是长单词
