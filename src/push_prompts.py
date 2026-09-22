"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurado no arquivo .env.")
        return False

    system_prompt = prompt_data.get("system_prompt", "").strip()
    user_prompt = prompt_data.get("user_prompt", "{bug_report}").strip()
    description = prompt_data.get("description", "Prompt otimizado para conversão de bugs em User Stories")
    tags = prompt_data.get("tags", [])

    if not system_prompt:
        print("❌ 'system_prompt' está vazio.")
        return False

    try:
        client = Client()
        full_prompt_name = f"{username}/{prompt_name}"
        print(f"Montando ChatPromptTemplate para '{full_prompt_name}'...")

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        print(f"Enviando prompt ao LangSmith Hub como PÚBLICO...")
        url = client.push_prompt(
            full_prompt_name,
            object=prompt,
            is_public=True,
            description=description,
            tags=tags
        )

        print(f"✓ Prompt publicado com sucesso!")
        print(f"✓ URL pública: {url}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt para o LangSmith: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPT OTIMIZADO PARA O LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    prompts_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
    data = load_yaml(str(prompts_file))

    if not data or "bug_to_user_story_v2" not in data:
        print(f"❌ Não foi possível carregar 'bug_to_user_story_v2' de {prompts_file}")
        return 1

    prompt_data = data["bug_to_user_story_v2"]

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Erros de validação encontrados no prompt:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print("✓ Estrutura do prompt validada com sucesso.")
    success = push_prompt_to_langsmith("bug_to_user_story_v2", prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
