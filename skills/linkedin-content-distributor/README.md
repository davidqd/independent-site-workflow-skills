# LinkedIn 内容分发 Skill

将已发布的网站文章或用户提供的内容改写、审批、发布并验证为 LinkedIn 个人账号帖子。

## 安装到 Codex

复制下面的提示词发送给 Codex：

```text
使用 $skill-installer，从下面的 GitHub 地址安装 Skill。请保留完整目录结构，安装后检查文件是否完整，并告诉我如何调用。

https://github.com/davidqd/independent-site-workflow-skills/tree/main/skills/linkedin-content-distributor
```

也可以按照仓库的 [Codex Skills 安装说明](../../CODEX-INSTALL.md) 手动安装。

## 使用

首次配置：

```text
使用 $linkedin-content-distributor，帮我连接自己的 LinkedIn 个人账号并检查发布条件。
```

分享文章：

```text
使用 $linkedin-content-distributor，把这篇已发布文章改写成 LinkedIn 帖子。先给我预览，得到确认后再发布。
```

## 依赖

- 用户自己控制的 LinkedIn Developer App。
- App 已启用 Share on LinkedIn。
- Access Token 含 `openid`、`profile`、`w_member_social`。
- 本地安全发布脚本使用 Python 3；macOS 可把令牌保存在钥匙串中。
- 当前本地发布器只支持 LinkedIn 个人账号公开自然帖子。

详细配置见 [首次配置指南](./references/getting-started.md)。

## 更新

重新下载最新版，用新的完整文件夹替换本地旧版本。替换前请备份自己修改过的文件。不要覆盖或分享本机钥匙串凭据。

## 授权

允许按 [LICENSE.md](./LICENSE.md) 进行非商业学习、研究和使用。任何商业用途均须事先取得大卫独立站营销的明确书面授权。
