# 首次配置指南

本指南用于首次连接 LinkedIn 个人账号，或把 Skill 分享给另一位用户。当前本地发布器支持公开的个人账号自然帖子；公司主页、广告、评论、点赞和私信不在此配置范围内。

## 用户需要准备什么

1. 一个由用户自己控制的 LinkedIn Developer App。
2. App 已启用 **Share on LinkedIn** 产品。
3. 通过 LinkedIn 官方 OAuth 工具或用户自己的 OAuth 流程取得 Access Token，并包含：
   - `openid`
   - `profile`
   - `w_member_social`
4. macOS 上可用的“钥匙串访问”。非 macOS 用户需通过运行环境的密钥管理机制提供 `LINKEDIN_ACCESS_TOKEN`，不要把令牌保存到仓库或普通配置文件。

不要让用户把 Client Secret 或 Access Token 发到聊天中。Skill 不需要共享原作者的 LinkedIn App、令牌或账号。

## 一键初始化

在用户自己的终端运行：

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py setup
```

按提示粘贴 Access Token。输入不会显示。向导会：

1. 将令牌保存到 macOS 钥匙串；
2. 调用 LinkedIn 官方 `userinfo` 接口验证令牌；
3. 输出 `ready` 和个人账号 URN，但不会输出令牌；
4. 提醒先生成预览，再获得本次发布确认。

macOS 第一次读取钥匙串时可能显示系统授权提示。用户应核对请求程序与钥匙串项目，再自行选择“允许”或“始终允许”。若未及时处理，命令会在 60 秒后停止并给出可重试提示，不会发布内容。

## 连接检查和更新令牌

只检查当前连接：

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py check
```

只更新钥匙串中的令牌、不连接 LinkedIn：

```bash
python3 <SKILL_DIR>/scripts/linkedin_publish.py store-token
```

Access Token 到期后重新执行 `setup` 即可覆盖旧令牌并验证。当前脚本不会自动刷新令牌。

## 首次发布验收

分享给他人前，建议让新用户用自己的账号完整完成一次：

1. `setup` 返回 `ready`；
2. 使用 `prepare` 生成帖子预览；
3. 核对账号、正文、链接、公开范围和媒体；
4. 用户明确确认后运行 `publish --approve`；
5. 保存帖子 ID 和公开链接，并检查分发记录。

首次发布跑通前，不要启用无人值守定时发布。

## 常见问题

- **`userinfo` 返回 401**：令牌无效或已过期，重新生成后运行 `setup`。
- **无法取得成员 ID**：令牌通常缺少 `openid` 或 `profile`。
- **发布返回 403**：确认 App 已启用 Share on LinkedIn，并且令牌含 `w_member_social`。
- **钥匙串读取超时**：处理 macOS 授权提示后重试；不要连续触发多次发布。
- **发布成功但无法读回**：保留 `published_but_unverified`，用返回的公开链接检查，不要自动重发。
