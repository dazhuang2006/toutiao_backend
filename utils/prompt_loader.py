from pathlib import Path


class PromptLoader:
    """Prompt 加载器"""

    def __init__(self):
        # 项目根目录/prompts
        self.prompt_dir = (
            Path(__file__).resolve().parent.parent / "prompts"
        )

    def load(self, prompt_name: str) -> str:
        """
        加载 Prompt

        Args:
            prompt_name: Prompt 文件名（不需要 .txt）

        Returns:
            Prompt 内容
        """
        prompt_path = self.prompt_dir / f"{prompt_name}.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt 文件不存在：{prompt_path}"
            )

        return prompt_path.read_text(
            encoding="utf-8"
        )


prompt_loader = PromptLoader()