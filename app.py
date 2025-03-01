import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math
import locale
import uuid

# Tentative de configuration de la locale française
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR')
    except:
        pass  # Si la locale n'est pas disponible, on continue avec la locale par défaut

# Dictionnaire pour traduire les noms des mois en français
mois_francais = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

# Définition des couleurs
colors = {
    'Physique': '#FF5A5A',
    'Émotionnel': '#FFCF56',
    'Intellectuel': '#5271FF'
}

# Configuration de la page
st.set_page_config(
    page_title="Calculateur de Biorythmes",
    page_icon="🔄",
    layout="wide"
)

# Initialisation des variables de session
if 'activities' not in st.session_state:
    st.session_state.activities = []

# Titre de l'application
st.title("🔄 Calculateur de Biorythmes")
st.markdown("### Visualisez vos cycles biologiques naturels")

# Informations sur les biorythmes
with st.expander("Qu'est-ce que les biorythmes?"):
    st.markdown("""
    Les biorythmes sont une théorie qui suggère que notre vie est influencée par trois cycles biologiques qui commencent dès notre naissance :
    
    * **Cycle Physique (23 jours)** : Concerne votre énergie, force, endurance, résistance et coordination physique.
    * **Cycle Émotionnel (28 jours)** : Influence votre humeur, sensibilité, créativité et état émotionnel.
    * **Cycle Intellectuel (33 jours)** : Affecte votre mémoire, concentration, réactivité mentale et raisonnement.
    
    Chaque cycle oscille de manière sinusoïdale entre des valeurs positives (favorables) et négatives (défavorables).
    """)

# Fonction pour calculer les biorythmes
def calculate_biorhythm(birthdate, target_date):
    # Nombre de jours écoulés depuis la naissance
    days_passed = (target_date - birthdate).days
    
    # Calcul des biorythmes
    physical = math.sin(2 * math.pi * (days_passed / 23))
    emotional = math.sin(2 * math.pi * (days_passed / 28))
    intellectual = math.sin(2 * math.pi * (days_passed / 33))
    
    return physical, emotional, intellectual

# Interface utilisateur
col1, col2 = st.columns([1, 3])

with col1:
    # Saisie de la date de naissance avec format français
    st.subheader("Entrez votre date de naissance")
    birth_date = st.date_input("Date de naissance", 
                             value=datetime.now() - timedelta(days=365*30),  # ~30 ans par défaut
                             max_value=datetime.now(),
                             format="DD/MM/YYYY")  # Format français
    
    # Date actuelle
    today = datetime.now().date()
    
    # Calcul des biorythmes pour la date actuelle
    physical_today, emotional_today, intellectual_today = calculate_biorhythm(birth_date, today)
    
    # Affichage des valeurs actuelles
    st.subheader("Vos biorythmes aujourd'hui")
    
    # Fonction pour formater la valeur et déterminer l'état
    def format_value(value):
        # Arrondir à 2 décimales
        rounded_value = round(value, 2)
        if rounded_value > 0:
            return f"+{rounded_value} (Phase positive)"
        elif rounded_value < 0:
            return f"{rounded_value} (Phase négative)"
        else:
            return f"{rounded_value} (Jour critique)"
    
    # Barres de progression colorées pour chaque cycle
    st.markdown("**Physique**")
    st.progress(float(physical_today/2 + 0.5))  # Normaliser entre 0 et 1
    st.markdown(f"<span style='color:#FF5A5A'>{format_value(physical_today)}</span>", unsafe_allow_html=True)
    
    st.markdown("**Émotionnel**")
    st.progress(float(emotional_today/2 + 0.5))
    st.markdown(f"<span style='color:#FFCF56'>{format_value(emotional_today)}</span>", unsafe_allow_html=True)
    
    st.markdown("**Intellectuel**")
    st.progress(float(intellectual_today/2 + 0.5))
    st.markdown(f"<span style='color:#5271FF'>{format_value(intellectual_today)}</span>", unsafe_allow_html=True)

# Création des données pour le graphique
# Génération de données pour le mois en cours
current_month = today.month
current_year = today.year

# Nom du mois en français
mois_courant = mois_francais[current_month]

# Déterminer le premier et dernier jour du mois
if current_month == 12:
    next_month = 1
    next_month_year = current_year + 1
else:
    next_month = current_month + 1
    next_month_year = current_year

start_date = datetime(current_year, current_month, 1).date()
end_date = datetime(next_month_year, next_month, 1).date() - timedelta(days=1)

# Création d'une liste de dates pour le mois actuel
date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# Calcul des biorythmes pour chaque jour
biorhythm_data = []

for date in date_range:
    physical, emotional, intellectual = calculate_biorhythm(birth_date, date)
    biorhythm_data.append({
        'Date': date,
        'Physique': physical,
        'Émotionnel': emotional,
        'Intellectuel': intellectual,
        'Jour': date.day
    })

# Création du DataFrame
df = pd.DataFrame(biorhythm_data)

