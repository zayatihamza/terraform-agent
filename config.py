import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class MilvusConfig:
    """Configuration pour Milvus"""
    host: str = "localhost"
    port: str = "19530"
    collection_name: str = "cloudstack_docs"
    dimension: int = 1024

@dataclass
class GroqConfig:
    """Configuration pour Groq"""
    api_key: Optional[str] = None
    default_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.1
    max_tokens: int = 2048

@dataclass
class TerraformConfig:
    """Configuration pour Terraform"""
    output_dir: str = "terraform_output"
    auto_approve: bool = False
    timeout_seconds: int = 300

@dataclass
class SystemConfig:
    """Configuration globale du système"""
    milvus: MilvusConfig
    groq: GroqConfig
    terraform: TerraformConfig
    debug_mode: bool = False
    log_level: str = "INFO"

def load_config() -> SystemConfig:
    """Charge la configuration depuis les variables d'environnement"""
    return SystemConfig(
        milvus=MilvusConfig(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530"),
            collection_name=os.getenv("MILVUS_COLLECTION", "cloudstack_docs")
        ),
        groq=GroqConfig(
            api_key=os.getenv("GROQ_API_KEY"),
            default_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "2048"))
        ),
        terraform=TerraformConfig(
            output_dir=os.getenv("TERRAFORM_OUTPUT_DIR", "terraform_output"),
            auto_approve=os.getenv("TERRAFORM_AUTO_APPROVE", "false").lower() == "true"
        ),
        debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )
