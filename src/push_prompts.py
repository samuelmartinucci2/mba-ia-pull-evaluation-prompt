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
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).
    """
    try:
        # Reconstrói o ChatPromptTemplate a partir do system_prompt e user_prompt
        messages = []
        if prompt_data.get("system_prompt"):
            messages.append(("system", prompt_data["system_prompt"]))
        if prompt_data.get("user_prompt"):
            messages.append(("human", prompt_data["user_prompt"]))
            
        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        # Consolida as tags bases com as técnicas aplicadas
        tags = prompt_data.get("tags", []) + prompt_data.get("techniques_applied", [])
        
        print(f"Enviando prompt '{prompt_name}' ao LangSmith Hub...")
        
        client = Client()
        client.push_prompt(
            prompt_identifier=prompt_name,
            object=prompt_template,
            is_public=True,
            description=prompt_data.get("description", ""),
            tags=tags
        )
        
        print("✓ Prompt enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar prompt: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")
    
    # 1. Configurações centrais do escopo (fácil de alterar depois)
    prompt_key = "bug_to_user_story_v2"
    input_path = f"prompts/{prompt_key}.yml"
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    
    # 2. Verifica todas as variáveis de ambiente necessárias de uma vez
    if not check_env_vars(required_vars):
        return 1
    
    username = os.getenv("USERNAME_LANGSMITH_HUB")
        
    # 3. Carrega o arquivo YAML local
    if not os.path.exists(input_path):
        print(f"❌ Arquivo de prompts otimizados não encontrado em: {input_path}")
        return 1
        
    yaml_data = load_yaml(input_path) or {}
    if prompt_key not in yaml_data:
        print(f"❌ Chave '{prompt_key}' não encontrada no arquivo {input_path}")
        return 1
        
    prompt_data = yaml_data[prompt_key]
    
    # 4. Valida a estrutura usando diretamente a função do utils
    is_valid, errors = validate_prompt_structure(prompt_data)
    if not is_valid:
        print("❌ Erros de validação encontrados no prompt:")
        for err in errors:
            print(f"  - {err}")
        return 1
    
    print("✓ Prompt validado com sucesso localmente.")
        
    # 5. Executa o push para o LangSmith Hub
    dest_prompt_name = f"{username}/{prompt_key}"
    
    if push_prompt_to_langsmith(dest_prompt_name, prompt_data):
        print(f"\n✅ PUSH CONCLUÍDO! O seu prompt está disponível em:")
        print(f"   https://smith.langchain.com/hub/{dest_prompt_name}")
        return 0
    
    print("\n❌ PUSH FALHOU!")
    return 1


if __name__ == "__main__":
    sys.exit(main())
