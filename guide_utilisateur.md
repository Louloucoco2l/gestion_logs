# Guide Utilisateur - Système de Détection d'Anomalies dans les Logs

## Qu'est-ce que ce programme ?

Ce programme est un outil intelligent qui analyse automatiquement vos fichiers de logs (journaux d'événements) pour détecter des comportements anormaux ou suspects. Imaginez-le comme un détective numérique qui examine des milliers de lignes de données pour repérer ce qui sort de l'ordinaire.

## À quoi ça sert ?

Dans le monde informatique, les systèmes génèrent constamment des logs - des enregistrements de tout ce qui se passe (connexions, erreurs, transferts de fichiers, etc.). Analyser manuellement ces logs est impossible quand on a des millions de lignes. Ce programme le fait automatiquement et vous signale les anomalies qui pourraient indiquer :

- Des pannes système
- Des tentatives de piratage
- Des dysfonctionnements
- Des comportements inhabituels

## Comment ça marche en gros ?

Le programme fonctionne en deux étapes principales :

### Étape 1 : Apprentissage (Création du modèle)

- Vous donnez au programme un fichier contenant des données "normales"
- Il étudie ces données et apprend ce qui est considéré comme normal
- Il crée un "modèle" (une sorte de référence) de ce comportement normal

### Étape 2 : Détection (Analyse)

- Vous donnez au programme un nouveau fichier à analyser
- Il compare ce nouveau fichier avec ce qu'il a appris
- Il vous signale tout ce qui lui semble anormal

## Types de fichiers supportés

Le programme est spécialement conçu pour analyser des logs au format HDFS (Hadoop Distributed File System). Ces fichiers ressemblent à des tableaux Excel où :

- Chaque ligne représente une séquence d'événements
- Chaque colonne représente un type d'événement différent
- Les chiffres indiquent combien de fois chaque événement s'est produit

**Exemple simplifié :**

```
TaskID, Connexion, Erreur, Transfert, Déconnexion  
Task_1, 5, 0, 3, 1  
Task_2, 2, 1, 4, 1  
```

## Comment utiliser le programme ?

### Méthode 1 : Interface Simple (Recommandée pour débutants)

1. Ouvrez votre terminal/invite de commande
2. Naviguez vers le dossier du programme
3. Tapez : `python main.py`
4. Le programme vous propose un menu avec 4 options :
   - Option 1 : Créer un modèle (apprentissage)
   - Option 2 : Analyser un fichier (détection)
   - Option 3 : Voir les fichiers disponibles
   - Option 4 : Quitter

### Méthode 2 : Ligne de commande (Pour utilisateurs avancés)

Vous pouvez donner des instructions directes :

- `python main.py create nom_fichier_normal.csv` : Crée un modèle
- `python main.py detect nom_fichier_suspect.csv` : Analyse un fichier
- `python main.py list` : Affiche les fichiers disponibles

## Étapes détaillées d'utilisation

### Première utilisation : Créer votre modèle

#### 1. Préparez vos données normales

- Vous avez besoin d'un fichier CSV contenant des données "normales"
- Ce fichier doit représenter le fonctionnement habituel de votre système
- Plus vous avez de données normales, meilleur sera le modèle

#### 2. Lancez la création du modèle

- Choisissez l'option 1 dans le menu
- Entrez le nom de votre fichier (ex: "donnees_normales.csv")
- Le programme va :
  - Charger vos données
  - Les analyser et les nettoyer
  - Créer un modèle d'apprentissage
  - Sauvegarder ce modèle pour usage futur

#### 3. Vérifiez le résultat

- Le programme vous indique si la création s'est bien passée
- Il vous donne des statistiques sur les données analysées
- Le modèle est sauvegardé automatiquement

### Utilisation courante : Détecter des anomalies

#### 1. Préparez le fichier à analyser

- Vous avez un nouveau fichier CSV à examiner
- Ce fichier doit avoir la même structure que celui utilisé pour l'apprentissage

#### 2. Lancez la détection

- Choisissez l'option 2 dans le menu
- Entrez le nom du fichier à analyser
- Le programme va :
  - Charger le modèle précédemment créé
  - Analyser votre nouveau fichier
  - Comparer avec ce qu'il considère comme normal
  - Identifier les anomalies

#### 3. Interprétez les résultats

Le programme vous donne :
- Le nombre total d'anomalies trouvées
- Le pourcentage d'anomalies
- Le détail des 5 anomalies les plus importantes
- Un fichier de résultats sauvegardé automatiquement

## Comment interpréter les résultats ?

**Exemple de résultat typique :**

```
RÉSULTATS DE L'ANALYSE:  
- Total analysé: 10000 séquences  
- Anomalies trouvées: 150  
- Pourcentage d'anomalies: 1.50%  

TOP 5 ANOMALIES LES PLUS SÉVÈRES:  
1. Ligne 5623: Score = -0.211  
   Événements principaux: {'Erreur_Réseau': 25, 'Timeout': 10}  
```

### Que signifient ces informations ?

- **Total analysé** : Nombre de lignes examinées dans votre fichier
- **Anomalies trouvées** : Nombre de lignes considérées comme anormales
- **Pourcentage** : Proportion d'anomalies (1-5% est généralement normal, plus de 10% peut indiquer un problème)
- **Score** : Plus le score est négatif, plus l'anomalie est sévère
- **Événements principaux** : Les types d'événements qui rendent cette ligne suspecte

## Comment réagir selon les résultats ?

### Si vous avez 0-2% d'anomalies :
- C'est normal, votre système fonctionne bien
- Examinez quand même les anomalies les plus sévères par précaution

### Si vous avez 5-15% d'anomalies :
- Il peut y avoir un problème mineur
- Vérifiez les événements principaux des top anomalies
- Comparez avec d'autres périodes

### Si vous avez plus de 20% d'anomalies :
- Problème potentiellement sérieux
- Examinez en détail les types d'événements anormaux
- Vérifiez si votre modèle d'apprentissage était approprié

## Organisation des fichiers

Le programme organise automatiquement vos fichiers :

```
votre_projet/  
├── data/  
│   ├── raw/          # Vos fichiers CSV originaux  
│   └── results/      # Résultats des analyses  
├── models/           # Modèles d'apprentissage sauvegardés  
├── logs/            # Journaux du programme  
└── main.py          # Programme principal  
```

## Conseils pratiques

### Pour de meilleurs résultats :

#### 1. Qualité des données d'apprentissage
- Utilisez des données vraiment normales (pas de pannes connues)
- Plus vous avez de données, mieux c'est (idéalement 10000+ lignes)
- Assurez-vous que les données couvrent différentes situations normales

#### 2. Cohérence des formats
- Tous vos fichiers CSV doivent avoir la même structure
- Même nombre de colonnes, mêmes noms de colonnes
- Même format de données

#### 3. Interprétation intelligente
- Un taux d'anomalies très bas peut indiquer que votre modèle est trop permissif
- Un taux très élevé peut indiquer que votre modèle est trop strict
- Ajustez le seuil de sensibilité si nécessaire

## Résolution de problèmes courants

### "Fichier non trouvé"
- Vérifiez que votre fichier CSV est dans le bon dossier
- Utilisez l'option "Lister les fichiers" pour voir ce qui est disponible

### "Erreur de format"
- Votre fichier CSV doit être bien formaté
- Vérifiez qu'il n'y a pas de caractères spéciaux dans les noms de colonnes

### "Pas assez de données"
- Votre fichier doit contenir au moins quelques centaines de lignes
- Pour l'apprentissage, plus c'est mieux

### "Modèle non trouvé"
- Vous devez d'abord créer un modèle avant de pouvoir analyser
- Utilisez l'option 1 pour créer un modèle

## Maintenance et bonnes pratiques

### Mise à jour du modèle :
- Recréez votre modèle régulièrement avec de nouvelles données normales
- Si votre système évolue, le modèle doit évoluer aussi
- Gardez une trace de quand vous avez créé chaque modèle

### Archivage des résultats :
- Le programme sauvegarde automatiquement tous les résultats
- Consultez régulièrement le dossier "results" pour suivre l'évolution
- Comparez les analyses dans le temps pour détecter des tendances

### Surveillance continue :
- Analysez régulièrement vos nouveaux logs
- Établissez une routine (quotidienne, hebdomadaire)
- Documentez les anomalies importantes que vous découvrez

## Limitations à connaître

- Le programme ne peut analyser que des fichiers au format CSV
- Il est optimisé pour les logs HDFS (format numérique)
- La qualité de détection dépend entièrement de la qualité des données d'apprentissage
- Il détecte les anomalies mais ne les explique pas automatiquement
- Les très gros fichiers (plus de 100MB) peuvent prendre du temps à traiter

## Support et aide

Si vous rencontrez des problèmes :

1. Vérifiez d'abord les messages d'erreur affichés
2. Consultez le fichier de log dans le dossier "logs"
3. Assurez-vous que vos fichiers CSV sont bien formatés
4. Vérifiez que vous avez suivi toutes les étapes dans l'ordre

Le programme est conçu pour être robuste et vous guider, mais n'hésitez pas à demander de l'aide technique si nécessaire.
