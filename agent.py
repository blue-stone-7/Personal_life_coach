"""Minimal local API agent using an OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class LifeCoachAgent:
    def __init__(self) -> None:
        self.base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.environ.get("API_KEY", "")
        self.model = os.environ.get("MODEL", "")
        if not self.api_key or not self.model:
            raise RuntimeError("Set API_KEY and MODEL in your .env file.")
        profile_path = Path(os.environ.get("PROFILE_PATH", "data/profile.md"))
        if not profile_path.is_absolute():
            profile_path = ROOT / profile_path
        self.profile_path = profile_path
        self.system_prompt = read_text(ROOT / "core_prompt.md")
        self.history: list[dict[str, str]] = []

    def reply(self, message: str) -> str:
        profile = read_text(self.profile_path)
        context = self.system_prompt
        if profile.strip():
            context += "\n\n## 用户提供的个人资料（作为可修订背景；以用户当前表述为准）\n" + profile
        messages = [{"role": "system", "content": context}, *self.history,
                    {"role": "user", "content": message}]
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages},
            timeout=90,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        answer = data["choices"][0]["message"]["content"]
        if not isinstance(answer, str):
            raise RuntimeError("The API returned an unsupported message format.")
        self.history.extend([{"role": "user", "content": message},
                             {"role": "assistant", "content": answer}])
        return answer


def main() -> None:
    agent = LifeCoachAgent()
    print("个人成长对话 agent 已启动。输入 /reset 清空本次会话，输入 /quit 退出。")
    while True:
        try:
            message = input("\n你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n会话已结束。")
            break
        if message == "/quit":
            break
        if message == "/reset":
            agent.history.clear()
            print("本次会话上下文已清空。")
            continue
        if not message:
            continue
        try:
            print(f"\nAgent：{agent.reply(message)}")
        except (httpx.HTTPError, KeyError, RuntimeError) as exc:
            print(f"\n请求失败：{exc}")


if __name__ == "__main__":
    main()
