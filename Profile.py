import json
import os

class InvestorProfile:
    """
    Classe para armazenar o perfil do investidor.
    """
    def __init__(self, profile_filepath: str = "profile.json"):
        """
        Inicializa o perfil do investidor.
        """
        self.profile_filepath = profile_filepath

    def save_profile_to_file(self, profile: str):
        """
        Salva o perfil do investidor em um arquivo JSON.
        """
        with open(self.profile_filepath, "w", encoding='utf-8') as file:
            json.dump(profile, file, ensure_ascii=False, indent=4)
            
    def load_profile_from_file(self) -> str:
        """
        Carrega o perfil do investidor de um arquivo JSON.
        """
        if not os.path.exists(self.profile_filepath):
            return None
        with open(self.profile_filepath, "r", encoding='utf-8') as file:
            profile = file.read()
            return json.loads(profile) if profile else None