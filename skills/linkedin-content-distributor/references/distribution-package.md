# 分发包规范

在写作工作流与 LinkedIn 分发之间交接内容时使用此结构。可以采用 JSON、YAML、电子表格行或其他等效的结构化记录，但必须保留字段含义。

## 内容源

- `source_type`：`website_article`、`supplied_text`、`document` 或其他明确类型
- `source_title`
- `source_url`：适用时填写公开的 canonical URL
- `source_status`：例如 `published`、`draft` 或 `private`
- `source_language`
- `supported_claims`：可以安全复用的事实主张
- `source_media`：媒体资源、所有权或授权状态、标题和 Alt 文本

## 分发意图

- `target_type`：`member` 或 `organization`
- `target_id`：经过验证的账号或组织标识符，不得猜测
- `target_display_name`
- `audience`
- `objective`
- `mode`：`prepare-only`、`approval-required` 或 `auto-publish`
- `scheduled_time` 和 `timezone`：用户要求排程时填写

## LinkedIn 内容

- `post_text`
- `content_type`：纯文本、文章链接、图片、视频、文档或多图
- `link_url`
- `link_title` 和 `link_description`：发布路径支持时填写
- `media`
- `hashtags`
- `visibility`
- `cta`

## 控制与结果

- `content_fingerprint`：根据目标、规范化源 URL 和最终帖子文案生成的稳定哈希或等效键
- `approval_status`
- `approved_at` 和 `approved_by`：适用时填写
- `publish_status`
- `linkedin_post_id`
- `linkedin_post_url`
- `published_at`
- `verification_status`
- `error`：不包含密钥、可用于处理问题的失败原因

目标和返回的帖子对象尚未核验时，不得将记录标记为 `已发布并验证`。请求超时或返回结果不明确时，使用 `已发布但未验证` 或 `失败-需要对账`；任何重试前必须先根据内容指纹或源 URL 搜索已发布帖子。
