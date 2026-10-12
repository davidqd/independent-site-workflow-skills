# 新 Skill 上传规范

以后向本仓库上传新 Skill 时，使用本清单保持目录、Codex 安装说明和索引格式一致。

## 1. Skill 目录

将完整文件夹放到 `skills/<skill-name>/`。文件夹名使用英文小写、数字和短横线，并与 `SKILL.md` 中的 `name` 一致。

至少包含：

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── LICENSE.md
└── agents/
    └── openai.yaml
```

`references/`、`scripts/` 和 `assets/` 仅在 Skill 实际需要时添加，不创建空目录。上传时保留全部配套文件及相对路径，不能只上传 `SKILL.md`。

## 2. Skill README 格式

每个 `skills/<skill-name>/README.md` 使用以下结构，根据实际情况删除不适用的可选段落：

````markdown
# <显示名称> Skill

<一句话说明用途和适用对象。>

## 安装到 Codex

复制下面的提示词发送给 Codex：

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/<skill-name>
```

也可以按照仓库的 [Codex Skills 安装说明](../../CODEX-INSTALL.md) 手动安装。

## 使用

```text
使用 $<skill-name>，<一个真实、简洁的调用示例>。
```

## 依赖

<可选：只列出实际需要的工具、权限或软件依赖。>

## 更新

重新下载最新版，用新的完整文件夹替换本地旧版本。替换前请备份自己修改过的文件。

## 授权

允许按 [LICENSE.md](./LICENSE.md) 进行非商业学习、研究和使用。任何商业用途均须事先取得大卫独立站营销的明确书面授权。
````

## 3. 同步更新公共文档

每次新增 Skill，必须在同一个提交中同步更新：

1. 根目录 `README.md` 的“已上传 Skill”。
2. `skills/README.md` 的“当前 Skill”。
3. `CODEX-INSTALL.md` 的自动安装提示词和调用示例。

## 4. 提交前验证

- 确认 `SKILL.md` YAML frontmatter 至少包含正确的 `name` 和 `description`。
- 确认 Skill 文件夹名、`SKILL.md` 的 `name`、GitHub URL 和调用名完全一致。
- 确认 README 与统一安装页中的相对链接可解析。
- 使用可用的 Skill 验证器检查新目录。
- 运行 `git diff --check`，并确认提交中没有无关文件。

## 5. 完成标准

只有当完整 Skill 文件夹、独立 README、统一安装说明、两个仓库索引和许可证都已提交，并完成结构验证后，才算上传完成。
