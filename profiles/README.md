# 用户资料目录约定

此目录用于在同一 Codex 项目中按资料名整理个人资料。技能在每段新对话中询问要使用的资料名，只读取当前用户明确选定的目录。建议资料名为 1–48 个 ASCII 字母、数字、下划线或连字符，例如 `mei_01`；不要使用真实姓名或路径字符。此限制是操作约定，技能不具备强制执行的文件系统权限。

## 建议结构

```text
profiles/
  README.md
  <profile-id>/
    profile.md
    quality_assess.md
    conversations/
      YYYY-MM-DD-topic.md
```

`<profile-id>` 建议使用不含真实姓名的代号。创建个人目录时，从仓库根目录的 `profile_template.md` 复制为 `profile.md`。对话摘要可参考本目录的 `conversation_template.md`；只有在用户审阅并明确同意后才保存，默认保存精简摘要，不保存完整原始对话。通过 Life Coach 技能生成的 agent 质量自评，依照用户对该项的持续授权写入 `quality_assess.md`，不显示在对话回复中；仅在对话明确结束或自然收束后追加，模板见 `quality_assess_template.md`。个人资料目录已被 Git 忽略。

## 重要限制

这只是 Codex 技能遵循的资料选择约定，不是用户认证或操作系统访问控制。技能不会验证用户名或密码，也不能阻止拥有此工作区权限的人直接查看其他资料目录。不要在 Codex 对话中输入密码；不同用户若需要彼此保密，应使用不同操作系统账号、不同工作区权限，或改用有真实身份认证与授权的独立应用。
