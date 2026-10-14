# 本地 LinkedIn API 发布器

当没有可用的发布连接器或 n8n 服务时，使用 `scripts/linkedin_publish.py`。脚本仅支持个人账号的公开自然帖子，不处理公司主页、广告、评论、点赞或私信。

## 凭证要求

- Token 必须包含 `w_member_social`。
- 省略 `--author-urn` 时，Token 还必须包含 `openid profile`，脚本通过 `/v2/userinfo` 取得当前成员 ID。
- Access Token 只通过 macOS 钥匙串或进程环境变量读取，不得放进命令参数、Skill、源码、文案文件或分发记录。
- `store-token` 使用隐藏输入把 Access Token 写入 macOS 钥匙串；该命令必须由用户在自己的终端中执行和粘贴。
- 当前脚本不自动刷新 Token。到期前必须通过已批准的 OAuth 流程更新钥匙串；不得静默使用过期凭证。

## 首次配置（推荐）

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py setup
```

向导会隐藏输入 Access Token，将其写入 macOS 钥匙串，然后调用 LinkedIn `userinfo` 验证个人账号。出现钥匙串授权提示时，由用户亲自选择“允许”或“始终允许”。`store-token` 保留为只更新令牌、不联网验证的兼容命令。

完整的 LinkedIn 应用、权限和令牌准备步骤见[首次配置指南](getting-started.md)。

## 预演

先把最终 LinkedIn 文案保存为 UTF-8 文件，再运行：

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py prepare \
  --text-file POST.txt \
  --article-url 'https://example.com/article/' \
  --article-title 'Article title' \
  --article-description 'Short verified description' \
  --linkedin-version YYYYMM
```

预演不读取 Token，也不访问 LinkedIn。向用户展示文案、目标、文章链接和媒体计划后才能发布。

## 发布

只有用户批准准确的最终预览后，才运行：

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py publish \
  --text-file POST.txt \
  --article-url 'https://example.com/article/' \
  --article-title 'Article title' \
  --article-description 'Short verified description' \
  --linkedin-version YYYYMM \
  --record-file DISTRIBUTION.jsonl \
  --approve
```

运行前从 LinkedIn 官方文档确认仍受支持的 `Linkedin-Version`，不得机械沿用示例。脚本会检查分发记录中的内容指纹、发送一次创建请求、保存返回的帖子 ID，并在权限允许时读回验证。读回权限不足时记录为 `published_but_unverified`，不得自动重发。

文章缩略图上传需要 Images API 和媒体 URN，当前本地脚本不处理图片上传。文章链接帖会显式提供 URL、标题和描述；不要把它误称为 LinkedIn 原生长文章。
