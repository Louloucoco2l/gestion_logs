"""
Script d'entraînement des modèles de détection d'anomalies.

Ce script permet d'entraîner un modèle de détection d'anomalies
à partir d'un fichier CSV contenant des données normales.
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.hdfs_detector import HDFSDetector
from utils.logger import get_project_logger


def main():
    """Fonction principale du script d'entraînement."""
    parser = argparse.ArgumentParser(
        description="Entraîne un modèle de détection d'anomalies"
    )
    parser.add_argument(
        "--data", 
        required=True, 
        help="Nom du fichier CSV d'entraînement"
    )
    parser.add_argument(
        "--model-type", 
        default="hdfs", 
        choices=["hdfs"],
        help="Type de modèle à entraîner"
    )
    parser.add_argument(
        "--contamination", 
        type=float, 
        default=0.01,
        help="Proportion d'anomalies attendues (défaut: 0.01 = 1%%)"
    )

    args = parser.parse_args()

    # Configuration du logger
    logger = get_project_logger()
    logger.info("Début de l'entraînement du modèle")

    try:
        # Initialisation du détecteur selon le type
        if args.model_type == "hdfs":
            detector = HDFSDetector(contamination=args.contamination)
        else:
            logger.error(f"Type de modèle non supporté: {args.model_type}")
            return 1

        # Entraînement du modèle
        success = detector.create_model_from_file(args.data)

        if success:
            logger.info("Entraînement terminé avec succès")
            return 0
        else:
            logger.error("Échec de l'entraînement")
            return 1

    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
