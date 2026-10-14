# 在 Codex 中安装 Skills

本仓库的每个 Skill 都是一个完整文件夹。安装时必须保留该文件夹内的 `SKILL.md`、`agents/`、`references/`、`scripts/`、`assets/` 和 `LICENSE.md` 等已有文件与相对目录结构；不要只下载或复制 `SKILL.md`。

## 方法一：让 Codex 自动安装（推荐）

在 Codex 中发送下面对应的提示词。Codex 会使用内置的 `$skill-installer` 下载并安装 Skill。

### B2B WordPress 建站

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/build-b2b-wordpress-site
```

安装后调用示例：

```text
使用 $build-b2b-wordpress-site，为这个外贸制造企业规划并搭建 WordPress B2B 独立站。
```

### GEO Article Writer

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/geo-article-writer
```

安装后调用示例：

```text
使用 $geo-article-writer，为目标客户写一篇围绕“关键词”的英文 GEO 文章。
```

### B2B 白帽外链开发

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/b2b-backlink-builder
```

安装后调用示例：

```text
使用 $b2b-backlink-builder，为 qpdryer.com 寻找免费的工业干燥设备相关外链机会。
```


### LinkedIn 内容分发

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/linkedin-content-distributor
```

安装后调用示例：

```text
使用 $linkedin-content-distributor，把这篇已发布文章改写成 LinkedIn 帖子。先给我预览，得到确认后再发布。
```

## 方法二：手动安装

1. 在仓库首页点击 **Code → Download ZIP**。
2. 解压下载文件，进入 `skills/`。
3. 复制需要的完整 Skill 文件夹到个人 Skills 目录：
   - macOS / Linux：`~/.codex/skills/`
   - Windows：`%USERPROFILE%\.codex\skills\`
4. 新建 Codex 任务或重新打开 Codex，让 Codex 重新发现 Skill。

例如，安装外链 Skill 后应存在：

```text
~/.codex/skills/b2b-backlink-builder/SKILL.md
```

## 更新已有 Skill

安装器不会覆盖同名的现有 Skill。更新前先备份自己的修改，再用最新版完整文件夹替换旧版本。不要把新旧版本的文件零散混合。

## 验证安装

在新的 Codex 任务中明确点名 Skill，例如：

```text
请使用 $b2b-backlink-builder，先说明这个 Skill 的工作模式和所需输入，不要执行外联发送。
```

如果 Codex 能识别并按 `SKILL.md` 回答，说明安装成功。某些 Skill 的实际任务还需要额外工具或权限，例如 WordPress 连接、网页访问或本地 Python 依赖；安装 Skill 本身不会自动配置这些能力。
