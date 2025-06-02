# 🧪 bacparser

`bacparser` est un script Python permettant de **scraper les résultats du baccalauréat** sur le site [l'Internaute](https://www.linternaute.com/) à partir d’un **nom**, d’une **académie** et d’une **année d’examen**.

Il utilise **Selenium** et **ChromeDriver** pour automatiser la navigation, remplir le formulaire de recherche, et extraire les résultats sous forme de fichier CSV.

---

## ✨ Fonctionnalités

- Scraping automatique des résultats depuis `resultat-bac.linternaute.com`
- Gestion des cookies (pour contourner la bannière RGPD)
- Export des résultats dans un fichier `.csv`
- Affichage en console du nombre de candidats trouvés

---

## 🧰 Prérequis

- Python 3.7 ou supérieur
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) **correspondant à ta version de Chrome**
- Un fichier `cookies.json` exporté depuis le site avec les bons cookies

---

## 📦 Installation

1. **Clone le dépôt ou télécharge le script** :

```bash
git clone https://github.com/ton-utilisateur/bacparser.git
cd bacparser
```

2. **Installe les dépendances** :

```bash
pip install selenium
```

3. **Télécharge ChromeDriver** :

- Va sur : [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
- Télécharge la version **correspondante à ta version de Chrome**
- Place `chromedriver.exe` dans le même dossier que le script, ou ajuste le chemin dans la variable `CHROMEDRIVER_PATH`.

4. **Export des cookies** :

- Va sur [https://resultat-bac.linternaute.com/](https://resultat-bac.linternaute.com/) dans Google Chrome.
- Connecte-toi et accepte les cookies si besoin.
- Utilise une extension comme [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/hnmpcagpplmpfojmgmnngilcnanddlhb) pour exporter les cookies en JSON.
- Renomme le fichier en `cookies.json` et place-le dans le même dossier que le script.

---

## 🚀 Utilisation

Lance le script depuis le terminal :

```bash
python bacparser.py
```

Tu devras ensuite saisir :

- Le **nom ou prénom** à rechercher (partiel ou complet)
- L’**académie** (ex : `academie-lyon`, `academie-nancy-metz`)
- L’**année** de passage du bac (ex : `2023`)

---

## 📁 Résultat

Le script génère un fichier CSV avec les colonnes suivantes :

- Nom complet
- Type de bac
- Ville
- Lien vers la fiche de l'élève

Le fichier est nommé automatiquement selon ce format :  
`<nom_recherche>_<academie>_<annee>.csv`

Exemple : `dupont_lyon_2023.csv`


---

## ❗ Avertissement

Ce script est à usage **personnel** et **éducatif**.  
Ne l’utilise pas pour collecter ou diffuser des données sensibles sans autorisation.  
Respecte les [conditions d'utilisation](https://www.linternaute.com/info/mentions-legales/) du site L’Internaute.



