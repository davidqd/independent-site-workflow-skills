# GEO Article Writer Skill

用于 SEO/GEO 内容规划与写作、产品库驱动的 AIDA 选题、Excel 文章队列，以及经验证的 WordPress 草稿自动化。

## 下载

1. 回到[总仓库首页](https://github.com/davidqd/independent-site-workflow-skills)。
2. 点击 **Code → Download ZIP**。
3. 解压后找到 `skills/geo-article-writer`。
4. 复制整个 `geo-article-writer` 文件夹，不要只复制 `SKILL.md`。

## 安装到 Codex

将完整文件夹复制到个人 Skills 目录：

- macOS / Linux：`~/.codex/skills/geo-article-writer/`
- Windows：`%USERPROFILE%\.codex\skills\geo-article-writer\`

安装后重新打开 Codex或新建任务，让 Codex 重新发现 Skill。请保留 `SKILL.md`、`agents/`、`references/`、`scripts/`、`LICENSE.md` 和本说明的原有相对位置。

## 依赖

普通写作和内容优化不需要运行配套脚本。使用 Excel 选题队列功能时，需要 Python 3 和 `openpyxl`：

```bash
python3 -m pip install openpyxl
```

创建 WordPress 草稿、上传特色图或验证站内链接时，还需配置相应的 WordPress 写入、媒体和网页访问能力。

## 使用

普通文章任务：

```text
使用 $geo-article-writer，为目标客户写一篇围绕“关键词”的英文 GEO 文章。
```

产品库选题任务：

```text
使用 $geo-article-writer，读取我的产品库 Excel，为每个产品关键词生成 AIDA 四阶段选题并建立文章队列。
```

仅安装 Skill 不会自动启用每日任务。自动创建 WordPress 草稿前，应先手动跑通流程并单独配置排程。

## 更新

重新下载最新版，用新的完整文件夹替换本地旧版本。替换前请备份自己修改过的文件和文章队列。

## 授权

允许按 [LICENSE.md](./LICENSE.md) 进行非商业学习、研究和使用。任何商业用途，包括收费写作、SEO 服务、代运营、培训、转卖和商业产品集成，均须事先取得大卫独立站营销的明确书面授权。
