from .docker import Ollama


def get_engine_factory_by_name(name: str):
    if name.lower() == "ollama":
        return Ollama
    