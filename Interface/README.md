# Guide d'Utilisation - Interface AVOSDIM

### 1. Installation des dépendances

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r Interface\requirements.txt
```

### 2. Lancement de l'interface

```powershell
cd Interface
streamlit run App.py
```

L'interface s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📋 Fonctionnalités

### 🏠 Page Accueil
- Vue d'ensemble du système
- Statut des données et des calculs
- Métriques rapides

### 📊 Page Analyses
- Visualisation des données historiques
- Statistiques descriptives
- Matrice de corrélation
- Conversion en temps de production

### ⚙️ Page Paramètres
- Configuration des capacités (shift durations, équipes min/max)
- Paramètres epsilon pour l'optimisation
- Temps de production par produit
- Paramètres de stockage et coupe

### 📈 Page Forecasting
- Exécution des prévisions avec Prophet
- Génération automatique des fichiers agrégés (5, 10, 20 jours)
- Visualisation des prévisions avec intervalles de confiance
- Métriques d'erreur (MAE, MSE, RMSE)
- Export CSV des résultats

### 🎯 Page Optimisation
- Optimisation multi-objectifs avec Gurobi
- Exploration de l'espace des solutions
- Identification du front de Pareto
- Visualisations 2D et 3D
- Export des matrices de production et stock

## 📝 Workflow Typique

1. **Charger les données** (barre latérale)
   - Uploader un fichier Excel/CSV
   - Ou charger des fichiers existants

2. **Analyser** (section Analyses)
   - Explorer les tendances historiques
   - Vérifier les corrélations

3. **Configurer** (section Paramètres)
   - Ajuster les capacités de production
   - Définir les contraintes epsilon
   - Configurer les temps de production

4. **Prévoir** (section Forecasting)
   - Définir l'horizon de prévision
   - Lancer le forecasting
   - Vérifier les prévisions

5. **Optimiser** (section Optimisation)
   - Choisir la méthode (Gurobi recommandé)
   - Lancer l'optimisation
   - Analyser les solutions Pareto-optimales
   - Sélectionner la meilleure solution

---

## 💡 Cas d'Usage Pratiques

### Cas 1: Analyse Rapide des Données
  
**Objectif**: Explorer les tendances et corrélations

1. Page " Analyses" → Onglet "Données Brutes"
2. Sélectionner 3-4 produits importants
3. Examiner les tendances temporelles
4. Onglet "Statistiques": vérifier la matrice de corrélation
5. Identifier les produits fortement corrélés

**Sortie**: Compréhension des patterns historiques
