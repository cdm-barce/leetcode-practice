# LeetCode 304. 二维区域和检索 - 矩阵不可变（中等）
# 套路：二维前缀和 + 四角容斥，O(m·n) 预处理 / O(1) 查询，O(m·n) 空间
# 2026-10-21
# 最优代码

from typing import List


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        rows, cols = len(matrix), len(matrix[0])
        # prefix[i][j] = 原矩阵「前 i 行、前 j 列」组成的矩形元素之和
        # 尺寸多开一行一列（rows+1 × cols+1），第一行第一列恒为 0，作为哨兵
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                # 建表也是容斥：上面一块 + 左边一块 − 左上被加了两遍 + 当前格
                self.prefix[i][j] = (
                    self.prefix[i - 1][j]                  # 上方矩形
                    + self.prefix[i][j - 1]                # 左方矩形
                    - self.prefix[i - 1][j - 1]            # 左上角重复加了一次，减掉
                    + matrix[i - 1][j - 1]                 # 当前格子（原矩阵 0 起，故 -1）
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        # 查询容斥：整个大矩形 − 上方条带 − 左方条带 + 左上被减了两次的区域
        # 注意 prefix 比 matrix 多一圈 0，所以所有下标要 +1
        return (
            self.prefix[row2 + 1][col2 + 1]     # 左上角到 (row2, col2) 的整块
            - self.prefix[row1][col2 + 1]       # 减去 row1 以上那条
            - self.prefix[row2 + 1][col1]       # 减去 col1 以左那条
            + self.prefix[row1][col1]           # 左上角被减了两次，加回来
        )


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
    # 边界用例：四个角 + 整块（与 solution_v1 用同一组，便于对拍）
    assert nm.sumRegion(0, 0, 0, 0) == 3          # 左上角单格
    assert nm.sumRegion(4, 4, 4, 4) == 5          # 右下角单格
    assert nm.sumRegion(0, 0, 4, 4) == 58         # 整个矩阵
    assert nm.sumRegion(0, 4, 4, 4) == 20         # 最后一列
    assert nm.sumRegion(4, 0, 4, 4) == 9          # 最后一行
    # 单行 / 单列矩阵
    assert NumMatrix([[1, 2, 3]]).sumRegion(0, 0, 0, 2) == 6
    assert NumMatrix([[1], [2], [3]]).sumRegion(0, 0, 2, 0) == 6
    # 负数
    assert NumMatrix([[-1, -2], [-3, -4]]).sumRegion(0, 0, 1, 1) == -10
    assert NumMatrix([[-1, -2], [-3, -4]]).sumRegion(1, 1, 1, 1) == -4
    # 单元素矩阵
    assert NumMatrix([[5]]).sumRegion(0, 0, 0, 0) == 5
    # 前缀和表自检：P[5][5] 应等于整个矩阵的和
    assert nm.prefix[5][5] == 58
    assert nm.prefix[0] == [0] * 6                # 第一行哨兵全 0
    assert all(row[0] == 0 for row in nm.prefix)  # 第一列哨兵全 0
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 两个坐标系差 1，是全题最容易错的地方：
#    matrix[i][j]（0 起）对应 prefix[i+1][j+1]（1 起）。
#    建表写 matrix[i][j] 而不是 matrix[i-1][j-1]，会 IndexError（i=rows 越界）；
#    查询少写 +1，就会变成查「上一行左边一点」的区域，答案稳定偏小且不报错。
# 2. 多开的那一圈 0 不是装饰：它让 row1=0、col1=0 时 prefix[row1][...] 直接取到 0，
#    省掉全部边界特判。去掉它，代码要翻倍。
# 3. 建表和查询是同一个容斥公式的两个方向：
#    建表是「小块拼大块」（加两次、减一次），查询是「大块切小块」（减两次、加一次）。
#    想通这一点就不用背公式了。
# 4. 和 v1 对比：两者预处理都是 O(m·n)、空间都是 O(m·n)，
#    但查询从 O(m) 降到 O(1)。本题数据量 m,n ≤ 200、查询 ≤ 10^4，
#    v1 约 2×10^6 次操作也能过，v2 是 10^4 次，快两个数量级。
# 5. 同款套路：1314（矩阵区域和）、221（最大正方形）、1292（二分+前缀和判全 1）。
