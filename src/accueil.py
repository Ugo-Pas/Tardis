##
## EPITECH PROJECT, 2026
## acceuil 
## File description:
## acceuil
##

import pandas as pd # panda for open a csv and extract the data for file and data manipulation
import matplotlib.pyplot as pl # matplotlib to create visualisation via graphs
import pydeck as pdk
import streamlit as st
import numpy as np
import re


def render(df, contributors=None):
    st.markdown("<h1 style='text-align: center;'>Tardis</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div style='display: flex; justify-content: center;'>"
        "<img src='https://github.com/user-attachments/assets/3526ee07-10e7-4bf7-a369-e051d2771329' style='max-width: 100%; height: auto;' />"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<h3 style='text-align: center;'>\"Sorry, i'm late\"</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        ## Comment utiliser le site

        1. Ouvre le menu de gauche pour naviguer entre les pages.
        2. Choisis **Home** pour revenir à l'accueil.
        3. Va dans **Info generale** pour consulter les statistiques globales.
        4. Va dans **Info utilisateur** pour comparer les gares de départ et d'arrivée.
        5. Sélectionne une ou plusieurs années pour filtrer les données affichées.

        ### Conseils

        - Utilise les filtres pour affiner l'analyse.
        - Les graphiques se mettent à jour automatiquement selon tes choix.
        - Si une gare n'apparaît pas, vérifie d'abord la sélection des années.

        ### Contributeurs
        - [Ugo-Pas](https://github.com/Ugo-Pas)
        - [Tadomika-Ari](https://github.com/Tadomika-Ari)
        - [Pekkatrol](https://github.com/Pekkatrol)

        ### Merci à vous, bonne utilisation
        """
    )
    st.image("/home/ugo/delivery/AIA/Tardis/src/Bonus/epitech_logo_bleu.png")