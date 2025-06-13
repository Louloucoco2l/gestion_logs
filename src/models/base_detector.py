"""
Module de base pour les détecteurs d'anomalies.
Définit l'interface commune pour tous les types de détecteurs.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple, Optional, Dict, Any
import pickle
from pathlib import Path


class BaseAnomalyDetector(ABC):
    """
    Classe abstraite de base pour tous les détecteurs d'anomalies.

    Cette classe définit l'interface commune que doivent implémenter
    tous les détecteurs spécialisés (HDFS, logs texte, etc.).
    """

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialise le détecteur de base.

        Args:
            project_root: Chemin racine du projet. Si None, utilise le répertoire courant.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.is_trained = False

    @abstractmethod
    def load_data(self, file_path: str) -> Tuple[pd.DataFrame, list]:
        """
        Charge les données depuis un fichier.

        Args:
            file_path: Chemin vers le fichier de données

        Returns:
            Tuple contenant (données_preprocessées, noms_des_features)
        """
        pass

    @abstractmethod
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Préprocesse les données pour l'entraînement ou la prédiction.

        Args:
            data: DataFrame contenant les données brutes

        Returns:
            DataFrame avec les données préprocessées
        """
        pass

    @abstractmethod
    def train_model(self, data: pd.DataFrame) -> bool:
        """
        Entraîne le modèle de détection d'anomalies.

        Args:
            data: Données d'entraînement préprocessées

        Returns:
            True si l'entraînement s'est bien passé, False sinon
        """
        pass

    @abstractmethod
    def predict_anomalies(self, data: pd.DataFrame) -> Tuple[list, list]:
        """
        Prédit les anomalies dans les données.

        Args:
            data: Données à analyser

        Returns:
            Tuple contenant (prédictions, scores_d_anomalie)
        """
        pass

    def save_model(self, model_path: Optional[str] = None) -> bool:
        """
        Sauvegarde le modèle entraîné.

        Args:
            model_path: Chemin de sauvegarde. Si None, utilise un nom par défaut.

        Returns:
            True si la sauvegarde s'est bien passée, False sinon
        """
        if not self.is_trained:
            print("Erreur: Aucun modèle entraîné à sauvegarder")
            return False

        if model_path is None:
            model_path = self.project_root / f"{self.__class__.__name__.lower()}_model.pkl"

        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'model_type': self.__class__.__name__
            }

            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)

            print(f"Modèle sauvegardé: {model_path}")
            return True

        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    def load_model(self, model_path: str) -> bool:
        """
        Charge un modèle précédemment sauvegardé.

        Args:
            model_path: Chemin vers le fichier de modèle

        Returns:
            True si le chargement s'est bien passé, False sinon
        """
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)

            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            self.is_trained = True

            print(f"Modèle chargé: {model_path}")
            return True

        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return False
