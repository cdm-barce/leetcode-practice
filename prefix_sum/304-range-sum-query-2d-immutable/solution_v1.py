# LeetCode 304. 二维区域和检索 - 矩阵不可变（中等）
# 套路：每行做一维前缀和 + 查询时逐行累加，O(m·n) 预处理 / O(m) 查询，O(m·n) 空间
# 2026-10-21
# 我的解答（能 AC，但查询不是 O(1)，最优解见 solution_v2.py）

from typing import List


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        # prefix[r] 存原矩阵「第 r 行」的一维前缀和，长度 cols+1
        # prefix[r][0] 故意留 0 作边界占位，让 c1=0 时不用特判
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                # 行内前缀和：前 c+1 列之和 = 前 c 列之和 + 当前格
                self.prefix[r][c + 1] = self.prefix[r][c] + matrix[r][c]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        # 逐行取「第 r 行 col1..col2」的区间和，再纵向累加
        # 单行内部是 O(1)，但一共有 row2-row1+1 行，所以整体 O(m)
        total = 0
        for r in range(row1, row2 + 1):
            total += self.prefix[r][col2 + 1] - self.prefix[r][col1]
        return total


if __name__ == "__main__":
    matrix = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]
    nm = NumMatrix(matrix)
    # 官方用例
    assert nm.sumRegion(2, 1, 4, 3) == 8
    assert nm.sumRegion(1, 1, 2, 2) == 11
    assert nm.sumRegion(1, 2, 2, 4) == 12
    # 边界用例：四个角 + 整块
    assert nm.sumRegion(0, 0, 0, 0) == 3          # 左上角单格
    assert nm.sumRegion(4, 4, 4, 4) == 5          # 右下角单格
    assert nm.sumRegion(0, 0, 4, 4) == 58         # 整个矩阵
    assert nm.sumRegion(0, 4, 4, 4) == 20         # 最后一列
    assert nm.sumRegion(4, 0, 4, 4) == 9          # 最后一行
    # 单行 / 单列矩阵（退化形状最容易踩 range 边界）
    assert NumMatrix([[1, 2, 3]]).sumRegion(0, 0, 0, 2) == 6
    assert NumMatrix([[1], [2], [3]]).sumRegion(0, 0, 2, 0) == 6
    # 负数（前缀和不单调，但区间和公式照样成立）
    assert NumMatrix([[-1, -2], [-3, -4]]).sumRegion(0, 0, 1, 1) == -10
    assert NumMatrix([[-1, -2], [-3, -4]]).sumRegion(1, 1, 1, 1) == -4
    # 单元素矩阵
    assert NumMatrix([[5]]).sumRegion(0, 0, 0, 0) == 5
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 这题我连错三轮，病灶都是「下标写死」，而且全都不报错：
#    第 1 轮 matrix[0][1]        -> 列和行都写死，prefix 每行全是 0，输出 [0, 0, 0]
#    第 2 轮 matrix[i][1]        -> 行活了列还死着，prefix 变成等差数列，输出 [9, 16, 24]
#    第 3 轮 matrix[i][j]        -> 正确
#    第二轮那个「数字 1」和「字母 j」在等宽字体下几乎分不清，靠截图根本看不出来，
#    最后是把代码当文本发出来，一字符一字符比对才定位到的。
# 2. 前缀和有个「健康检查」：正确的前缀和一定是杂乱的（如 [0,3,3,4,8,10]）。
#    如果某一行是漂亮的等差数列，或者整行全 0，一定是构造阶段把某个下标写死了。
# 3. for r in range(row1, row2) 少写 +1：range 左闭右开，会漏掉最后一行。
#    症状很好认——查询 3 行少 3、查询 2 行少 2、查询 1 行直接得 0。
# 4. 变量别用 i / j：i、j、1、l 在小字号下互相打架，改用 r / c 后这类错再没犯过。
# 5. 学到的点：前缀和数组多开一位（这里是多开一列）就是「哨兵」思想——
#    用虚拟边界把 c1=0、row1=0 这类特殊判断变成正常流程。
#    560 题的 cnt[0] = 1、DP 多开一行，本质上是同一招。
