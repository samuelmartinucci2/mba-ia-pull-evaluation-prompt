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
    def setup_prompts(self):
        # Carrega o prompt v2
        self.prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        self.prompt_data = self.prompts.get("bug_to_user_story_v2", {})

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data
        assert self.prompt_data["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        persona_terms = ["Product Manager", "PO", "Product Owner", "assistente", "persona", "Você é"]
        assert any(term.lower() in system_prompt.lower() for term in persona_terms)

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        format_terms = ["Como um", "Como", "Eu quero", "Para que", "Critérios de Aceitação", "Given-When-Then", "Dado", "Quando", "Então", "Markdown"]
        assert any(term.lower() in system_prompt.lower() for term in format_terms)

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        example_terms = ["Exemplo", "Few-shot", "Input:", "Output:", "Exemplo 1", "Exemplo 2", "Exemplo 3"]
        assert any(term.lower() in system_prompt.lower() for term in example_terms)

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        assert "TODO" not in system_prompt

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])