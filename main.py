"""
Point d'entrée principal du système de détection d'anomalies.

Ce script sert de point d'entrée unique pour toutes les fonctionnalités
du système de détection d'anomalies dans les logs.
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from models.hdfs_detector import HDFSDetector
    from utils.logger import get_project_logger
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que le répertoire 'src' existe avec les modules requis")
    sys.exit(1)


def main():
    """Fonction principale du programme."""
    parser = argparse.ArgumentParser(
        description="Système de détection d'anomalies dans les logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s                                    # Interface interactive
  %(prog)s create normal_trace.csv            # Créer un modèle
  %(prog)s detect failure_trace.csv           # Détecter des anomalies
  %(prog)s list                              # Lister les fichiers CSV
        """
    )

    parser.add_argument(
        "action",
        nargs="?",
        choices=["create", "detect", "list"],
        help="Action à effectuer"
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="Nom du fichier CSV"
    )
    parser.add_argument(
        "--model-type",
        default="hdfs",
        choices=["hdfs"],
        help="Type de modèle (défaut: hdfs)"
    )
    parser.add_argument(
        "--contamination",
        type=float,
        default=0.01,
        help="Proportion d'anomalies attendues (défaut: 0.01)"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["create", "detect", "list", "visualize"],  # Ajouter "visualize"
        help="Action à effectuer"
    )

    args = parser.parse_args()

    # Configuration du logger
    try:
        logger = get_project_logger()
    except Exception as e:
        print(f"Erreur de configuration du logger: {e}")
        # Fallback vers print si le logger ne fonctionne pas
        logger = None

    try:
        # Initialisation du détecteur
        detector = HDFSDetector(contamination=args.contamination)

        # Traitement selon l'action demandée
        if args.action == "create":
            if not args.filename:
                print("Erreur: Nom de fichier requis pour la création de modèle")
                return 1

            if logger:
                logger.info(f"Création de modèle à partir de {args.filename}")
            success = detector.create_model_from_file(args.filename)
            return 0 if success else 1

        elif args.action == "detect":
            if not args.filename:
                print("Erreur: Nom de fichier requis pour la détection")
                return 1

            if logger:
                logger.info(f"Détection d'anomalies dans {args.filename}")
            success = detector.detect_anomalies_in_file(args.filename)
            return 0 if success else 1

        elif args.action == "list":
            detector.list_available_files()
            return 0

        elif args.action == "visualize":
            from scripts.visualize_anomalies import main as visualize_main
            return visualize_main()

        else:
            # Mode interactif si aucune action spécifiée
            try:
                # Import dynamique pour éviter les erreurs si le module n'existe pas
                scripts_dir = current_dir / "scripts"
                sys.path.insert(0, str(scripts_dir))
                from interactive_cli import InteractiveCLI
                cli = InteractiveCLI()
                cli.run()
                return 0
            except ImportError:
                print("Interface interactive non disponible")
                print("Utilisez: python main.py create|detect|list <filename>")
                return 1

    except Exception as e:
        error_msg = f"Erreur: {e}"
        if logger:
            logger.error(error_msg)
        print(error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
