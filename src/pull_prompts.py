"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Faz o pull do prompt semente leonanluppi/bug_to_user_story_v1 e salva em prompts/bug_to_user_story_v1.yml.
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v1.yml"

    try:
        print(f"Conectando ao LangSmith...")
        client = Client()

        print(f"Puxando prompt '{prompt_name}'...")
        prompt = client.pull_prompt(prompt_name, dangerously_pull_public_prompt=True)
        print("✓ Prompt obtido com sucesso do LangSmith Hub.")

        system_prompt = ""
        user_prompt = "{bug_report}"

        if hasattr(prompt, "messages"):
            for msg in prompt.messages:
                content = ""
                if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
                    content = msg.prompt.template
                elif hasattr(msg, "content"):
                    content = str(msg.content)
                elif isinstance(msg, tuple) and len(msg) >= 2:
                    content = str(msg[1])

                cls_name = msg.__class__.__name__.lower()
                role = getattr(msg, "role", "") or getattr(msg, "type", "")

                if "system" in cls_name or role == "system":
                    system_prompt = content
                elif "human" in cls_name or "user" in cls_name or role in ("human", "user"):
                    user_prompt = content
                elif not system_prompt:
                    system_prompt = content
                else:
                    user_prompt = content

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }

        if save_yaml(prompt_data, str(output_path)):
            print(f"✓ Prompt salvo com sucesso em: {output_path}")
            return True
        else:
            print(f"❌ Falha ao salvar arquivo YAML em: {output_path}")
            return False

    except Exception as e:
        print(f"❌ Erro durante o pull do prompt: {e}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
