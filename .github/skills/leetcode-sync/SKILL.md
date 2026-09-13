---
name: leetcode-sync
description: 把一道 LeetCode 题解按仓库规范整理进 leetcode-practice：建专题目录、写 solution_vN.py、跑 assert 测试、更新 README 双表、按格式 commit。当用户贴出题解代码/力扣截图，或要求"整理到仓库""入库""更新刷题记录"时使用。
---

# LeetCode 题解入库流程

## 前置（每次必做）

1. 读完项目根目录 `AGENTS.md` 与 `.github/copilot-instructions.md`，未读不要动笔。
2. 确认目标仓库根目录（本地路径 `C:\Users\suntianyu\Desktop\leetcode-practice`），默认分支 `main`。
3. 先读 README 当前的「进度总览」和「题目清单」，记住要改的数字和插入位置。

## 步骤

### 1. 定目录

`专题/NNN-英文题名/`，题号补零三位、英文名用 LeetCode 官方 slug 全小写连字符。
已知专题：`arrays/`、`linked_list/`、`dp/`、`hash_table/`、`math/`；新专题小写下划线。

### 2. 拆版本

按**尝试顺序**写 `solution_v1.py`、`v2`、`v3`…… 每版独立成文件，不合并。

- v1 通常是暴力解或错误示范，**不要删、不要顺手修正**
- 错误版本：文件头补充行标明「错误示范」，`__main__` 里断言它**实际会输出的错误结果**，再用 print 说明正确值；会抛异常的用 try/except 捕获并打印证据
- 正确版本：`__main__` 用 assert 覆盖官方示例 + 边界（空输入 / 单元素 / 全相同 / 负数）

### 3. 文件模板

```python
# LeetCode <题号>. <中文题名>（<难度>）
# 套路：<解法名>，O(?) 时间 / O(?) 空间
# <YYYY-MM-DD>
# <我的解答 / 最优代码 / 错误示范，保留以记录 bug>

<带行内注释的代码，注释解释「为什么」而非复述代码>


if __name__ == "__main__":
    s = Solution()
    assert ...
    print("全部用例通过 ✓")


# 思路拆解
# ...
# 踩坑记录：
# 1. 【错误类型】错在哪 → 为什么错 → 怎么改
# 2. ...
```

### 4. 跑测试（不能跳）

每个文件都必须实际运行：

```bash
"C:/Users/suntianyu/.workbuddy/binaries/python/versions/3.13.12/python.exe" <文件绝对路径>
```

全部通过才继续；断言失败先判断是代码错还是**预期值写错**（预期写错过一次：错误示范的预期应是它的真实输出）。

### 5. 更新 README（两处，缺一不可）

1. 进度总览：对应类别 +1，合计 +1
2. 题目清单：按题号顺序插入一行
   `| <题号> | <中文题名> | <难度> | <类别> | <套路> | <YYYY-MM-DD> | ✅ |`

### 6. 提交

```bash
git -c http.schannelCheckRevoke=false add -A
git -c http.schannelCheckRevoke=false commit -m "add LC<题号> <中文题名>：<v1 套路> / <v2 套路>，含踩坑记录"
```

## 硬性约束

- **不要自行 `git push`**：推送前必须询问使用者，得到明确同意后再执行。
  推送用：`GIT_TERMINAL_PROMPT=0 git -c http.sslBackend=schannel -c http.schannelCheckRevoke=false push origin main`
  本机直连 GitHub 不通，需使用者开启 Watt Toolkit（Steam++）加速；卡住不动就重试，不要改参数。
- 不引入第三方库；不删历史版本；不改历史文件的完成日期；注释与踩坑记录全程中文。
- 使用者是在校学生，**不要一上来给最优解**：先问思路或给方向性提示，明确要求才写完整实现。

## 讲解类请求（"讲一下这题""为什么错了"）

- 报错先讲清思路漏洞再给代码；同类题顺带点一句迁移（如「这和 LC1 两数之和一个套路」）。
- 怀疑代码有 bug：先写随机对拍脚本（ref 用最笨但正确的写法）跑几十万组捞反例，比肉眼审代码可靠。
- 讲解放对话里，不写进仓库正文。
