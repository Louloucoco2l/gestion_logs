"""
Script de détection d'anomalies.

Ce script permet de détecter des anomalies dans un fichier CSV
en utilisant un modèle précédemment entraîné, avec des options
avancées pour la visualisation et la catégorisation des résultats.
"""

import sys
import argparse
from pathlib import Path
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.hdfs_detector import HDFSDetector
from utils.logger import get_project_logger


def generate_report(results, anomaly_data=None, output_dir=None):
    """
    Génère un rapport détaillé des anomalies détectées.

    Args:
        results: Dictionnaire contenant les résultats de l'analyse
        anomaly_data: DataFrame contenant les données d'anomalies (optionnel)
        output_dir: Répertoire de sortie pour les visualisations

    Returns:
        Chemin vers le rapport généré
    """
    logger = get_project_logger()

    if output_dir is None:
        output_dir = Path.cwd() / "data" / "reports"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Nom du fichier basé sur la date/heure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"anomaly_report_{timestamp}.txt"

    with open(report_path, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("RAPPORT DE DÉTECTION D'ANOMALIES\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Date d'analyse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Fichier analysé: {results['file_analyzed']}\n\n")

        f.write("RÉSUMÉ:\n")
        f.write(f"  - Total analysé: {results['total_sequences']} séquences\n")
        f.write(f"  - Anomalies trouvées: {results['anomalies_count']}\n")
        f.write(f"  - Pourcentage d'anomalies: {results['anomaly_rate']:.2f}%\n\n")

        f.write("PARAMÈTRES DU MODÈLE:\n")
        f.write(f"  - Contamination: {results['model_info']['contamination']}\n")
        f.write(f"  - PCA utilisée: {results['model_info']['use_pca']}\n")
        f.write(f"  - Nombre de features: {results['model_info']['n_features']}\n\n")

        if 'top_anomalies' in results and results['top_anomalies']:
            f.write("TOP ANOMALIES:\n")
            for i, anomaly in enumerate(results['top_anomalies'], 1):
                f.write(f"  {i}. Ligne {anomaly['index']+1}: Score = {anomaly['score']:.3f}\n")
                if anomaly.get('task_id'):
                    f.write(f"     TaskID: {anomaly['task_id']}\n")
                if 'top_events' in anomaly:
                    f.write("     Événements principaux:\n")
                    for event, count in anomaly['top_events'].items():
                        f.write(f"       - {event}: {count}\n")
                f.write("\n")

    logger.info(f"Rapport généré: {report_path}")

    # Générer des visualisations si les données d'anomalies sont disponibles
    if anomaly_data is not None and len(anomaly_data) > 0:
        try:
            # Distribution des scores d'anomalies
            plt.figure(figsize=(10, 6))
            sns.histplot(anomaly_data['anomaly_score'], kde=True)
            plt.title('Distribution des scores d anomalies')
            plt.xlabel('Score d anomalie')
            plt.ylabel('Fréquence')
            plt.grid(True, alpha=0.3)
            viz_path = output_dir / f"anomaly_scores_dist_{timestamp}.png"
            plt.savefig(viz_path)
            plt.close()
            logger.info(f"Visualisation générée: {viz_path}")

            # Top features pour les anomalies
            if len(anomaly_data.columns) > 2:  # Au moins quelques features + score
                # Sélectionner les colonnes numériques (exclure task_id si présent)
                numeric_cols = anomaly_data.select_dtypes(include=['number']).columns
                numeric_cols = [col for col in numeric_cols if col != 'anomaly_score']

                if numeric_cols:
                    # Calculer la somme de chaque feature pour les anomalies
                    feature_sums = anomaly_data[numeric_cols].sum().sort_values(ascending=False)
                    top_features = feature_sums.head(10)

                    plt.figure(figsize=(12, 6))
                    sns.barplot(x=top_features.index, y=top_features.values)
                    plt.title('Top 10 des événements les plus fréquents dans les anomalies')
                    plt.xlabel('Type d événement')
                    plt.ylabel('Fréquence totale')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    viz_path = output_dir / f"top_anomaly_events_{timestamp}.png"
                    plt.savefig(viz_path)
                    plt.close()
                    logger.info(f"Visualisation générée: {viz_path}")

        except Exception as e:
            logger.error(f"Erreur lors de la génération des visualisations: {e}")

    return report_path


def main():
    """Fonction principale du script de détection."""
    parser = argparse.ArgumentParser(
        description="Détecte des anomalies dans un fichier CSV avec options avancées"
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
    parser.add_argument(
        "--contamination",
        type=float,
        default=None,
        help="Proportion d'anomalies attendues (ex: 0.01 pour 1%)"
    )
    parser.add_argument(
        "--output-format",
        choices=["default", "json", "detailed"],
        default="default",
        help="Format de sortie des résultats"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Générer un rapport détaillé"
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Générer des visualisations"
    )

    args = parser.parse_args()

    # Configuration du logger
    logger = get_project_logger()
    logger.info("Début de la détection d'anomalies")

    try:
        # Initialisation du détecteur selon le type
        if args.model_type == "hdfs":
            detector_kwargs = {}
            if args.contamination is not None:
                detector_kwargs['contamination'] = args.contamination

            detector = HDFSDetector(**detector_kwargs)
        else:
            logger.error(f"Type de modèle non supporté: {args.model_type}")
            return 1

        # Détection des anomalies
        success = detector.detect_anomalies_in_file(args.data, output_format=args.output_format)

        if success:
            # Générer un rapport si demandé
            if args.report or args.visualize:
                # Charger les résultats JSON
                results_path = detector.project_root / "data" / "results" / f"anomalies_{args.data.replace('.csv', '')}.json"
                if results_path.exists():
                    with open(results_path, 'r') as f:
                        results = json.load(f)

                    # Charger les données d'anomalies pour les visualisations
                    anomaly_data = None
                    if args.visualize:
                        csv_path = results_path.with_suffix('.csv')
                        if csv_path.exists():
                            anomaly_data = pd.read_csv(csv_path)

                    # Générer le rapport
                    report_path = generate_report(results, anomaly_data)
                    logger.info(f"Rapport détaillé disponible: {report_path}")
                else:
                    logger.warning(f"Fichier de résultats non trouvé: {results_path}")

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
