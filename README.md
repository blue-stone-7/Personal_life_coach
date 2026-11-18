# 个人成长对话 agent

这是一个以平台无关提示词为核心的本地 API agent 起步项目。核心行为规范在 `core_prompt.md`，本地 Python 命令行程序负责调用兼容 OpenAI Chat Completions 的 API。更换服务商时，通常只需更改 `.env` 中的 API 地址、密钥和模型；若服务商接口不兼容该格式，则需要替换 `agent.py` 中的请求适配层。

## 目录

- `core_prompt.md`：平台无关的角色、对话流程、安全边界和记忆规则。
- `profile_template.md`：可移植的个人资料模板。
- `agent.py`：本地命令行 agent；对话历史仅保存在当前进程内存中。
- `.env.example`：API 和运行参数示例。实际 `.env` 不应提交。

## 本地运行

需要 Python 3.10 或更新版本及一个兼容 OpenAI Chat Completions 的 API 服务。

1. 在本目录创建虚拟环境并安装依赖：

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. 复制 `.env.example` 为 `.env`，填写 `API_BASE_URL`、`API_KEY` 和服务商支持的 `MODEL`。
3. 运行：

   ```powershell
   python agent.py
   ```

输入 `/reset` 清空本次进程中的对话上下文，输入 `/quit` 退出。

## 个人资料与隐私

程序会在每次请求时读取 `PROFILE_PATH` 指向的资料文件，默认是 `data/profile.md`。该私有路径已加入 `.gitignore`；用户可自行创建文件并从 `profile_template.md` 复制模板。agent 不会自动改写文件，也不会把对话内容自动保存成长期记忆。若希望保存某次对话的内容，请先审阅并手动更新个人资料。

本地运行不代表 API 请求完全留在本机：对话内容会发送到 `.env` 配置的 API 服务商。请先确认该服务商的数据处理与保留设置，并避免上传你不愿分享的敏感内容。API 密钥只放在本地 `.env`，不要提交到 Git。

## 跨平台维护

把 `core_prompt.md` 作为行为规范的单一来源。其他平台适配应引用或复制该文件，并保留其安全边界、用户确认式记忆规则和自然对话方式。平台专属 API 参数、工具调用和记忆功能放在适配层，不要混入核心提示词。
