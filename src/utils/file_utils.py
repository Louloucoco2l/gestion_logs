"""
Utilitaires pour la gestion des fichiers et des chemins.
"""

from pathlib import Path
from typing import List, Optional
import os


def find_files_by_extension(root_path: str, extension: str) -> List[Path]:
    """
    Recherche tous les fichiers avec une extension donnée dans un répertoire.

    Args:
        root_path: Chemin racine de la recherche
        extension: Extension à rechercher (ex: '.csv', '.txt')

    Returns:
        Liste des chemins vers les fichiers trouvés
    """
    root = Path(root_path)
    if not root.exists():
        return []

    return list(root.rglob(f"*{extension}"))


def ensure_directory_exists(directory_path: str) -> bool:
    """
    S'assure qu'un répertoire existe, le crée si nécessaire.

    Args:
        directory_path: Chemin du répertoire

    Returns:
        True si le répertoire existe ou a été créé, False sinon
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erreur lors de la création du répertoire {directory_path}: {e}")
        return False


def get_file_size_mb(file_path: str) -> float:
    """
    Retourne la taille d'un fichier en mégaoctets.

    Args:
        file_path: Chemin vers le fichier

    Returns:
        Taille du fichier en MB, ou 0 si le fichier n'existe pas
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)  # Conversion en MB
    except (OSError, FileNotFoundError):
        return 0.0


def validate_csv_file(file_path: str) -> bool:
    """
    Valide qu'un fichier CSV peut être lu correctement.

    Args:
        file_path: Chemin vers le fichier CSV

    Returns:
        True si le fichier est valide, False sinon
    """
    try:
        import pandas as pd
        # Essayer de lire juste les premières lignes pour validation
        pd.read_csv(file_path, nrows=5)
        return True
    except Exception:
        return False
