# 📰 Le Quotidien — Plateforme d'Information Moderne

**Le Quotidien** est une application web de blog et de gestion de contenu (CMS) robuste, conçue avec Django, HTMX et Alpine.js. Elle est pensée pour offrir une expérience fluide tant pour les lecteurs que pour l'équipe rédactionnelle.

---

## 🚀 Fonctionnalités Clés

### 📖 Pour les Lecteurs
*   **Interface Moderne** : Design épuré avec Tailwind CSS, incluant un **Mode Sombre** (Dark Mode).
*   **Lecture Fluide** : Navigation rapide sans rechargement de page grâce à **HTMX**.
*   **Système de Favoris** : Sauvegardez vos articles préférés pour une lecture ultérieure.
*   **Notifications Temps Réel** : Une cloche interactive vous alerte des nouveaux commentaires et événements importants.
*   **Recherche Instantanée** : Barre de recherche prédictive ("Search-as-you-type").

### ✍️ Pour les Créateurs (Dashboard)
*   **Éditeur Markdown** : Rédaction simplifiée avec prévisualisation en temps réel.
*   **Gestion des Rôles** : Système de recrutement intégré pour passer de Visiteur à Rédacteur.
*   **Modération Intelligente** : Approbation automatique pour les auteurs de confiance et file d'attente pour les nouveaux contributeurs.
*   **Audit Trail** : Historique complet des versions des articles (Versioning) et journal d'activité.
*   **Analytiques** : Dashboard avec statistiques de vues et performances des articles.

### 🔍 SEO & Technique
*   **Optimisation Moteurs** : Sitemaps, robots.txt et meta-tags OpenGraph/Twitter dynamiques.
*   **Performance** : Mise en cache avec Redis et tâches asynchrones (emails) avec Celery.
*   **Architecture Propre** : Code modulaire structuré en `apps/`.

---

## 🛠️ Stack Technique

*   **Backend** : Python 3.12+, Django 5.0.14
*   **Frontend** : Tailwind CSS (CDN), HTMX 1.9.10, Alpine.js 3.x
*   **Base de données** : SQLite (Dev) / Prêt pour PostgreSQL
*   **Asynchrone** : Redis & Celery
*   **Outils** : Django Simple History, Django Allauth, Django Environ

---

## 📦 Installation (Local)

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Bostan18/blog.git
   cd blog
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement** :
   Créez un fichier `.env` à la racine :
   ```env
   DEBUG=True
   SECRET_KEY=votre-cle-secrete
   DATABASE_URL=sqlite:///db.sqlite3
   REDIS_URL=redis://localhost:6379/1
   ```

5. **Appliquer les migrations** :
   ```bash
   python manage.py migrate
   ```

6. **Lancer le serveur** :
   ```bash
   python manage.py runserver
   ```

---

## 📜 Licence

Ce projet est sous licence MIT.
