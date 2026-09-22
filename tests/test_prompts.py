"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        prompts_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        self.data = load_prompts(str(prompts_file))
        assert "bug_to_user_story_v2" in self.data, "Chave bug_to_user_story_v2 não encontrada no YAML"
        self.prompt_data = self.data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "Campo 'system_prompt' não encontrado"
        assert self.prompt_data["system_prompt"] is not None, "Campo 'system_prompt' é None"
        assert len(self.prompt_data["system_prompt"].strip()) > 0, "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        role_indicators = [
            "Product Manager",
            "Tech Lead",
            "Especialista",
            "Analista de Requisitos",
            "Você é um"
        ]
        has_role = any(indicator.lower() in system_prompt.lower() for indicator in role_indicators)
        assert has_role, f"O prompt não define uma persona reconhecida. Indicadores esperados: {role_indicators}"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        format_indicators = [
            "markdown",
            "user story",
            "critérios de aceitação",
            "como um",
            "dado que"
        ]
        has_format = any(indicator.lower() in system_prompt.lower() for indicator in format_indicators)
        assert has_format, "O prompt não menciona o formato esperado (Markdown / User Story / BDD)"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        example_indicators = [
            "exemplo",
            "few-shot",
            "relato do bug",
            "resposta:"
        ]
        has_examples = any(indicator.lower() in system_prompt.lower() for indicator in example_indicators)
        assert has_examples, "O prompt não contém exemplos de Few-shot (entrada/saída)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        user_prompt = self.prompt_data.get("user_prompt", "")
        assert "[TODO]" not in system_prompt, "system_prompt contém marcador [TODO]"
        assert "TODO" not in system_prompt, "system_prompt contém TODO pendente"
        assert "[TODO]" not in user_prompt, "user_prompt contém marcador [TODO]"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas nos metadados, encontradas: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])