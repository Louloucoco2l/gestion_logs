"""
Détecteur d'anomalies spécialisé pour le format HDFS vectorisé.

Ce module implémente un détecteur spécifiquement conçu pour analyser
les logs HDFS sous forme vectorisée, où chaque colonne représente
un type d'événement et les valeurs sont des compteurs d'occurrences.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import warnings

from .base_detector import BaseAnomalyDetector

warnings.filterwarnings('ignore')


class HDFSDetector(BaseAnomalyDetector):
    """
    Détecteur d'anomalies spécialisé pour le format HDFS vectorisé.

    Ce détecteur est optimisé pour analyser des logs HDFS où:
    - Chaque ligne représente une séquence d'événements
    - Chaque colonne représente un type d'événement spécifique
    - Les valeurs sont des compteurs d'occurrences (0, 1, 2, ...)
    """

    def __init__(self, project_root: Optional[str] = None, contamination: float = 0.01):
        """
        Initialise le détecteur HDFS.

        Args:
            project_root: Chemin racine du projet
            contamination: Proportion d'anomalies attendues (0.01 = 1%)
        """
        super().__init__(project_root)
        self.contamination = contamination
        self.pca = None
        self.model_path = self.project_root / "models" / "hdfs_anomaly_model.pkl"

        # Créer le dossier models s'il n'existe pas
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

    def find_csv_files(self) -> list:
        """
        Recherche tous les fichiers CSV dans le projet.

        Returns:
            Liste des chemins vers les fichiers CSV trouvés
        """
        csv_files = []
        search_dirs = [
            self.project_root / "data" / "raw",
            self.project_root / "data",
            self.project_root
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                csv_files.extend(list(search_dir.glob("*.csv")))

        return sorted(set(csv_files))

    def load_data(self, file_path: str) -> Tuple[pd.DataFrame, list]:
        """
        Charge les données HDFS vectorisées depuis un fichier CSV.

        Args:
            file_path: Chemin vers le fichier CSV

        Returns:
            Tuple contenant (données_features, noms_des_colonnes)
        """
        print(f"Chargement des données: {file_path}")

        try:
            # Essayer différents encodages pour la compatibilité
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception("Impossible de décoder le fichier avec les encodages supportés")

            print(f"Données chargées: {len(df)} lignes, {len(df.columns)} colonnes")

            # Identifier la colonne TaskID (généralement la première)
            if 'TaskID' in df.columns or df.columns[0].lower().startswith('task'):
                task_col = df.columns[0]
                feature_cols = [col for col in df.columns if col != task_col]
                print(f"Colonne TaskID détectée: {task_col}")
            else:
                # Pas de TaskID, toutes les colonnes sont des features
                feature_cols = df.columns.tolist()
                print("Aucune colonne TaskID détectée - toutes les colonnes sont des features")

            # Extraire les features et les convertir en numérique
            X = df[feature_cols].copy()

            # Conversion en numérique avec gestion des erreurs
            for col in X.columns:
                X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

            print(f"Features extraites: {len(feature_cols)} colonnes d'événements HDFS")

            # Afficher quelques exemples de colonnes pour information
            sample_cols = feature_cols[:3]
            print(f"Exemples de colonnes: {', '.join(sample_cols)}...")

            return X, feature_cols

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return None, None

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Préprocesse les données HDFS pour l'analyse.

        Args:
            data: DataFrame contenant les données brutes

        Returns:
            DataFrame avec les données préprocessées et normalisées
        """
        print("Préprocessing des données HDFS...")

        # Les données HDFS sont déjà sous forme numérique
        # On s'assure juste qu'il n'y a pas de valeurs manquantes
        data_clean = data.fillna(0)

        print(f"Données préprocessées: {data_clean.shape[0]} lignes × {data_clean.shape[1]} features")

        return data_clean

    def train_model(self, data: pd.DataFrame) -> bool:
        """
        Entraîne le modèle de détection d'anomalies sur les données HDFS.

        Args:
            data: Données d'entraînement préprocessées

        Returns:
            True si l'entraînement s'est bien passé, False sinon
        """
        try:
            print("Début de l'entraînement du modèle HDFS...")

            # Échantillonnage si le dataset est trop volumineux
            if len(data) > 50000:
                print(f"Échantillonnage de {len(data)} à 50000 lignes pour l'entraînement...")
                data = data.sample(n=50000, random_state=42)

            # Normalisation des données
            print("Normalisation des features...")
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(data)

            # Réduction de dimensionnalité si nécessaire
            if X_scaled.shape[1] > 100:
                print(f"Réduction de dimensionnalité: {X_scaled.shape[1]} -> 100 dimensions")
                self.pca = PCA(n_components=100, random_state=42)
                X_scaled = self.pca.fit_transform(X_scaled)

            # Configuration et entraînement du modèle Isolation Forest
            print("Entraînement du modèle Isolation Forest...")
            self.model = IsolationForest(
                contamination=self.contamination,  # Proportion d'anomalies attendues
                random_state=42,
                n_estimators=200,  # Nombre d'arbres pour plus de précision
                max_samples='auto'
            )

            self.model.fit(X_scaled)

            # Test sur les données d'entraînement pour validation
            predictions = self.model.predict(X_scaled)
            anomalies_count = np.sum(predictions == -1)

            print(f"Entraînement terminé!")
            print(f"Anomalies détectées sur les données d'entraînement: {anomalies_count}/{len(X_scaled)}")
            print(f"Taux d'anomalies: {anomalies_count/len(X_scaled)*100:.2f}%")

            self.is_trained = True
            return True

        except Exception as e:
            print(f"Erreur lors de l'entraînement: {e}")
            return False

    def predict_anomalies(self, data: pd.DataFrame) -> Tuple[list, list]:
        """
        Prédit les anomalies dans les données HDFS.

        Args:
            data: Données à analyser

        Returns:
            Tuple contenant (prédictions, scores_d_anomalie)
        """
        if not self.is_trained:
            raise Exception("Le modèle n'est pas entraîné. Entraînez d'abord le modèle.")

        print(f"Analyse de {len(data)} séquences HDFS...")

        # S'assurer que les colonnes correspondent à celles de l'entraînement
        missing_cols = set(self.feature_names) - set(data.columns)
        if missing_cols:
            print(f"Ajout de {len(missing_cols)} colonnes manquantes (remplies avec 0)")
            for col in missing_cols:
                data[col] = 0

        # Réorganiser les colonnes dans le même ordre que l'entraînement
        data_ordered = data[self.feature_names]

        # Normalisation avec le même scaler que l'entraînement
        X_scaled = self.scaler.transform(data_ordered)

        # Application de la PCA si elle a été utilisée
        if self.pca:
            X_scaled = self.pca.transform(X_scaled)

        # Prédiction des anomalies
        predictions = self.model.predict(X_scaled)
        scores = self.model.decision_function(X_scaled)

        return predictions.tolist(), scores.tolist()

    def create_model_from_file(self, csv_filename: str) -> bool:
        """
        Crée et entraîne un modèle à partir d'un fichier CSV.

        Args:
            csv_filename: Nom du fichier CSV d'entraînement

        Returns:
            True si la création s'est bien passée, False sinon
        """
        print("CRÉATION DU MODÈLE HDFS")
        print("=" * 40)

        # Rechercher le fichier
        csv_files = self.find_csv_files()
        file_path = None

        for f in csv_files:
            if csv_filename.lower() in f.name.lower():
                file_path = f
                break

        if not file_path:
            print(f"Erreur: Fichier '{csv_filename}' non trouvé")
            print("Fichiers CSV disponibles:")
            for f in csv_files:
                print(f"  - {f.name}")
            return False

        # Charger et préprocesser les données
        data, feature_names = self.load_data(file_path)
        if data is None:
            return False

        self.feature_names = feature_names
        processed_data = self.preprocess_data(data)

        # Entraîner le modèle
        success = self.train_model(processed_data)

        if success:
            # Sauvegarder le modèle
            self.save_model(self.model_path)
            print("CRÉATION DU MODÈLE TERMINÉE!")

        return success

    def detect_anomalies_in_file(self, csv_filename: str) -> bool:
        """
        Détecte les anomalies dans un fichier CSV.

        Args:
            csv_filename: Nom du fichier CSV à analyser

        Returns:
            True si l'analyse s'est bien passée, False sinon
        """
        print("DÉTECTION D'ANOMALIES HDFS")
        print("=" * 40)

        # Charger le modèle s'il n'est pas déjà chargé
        if not self.is_trained:
            if not self.model_path.exists():
                print("Erreur: Aucun modèle trouvé. Créez d'abord un modèle.")
                return False

            print("Chargement du modèle...")
            if not self.load_model(self.model_path):
                return False

        # Rechercher le fichier à analyser
        csv_files = self.find_csv_files()
        file_path = None

        for f in csv_files:
            if csv_filename.lower() in f.name.lower():
                file_path = f
                break

        if not file_path:
            print(f"Erreur: Fichier '{csv_filename}' non trouvé")
            return False

        # Charger et analyser les données
        data, _ = self.load_data(file_path)
        if data is None:
            return False

        processed_data = self.preprocess_data(data)
        predictions, scores = self.predict_anomalies(processed_data)

        # Analyser les résultats
        anomalies = np.array(predictions) == -1
        n_anomalies = np.sum(anomalies)

        print(f"\nRÉSULTATS DE L'ANALYSE:")
        print(f"  - Total analysé: {len(data)} séquences HDFS")
        print(f"  - Anomalies trouvées: {n_anomalies}")
        print(f"  - Pourcentage d'anomalies: {n_anomalies/len(data)*100:.2f}%")

        if n_anomalies > 0:
            # Analyser les anomalies les plus sévères
            anomaly_indices = np.where(anomalies)[0]
            anomaly_scores = np.array(scores)[anomalies]

            # Trier par score (plus négatif = plus anormal)
            sorted_indices = np.argsort(anomaly_scores)
            top_anomalies = anomaly_indices[sorted_indices[:min(5, len(sorted_indices))]]

            print(f"\nTOP 5 ANOMALIES LES PLUS SÉVÈRES:")
            for i, idx in enumerate(top_anomalies, 1):
                score = scores[idx]
                print(f"  {i}. Ligne {idx+1}: Score = {score:.3f}")

                # Identifier les événements les plus actifs pour cette anomalie
                row = processed_data.iloc[idx]
                active_features = row[row > 0].sort_values(ascending=False)
                if len(active_features) > 0:
                    top_features = active_features.head(3)
                    print(f"     Événements principaux: {dict(top_features)}")

            # Sauvegarder les anomalies détectées
            results_path = self.project_root / "data" / "results" / f"anomalies_{csv_filename.replace('.csv', '')}.csv"
            results_path.parent.mkdir(parents=True, exist_ok=True)

            anomaly_data = processed_data.iloc[anomaly_indices].copy()
            anomaly_data['anomaly_score'] = anomaly_scores
            anomaly_data.to_csv(results_path, index=False)
            print(f"\nAnomalies sauvegardées dans: {results_path}")
        else:
            print("\nAucune anomalie détectée avec le seuil actuel")
            print("Le modèle peut être trop strict ou les données sont très similaires aux données d'entraînement")

        return True

    def list_available_files(self):
        """Affiche la liste des fichiers CSV disponibles."""
        csv_files = self.find_csv_files()
        print("\nFichiers CSV disponibles:")
        if csv_files:
            for f in csv_files:
                print(f"  - {f.name} (dans {f.parent.name}/)")
        else:
            print("  Aucun fichier CSV trouvé")
