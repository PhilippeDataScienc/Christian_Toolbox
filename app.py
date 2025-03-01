import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import math

# Configuration de la page
st.set_page_config(
    page_title="Calculateur de Biorythmes",
    page_icon="🔄",
    layout="wide"
)

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
    # Saisie de la date de naissance
    st.subheader("Entrez votre date de naissance")
    birth_date = st.date_input("Date de naissance", 
                               value=datetime.now() - timedelta(days=365*30),  # ~30 ans par défaut
                               max_value=datetime.now())
    
    # Date actuelle
    today = datetime.now().date()
    
    # Calcul des biorythmes pour la date actuelle
    physical_today, emotional_today, intellectual_today = calculate_biorhythm(birth_date, today)
    
    # Affichage des valeurs actuelles
    st.subheader("Vos biorythmes aujourd'hui")
    
    # Fonction pour formater le pourcentage et déterminer l'état
    def format_percentage(value):
        percentage = round(value * 100, 1)
        if percentage > 0:
            return f"+{percentage}% (Phase positive)"
        elif percentage < 0:
            return f"{percentage}% (Phase négative)"
        else:
            return f"{percentage}% (Jour critique)"
    
    # Barres de progression colorées pour chaque cycle
    st.markdown("**Physique**")
    st.progress(float(physical_today/2 + 0.5))  # Normaliser entre 0 et 1
    st.markdown(f"<span style='color:#FF5A5A'>{format_percentage(physical_today)}</span>", unsafe_allow_html=True)
    
    st.markdown("**Émotionnel**")
    st.progress(float(emotional_today/2 + 0.5))
    st.markdown(f"<span style='color:#FFCF56'>{format_percentage(emotional_today)}</span>", unsafe_allow_html=True)
    
    st.markdown("**Intellectuel**")
    st.progress(float(intellectual_today/2 + 0.5))
    st.markdown(f"<span style='color:#5271FF'>{format_percentage(intellectual_today)}</span>", unsafe_allow_html=True)

with col2:
    # Création des données pour le graphique
    # Génération de données pour le mois en cours
    current_month = today.month
    current_year = today.year
    
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
    
    # Transformation des données pour Altair
    df_melted = pd.melt(
        df, 
        id_vars=['Date', 'Jour'],
        value_vars=['Physique', 'Émotionnel', 'Intellectuel'],
        var_name='Cycle',
        value_name='Valeur'
    )
    
    # Déterminer les couleurs pour chaque cycle
    color_scale = alt.Scale(
        domain=['Physique', 'Émotionnel', 'Intellectuel'],
        range=['#FF5A5A', '#FFCF56', '#5271FF']
    )
    
    # Ligne horizontale pour la valeur zéro
    zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
        strokeDash=[3, 3],
        stroke='gray',
        opacity=0.5
    ).encode(y='y')
    
    # Ligne verticale pour aujourd'hui
    today_df = pd.DataFrame({'x': [today.day]})
    today_line = alt.Chart(today_df).mark_rule(
        stroke='gray',
        strokeWidth=2
    ).encode(x='x:Q')
    
    # Création du graphique avec Altair
    chart = alt.Chart(df_melted).mark_line(
        point=True,
        strokeWidth=3
    ).encode(
        x=alt.X('Jour:O', axis=alt.Axis(title='Jour du mois')),
        y=alt.Y('Valeur:Q', 
               scale=alt.Scale(domain=[-1, 1]),
               axis=alt.Axis(title='Niveau du biorythme', format='%')),
        color=alt.Color('Cycle:N', scale=color_scale),
        tooltip=['Date:T', 'Cycle:N', alt.Tooltip('Valeur:Q', format='.1%')]
    ).properties(
        title=f'Biorythmes pour {today.strftime("%B %Y")}',
        width=800,
        height=400
    )
    
    # Combiner les charts
    final_chart = chart + zero_line + today_line
    
    # Affichage du graphique
    st.altair_chart(final_chart, use_container_width=True)
    
    # Légende des jours critiques
    st.markdown("""
    ### Interprétation
    
    - **Valeurs positives (> 0)** : Période favorable pour les activités liées à ce cycle
    - **Valeurs négatives (< 0)** : Période moins favorable, prenez des précautions
    - **Autour de zéro (≈ 0)** : Jour critique - soyez particulièrement vigilant
    
    Les jours critiques sont les moments où un cycle passe de positif à négatif (ou inversement).
    """)

# Pied de page
st.markdown("---")
st.markdown("""
**Note** : Cette application est fournie à titre informatif uniquement. Les biorythmes sont considérés 
comme une théorie pseudoscientifique et ne doivent pas remplacer un avis médical ou psychologique professionnel.
""")
