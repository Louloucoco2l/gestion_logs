"""
Configuration du système de logging pour le projet.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configure et retourne un logger pour le projet.

    Args:
        name: Nom du logger
        log_file: Chemin vers le fichier de log (optionnel)
        level: Niveau de logging

    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Éviter la duplication des handlers
    if logger.handlers:
        return logger

    # Format des messages de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler pour fichier si spécifié
    if log_file:
        # S'assurer que le répertoire existe
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_project_logger(log_to_file: bool = True) -> logging.Logger:
    """
    Retourne le logger principal du projet.

    Args:
        log_to_file: Si True, les logs sont aussi écrits dans un fichier

    Returns:
        Logger configuré pour le projet
    """
    log_file = None
    if log_to_file:
        log_file = Path.cwd() / "logs" / "gestionlogs.log"

    return setup_logger("gestionlogs", log_file)