with col2:
    # Affichage du mois en cours en français
    st.markdown(f"## {mois_courant} {current_year}")
    
    # Création du graphique avec Plotly
    fig = go.Figure()
    
    # Ajouter les courbes
    fig.add_trace(go.Scatter(
        x=df['Jour'], 
        y=df['Physique'], 
        mode='lines+markers',
        name='Physique',
        line=dict(color='#FF5A5A', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Jour'], 
        y=df['Émotionnel'], 
        mode='lines+markers',
        name='Émotionnel',
        line=dict(color='#FFCF56', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Jour'], 
        y=df['Intellectuel'], 
        mode='lines+markers',
        name='Intellectuel',
        line=dict(color='#5271FF', width=3),
        marker=dict(size=8)
    ))
    
    # Ligne horizontale pour la valeur zéro
    fig.add_shape(
        type="line",
        x0=1,
        y0=0,
        x1=len(df['Jour']),
        y1=0,
        line=dict(
            color="gray",
            width=1,
            dash="dash",
        )
    )
    
    # Ligne verticale pour aujourd'hui
    fig.add_shape(
        type="line",
        x0=today.day,
        y0=-1,
        x1=today.day,
        y1=1,
        line=dict(
            color="red",
            width=2,
        )
    )
    
    # Mise en page du graphique
    fig.update_layout(
        title='Biorythmes',
        xaxis_title='Jour du mois',
        yaxis_title='Niveau du biorythme',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(
            range=[-1.1, 1.1],
            zeroline=False,
            gridwidth=1,
            gridcolor='rgba(233, 233, 233, 0.6)',
        ),
        xaxis=dict(
            tickmode='linear',
            gridwidth=1,
            gridcolor='rgba(233, 233, 233, 0.6)',
        ),
        plot_bgcolor='rgba(255, 255, 255, 1)',
        margin=dict(t=50, l=50, r=50, b=50),
        height=500,
    )
    
    # Supprimer l'axe x supérieur
    fig.update_layout(
        xaxis=dict(
            mirror=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=True,
        )
    )
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Légende des jours critiques
    st.markdown("""
    ### Interprétation
    
    - **Valeurs positives (> 0)** : Période favorable pour les activités liées à ce cycle
    - **Valeurs négatives (< 0)** : Période moins favorable, prenez des précautions
    - **Autour de zéro (≈ 0)** : Jour critique - soyez particulièrement vigilant
    
    Les jours critiques sont les moments où un cycle passe de positif à négatif (ou inversement).
    """)

# Section pour les activités planifiées
st.markdown("---")
st.subheader("📋 Planificateur d'activités")
st.markdown("Planifiez vos activités en fonction de vos biorythmes pour optimiser votre performance")

# Gestion des activités existantes
if 'activities' not in st.session_state:
    st.session_state.activities = []

# Formulaire pour ajouter une nouvelle activité
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    activity_name = st.text_input("Nom de l'activité", key="new_activity_name")
with col2:
    activity_category = st.selectbox(
        "Catégorie",
        options=["Physique", "Émotionnel", "Intellectuel"],
        key="new_activity_category"
    )
with col3:
    add_button = st.button("+ Ajouter une activité")
    
if add_button and activity_name:
    new_activity = {
        'id': str(uuid.uuid4()),
        'name': activity_name,
        'category': activity_category
    }
    st.session_state.activities.append(new_activity)
    st.success(f"Activité '{activity_name}' ajoutée avec succès!")
    st.rerun()

# Afficher les activités et leurs périodes recommandées
if st.session_state.activities:
    # Créer un conteneur pour le graphique de recommandation
    recommendation_container = st.container()
    
    with recommendation_container:
        # Pour chaque activité, créer un graphique de périodes recommandées
        for activity in st.session_state.activities:
            # Créer une figure pour cette activité
            fig_activity = go.Figure()
            
            # Obtenir les données de biorythme pour cette catégorie
            cycle_data = df[activity['category']].values
            
            # Créer une visualisation de type heatmap horizontale
            # Utiliser une seule ligne de couleur qui varie selon la valeur du biorythme
            fig_activity.add_trace(go.Heatmap(
                z=[cycle_data],
                x=df['Jour'],
                colorscale=[
                    [0, f'rgba{tuple(int(c) for c in bytes.fromhex(colors[activity['category']][1:] + "00"))}'],
                    [0.5, f'rgba{tuple(int(c) for c in bytes.fromhex(colors[activity['category']][1:] + "80"))}'],
                    [1, colors[activity['category']]]
                ],
                showscale=False,
                zmin=-1,
                zmax=1
            ))
            
            # Ajouter une ligne verticale pour le jour actuel
            fig_activity.add_shape(
                type="line",
                x0=today.day,
                y0=-0.5,
                x1=today.day,
                y1=0.5,
                line=dict(
                    color="red",
                    width=2,
                )
            )
            
            # Configuration du graphique
            fig_activity.update_layout(
                height=100,
                margin=dict(l=50, r=20, t=30, b=20),
                xaxis=dict(
                    title=None,
                    tickmode='linear',
                    tick0=1,
                    dtick=1,
                    showgrid=False
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False
                ),
                plot_bgcolor='rgba(255, 255, 255, 1)',
                title=dict(
                    text=f"{activity['name']} ({activity['category']})",
                    x=0,
                    font=dict(
                        size=14
                    )
                )
            )
            
            # Afficher le bouton de suppression à droite du titre
            col_graph, col_btn = st.columns([6, 1])
            
            with col_graph:
                # Afficher le graphique
                st.plotly_chart(fig_activity, use_container_width=True)
            
            with col_btn:
                st.write("")  # Espace pour aligner avec le titre
                st.write("")  # Espace pour aligner avec le titre
                if st.button("Supprimer", key=f"delete_{activity['id']}"):
                    st.session_state.activities.remove(activity)
                    st.rerun()
else:
    st.info("Ajoutez votre première activité en utilisant le formulaire ci-dessus.")

# Pied de page
st.markdown("---")
st.markdown("""
Copyright Philippe Acquier
""")
