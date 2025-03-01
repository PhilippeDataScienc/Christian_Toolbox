# Christian_Toolbox

Développement d'outils d'aide à la décision pour des application en psychologie

# 🔄 Calculateur de Biorythmes

Une application web interactive permettant de visualiser et d'analyser vos cycles biologiques naturels en fonction de votre date de naissance, développée avec Streamlit et Plotly.

![Licence](https://img.shields.io/badge/licence-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.15+-red)

## 📷 Captures d'écran

![image](https://github.com/user-attachments/assets/a7ffe535-a549-445b-a9d0-0b86dcd2a21b)
![image](https://github.com/user-attachments/assets/7ec661a6-d4b9-494d-bf16-6c258088d221)



## ✨ Fonctionnalités

- **Calcul personnalisé** des biorythmes basé sur votre date de naissance
- Visualisation des **trois cycles biologiques** :
  - 🔴 Cycle physique (23 jours) : énergie, force, endurance, coordination
  - 🟡 Cycle émotionnel (28 jours) : humeur, sensibilité, créativité
  - 🔵 Cycle intellectuel (33 jours) : mémoire, concentration, raisonnement
- **Graphique interactif** montrant l'évolution des cycles sur un mois complet
- Indicateur de votre état actuel pour chaque cycle (valeurs et barres de progression)
- **Planificateur d'activités** avec visualisation des périodes favorables
- Interface entièrement en français avec dates formatées selon les standards français

## 🚀 Installation et démarrage

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-nom/calculateur-biorythmes.git
   cd calculateur-biorythmes
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Démarrage

Lancez l'application avec Streamlit :
```bash
streamlit run app.py
```

L'application sera accessible dans votre navigateur à l'adresse `http://localhost:8501`.

## 📖 Utilisation

1. **Saisissez votre date de naissance** dans le champ prévu à cet effet.
2. Visualisez vos biorythmes du jour sur les barres de progression.
3. Consultez le graphique mensuel pour voir l'évolution de vos cycles.
4. Utilisez le **planificateur d'activités** :
   - Entrez le nom de votre activité
   - Sélectionnez la catégorie correspondante (Physique, Émotionnel, Intellectuel)
   - Cliquez sur "+ Ajouter une activité"
5. Les périodes favorables pour chaque activité sont visualisées avec un dégradé d'opacité (plus l'opacité est forte, plus la période est favorable).

## 🛠️ Technologies utilisées

- **[Streamlit](https://streamlit.io/)** : framework pour l'interface utilisateur
- **[Plotly](https://plotly.com/)** : bibliothèque de visualisation de données interactive
- **[Pandas](https://pandas.pydata.org/)** : manipulation et analyse de données
- **Python** : langage de programmation principal

## 🗂️ Structure du projet

```
calculateur-biorythmes/
├── app.py            # Application principale Streamlit
├── requirements.txt  # Dépendances du projet
├── LICENSE           # Fichier de licence
└── README.md         # Ce fichier
```

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add some amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

## 📞 Contact

Philippe Acquier - [contact@datamanufactura.fr]

Lien du projet : [https://github.com/votre-nom/calculateur-biorythmes](https://github.com/votre-nom/calculateur-biorythmes)

---

⭐️ Si vous trouvez ce projet utile, n'hésitez pas à lui donner une étoile sur GitHub !
