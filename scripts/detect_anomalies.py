"""
Script de détection d'anomalies.

Ce script permet de détecter des anomalies dans un fichier CSV
en utilisant un modèle précédemment entraîné.
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.hdfs_detector import HDFSDetector
from utils.logger import get_project_logger


def main():
    """Fonction principale du script de détection."""
    parser = argparse.ArgumentParser(
        description="Détecte des anomalies dans un fichier CSV"
    )
    parser.add_argument(
        "--data", 
        required=True, 
        help="Nom du fichier CSV à analyser"
    )
    parser.add_argument(
        "--model-type", 
        default="hdfs", 
        choices=["hdfs"],
        help="Type de modèle à utiliser"
    )

    args = parser.parse_args()

    # Configuration du logger
    logger = get_project_logger()
    logger.info("Début de la détection d'anomalies")

    try:
        # Initialisation du détecteur selon le type
        if args.model_type == "hdfs":
            detector = HDFSDetector()
        else:
            logger.error(f"Type de modèle non supporté: {args.model_type}")
            return 1

        # Détection des anomalies
        success = detector.detect_anomalies_in_file(args.data)

        if success:
            logger.info("Détection terminée avec succès")
            return 0
        else:
            logger.error("Échec de la détection")
            return 1

    except Exception as e:
        logger.error(f"Erreur lors de la détection: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
