# 机会发现、评分与输出规范

## 搜索组合

把 `<product>` 替换为标准英文市场词，把 `<country>` 替换为目标国家或地区：

```text
<product> association <country>
<product> supplier directory <country>
<product> distributor directory
<product> "resources"
<product> "write for us"
<product> "contributor guidelines"
<product> podcast interview
<product> buyer guide
<product> trade publication
<product> inurl:links
<product> inurl:resources
site:.org <product> suppliers
site:.gov <product> directory
"competitor brand" -site:competitor-domain.example
```

`write for us`、目录和资源页只是发现线索，不能视为质量证明。打开页面后确认其行业、受众、编辑和最近更新时间。

## 100 分模型

| 维度 | 分值 | 判断重点 |
|---|---:|---|
| 行业与产品相关性 | 0-30 | 是否服务相同产业链、采购角色或应用场景 |
| 编辑与组织可信度 | 0-20 | 是否有真实组织、编辑规范、作者和更新痕迹 |
| 合作/收录合理性 | 0-15 | 是否存在自然且符合规则的贡献或收录路径 |
| 目标市场受众 | 0-15 | 是否覆盖目标国家、语言或买家群体 |
| 联系可达性 | 0-10 | 是否存在已验证的公开商务联系渠道 |
| 链接与页面价值 | 0-10 | 目标页、上下文和潜在引荐价值是否合理 |

风险扣分 `risk_penalty` 为 0-50：

- 大量无关主题、明显站群或自动生成内容：10-30。
- 公开售卖传递排名权重链接、锚文本套餐：20-40。
- 恶意软件、仿冒、博彩/成人等不相干高风险邻接：30-50。
- 无编辑审核的开放评论、论坛资料页或批量目录：10-30。

`total_score = 六项得分之和 - risk_penalty`，最低为 0。

- `A`：总分至少 75，且风险扣分不高于 10。
- `B`：总分至少 60，且风险扣分不高于 20。
- `C`：总分至少 45。
- `Reject`：总分低于 45，或风险扣分至少 30。

第三方权重、流量等指标可作为证据列，但不直接替代相关性和编辑判断。

## prospects.csv 必填字段

| 字段 | 含义 |
|---|---|
| `prospect_url` | 实际验证的机会页 URL |
| `domain` | 来源域名 |
| `organization` | 组织或网站名称 |
| `opportunity_type` | 协会、目录、媒体、资源页、伙伴、采访、broken link 等 |
| `target_market` | 国家、地区或语言 |
| `evidence` | 页面上观察到的机会依据 |
| `source_url` | 证据来源 URL；可与机会页相同 |
| `contact_name` | 公开联系人姓名；未知时留空 |
| `contact_channel` | 公开商务邮箱、表单、LinkedIn 公司页等 |
| `contact_source_url` | 联系方式来源 URL |
| `suggested_asset` | 拟提供的真实内容或资料 |
| `suggested_target_url` | 我方建议落地页 |
| 六项评分字段 | 对应评分模型 |
| `risk_penalty` | 0-50 |
| `risk_notes` | 风险证据 |
| `status` | 工作流状态 |
| `checked_at` | `YYYY-MM-DD` |

严禁推测个人邮箱。若只找到公司通用渠道，保留真实通用渠道并标记联系人姓名 `未确认`。

## data_coverage

对网站验证、联系人、第三方指标、内容适配和外联状态分别标注：`已验证`、`部分验证`、`失败`、`未授权`、`无数据`。附失败原因，不把缺失数据默认为零。

