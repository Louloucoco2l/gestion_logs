"""
Interface en ligne de commande interactive pour la gestion des anomalies.

Ce script fournit une interface utilisateur simple pour entraîner des modèles
et détecter des anomalies sans avoir à utiliser les arguments en ligne de commande.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.hdfs_detector import HDFSDetector
from utils.logger import get_project_logger


class InteractiveCLI:
    """Interface en ligne de commande interactive."""

    def __init__(self):
        """Initialise l'interface interactive."""
        self.detector = HDFSDetector()
        self.logger = get_project_logger()

    def show_menu(self):
        """Affiche le menu principal."""
        print("\nDÉTECTEUR D'ANOMALIES HDFS")
        print("=" * 50)
        print(f"Projet détecté: {self.detector.project_root}")
        print("Détecteur spécialisé pour le format HDFS vectorisé\n")

        print("Actions disponibles:")
        print("1. Créer un modèle HDFS (données d'entraînement)")
        print("2. Inspecter un CSV HDFS (détecter anomalies)")
        print("3. Lister les CSV disponibles")
        print("4. Quitter")

    def handle_create_model(self):
        """Gère la création d'un modèle."""
        csv_file = input("\nFichier CSV d'entraînement (ex: normal_trace.csv): ").strip()
        if csv_file:
            print("\nCréation du modèle en cours...")
            success = self.detector.create_model_from_file(csv_file)
            if success:
                print("\nModèle créé avec succès!")
            else:
                print("\nÉchec de la création du modèle.")
        else:
            print("Nom de fichier requis.")

    def handle_detect_anomalies(self):
        """Gère la détection d'anomalies."""
        csv_file = input("\nFichier CSV à inspecter: ").strip()
        if csv_file:
            print("\nDétection d'anomalies en cours...")
            success = self.detector.detect_anomalies_in_file(csv_file)
            if not success:
                print("\nÉchec de la détection d'anomalies.")
        else:
            print("Nom de fichier requis.")

    def handle_list_files(self):
        """Gère l'affichage de la liste des fichiers."""
        self.detector.list_available_files()

    def run(self):
        """Lance l'interface interactive."""
        while True:
            self.show_menu()

            try:
                choice = input("\nChoisissez (1-4): ").strip()

                if choice == '1':
                    self.handle_create_model()
                elif choice == '2':
                    self.handle_detect_anomalies()
                elif choice == '3':
                    self.handle_list_files()
                elif choice == '4':
                    print("\nAu revoir!")
                    break
                else:
                    print("\nChoix invalide. Veuillez choisir entre 1 et 4.")

            except KeyboardInterrupt:
                print("\n\nInterruption détectée. Au revoir!")
                break
            except Exception as e:
                self.logger.error(f"Erreur dans l'interface: {e}")
                print(f"\nErreur: {e}")


def main():
    """Fonction principale."""
    try:
        cli = InteractiveCLI()
        cli.run()
        return 0
    except Exception as e:
        print(f"Erreur fatale: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
