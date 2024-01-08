import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import io
import requests

import warnings

# Masquer le avertissement PyplotGlobalUseWarning
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Charger le dataset des voitures depuis le lien
url = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
content = requests.get(url).content
df = pd.read_csv(io.StringIO(content.decode('utf-8')))

# Nettoyer la colonne "Continent"
df['continent'] = df['continent'].str.rstrip('.')  # Supprimer les points à la fin

# Convertir "time-to-60" en datetime (si elle est déjà au format date)
df['time-to-60'] = pd.to_datetime(df['time-to-60'], errors='coerce')

# Convertir "year" en datetime (si elle est déjà au format date)
df['year'] = pd.to_datetime(df['year'], errors='coerce')

# Remplacez "Continent" par le nom réel de la colonne représentant la région/continent dans votre base de données
regions = df["continent"].unique()
selected_region = st.selectbox("Sélectionner un continent", regions)
filtered_df = df[df["continent"] == selected_region]

# Afficher les données
st.write(f"Affichage des données pour le continent {selected_region}")
st.write(filtered_df)
st.set_option('deprecation.showPyplotGlobalUse', False)
# Analyse de corrélation et de distribution
st.subheader("Analyse de corrélation")
correlation_matrix = filtered_df.select_dtypes(include=['float64', 'int64']).corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5)
st.pyplot()

st.subheader("Distribution des variables")
for column in filtered_df.columns:
    if filtered_df[column].dtype != "object":
        st.write(f"**{column}**")
        if filtered_df[column].dtype == "float64" or filtered_df[column].dtype == "int64":
            plt.hist(filtered_df[column])
            st.pyplot()

