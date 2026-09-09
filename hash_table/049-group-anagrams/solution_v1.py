# LeetCode 49. 字母异位词分组（中等）
# 套路：排序后字符串当哈希键分组，O(n·k·log k) 时间 / O(n·k) 空间
# 2026-09-09
# 我的解答
# 思路：互为字母异位词的字符串排序后完全相同（"eat"->"aet"、"tea"->"aet"），
#       用排序结果做字典的键，把同键的字符串收进同一个列表
class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = {}
        for s in strs:
            key = ''.join(sorted(s))            # 排序结果 = 分组签名
            groups.setdefault(key, []).append(s)  # 有键就用，没键先建空列表再追加
        return list(groups.values())


if __name__ == "__main__":
    s = Solution()

    def norm(res: list[list[str]]) -> list[list[str]]:
        # 输出组间顺序不固定，排序后比较更稳
        return sorted(sorted(g) for g in res)

    assert norm(s.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
        norm([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert norm(s.groupAnagrams([""])) == [[""]]        # 空字符串：key = ""
    assert norm(s.groupAnagrams(["a"])) == [["a"]]      # 单字符
    assert norm(s.groupAnagrams(["a", "a"])) == [["a", "a"]]  # 重复词同组
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. sorted(s) 返回的是【字符列表】，不能直接当哈希键（list 不可哈希）
#    -> 必须 ''.join(...) 拼回字符串，或 tuple(sorted(s))
# 2. setdefault(key, []).append(s) 原理：setdefault 返回的是字典里那个
#    列表的引用，.append 加进去 = 改字典里的本体（Python 引用语义）
# 3. 键里字符带中文/大写也能排（按 Unicode 码），但本题只有小写字母
# 相关题目：242. 有效的字母异位词（单对判断，本题的降级版）
