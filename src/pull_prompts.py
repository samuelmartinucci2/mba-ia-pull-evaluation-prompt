"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
import yaml
from dotenv import load_dotenv
from langchain import hub
from utils import load_yaml, save_yaml, check_env_vars, print_section_header

load_dotenv()


def str_presenter(dumper, data):
    """Configura o yaml para salvar strings multilinha usando o estilo |"""
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def fetch_prompt_templates(prompt_name: str):
    """Busca o prompt no LangSmith Hub e extrai as strings de sistema e usuário."""
    prompt = hub.pull(prompt_name)
    system_prompt, user_prompt = "", ""

    if hasattr(prompt, 'messages'):
        for msg in prompt.messages:
            # Captura o tipo de forma mais segura (via atributo .type ou nome da classe)
            msg_type = getattr(msg, 'type', msg.__class__.__name__).lower()
            if "system" in msg_type:
                system_prompt = msg.prompt.template
            elif "human" in msg_type or "user" in msg_type:
                user_prompt = msg.prompt.template
    elif hasattr(prompt, 'template'):
        system_prompt = prompt.template

    return system_prompt, user_prompt


def update_prompt_file(prompt_key: str, prompt_name: str, output_path: str):
    """Busca o prompt, mescla com metadados existentes e salva o arquivo YAML."""
    # Metadados padrão caso o arquivo não exista
    metadata = {
        "description": "Prompt para converter relatos de bugs em User Stories",
        "version": "v1",
        "created_at": "2025-01-15",
        "tags": ["bug-analysis", "user-story", "product-management"]
    }

    # Se o arquivo já existir, preserva os metadados antigos de forma dinâmica
    if os.path.exists(output_path):
        existing_data = load_yaml(output_path) or {}
        if prompt_key in existing_data:
            old_meta = existing_data[prompt_key]
            metadata = {k: old_meta.get(k, v) for k, v in metadata.items()}

    # Busca os templates atualizados do LangSmith
    system_prompt, user_prompt = fetch_prompt_templates(prompt_name)

    # Monta a estrutura final combinando os dicionários
    yaml_data = {
        prompt_key: {
            **metadata,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
    }

    return save_yaml(yaml_data, output_path)


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")
    
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        print("⚠️  Aviso: LANGSMITH_API_KEY não configurada no .env. Tentando pull público...")
        
    # Centralização das variáveis de escopo
    prompt_key = "bug_to_user_story_v1"
    prompt_name = f"leonanluppi/{prompt_key}"
    output_path = f"prompts/{prompt_key}.yml"
        
    try:
        if update_prompt_file(prompt_key, prompt_name, output_path):
            print(f"✅ Prompt salvo com sucesso em: {output_path}")
            return 0
        
        print(f"❌ Erro ao salvar prompt no arquivo local: {output_path}")
        return 1
            
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
