# Suivi du Projet : Blog Moderne (Django + HTMX)

**Dernière mise à jour** : 2026-04-11  
**État global** : 75% du MVP fonctionnel

---

## ✅ Phases Complétées

### Phase 0 – Fondations
- [x] Structure Django modulaire (`apps/`).
- [x] Variables d'environnement (`django-environ`).
- [x] Dockerfile & Docker Compose (PostgreSQL, Redis, Celery).
- [x] SQLite local opérationnel pour le prototype.

### Phase 1 – Identité
- [x] Custom User Model (`CustomUser`) avec rôles.
- [x] Super-utilisateur (`admin` / `pass123`).
- [x] Interface Admin configurée.

### Phase 2 – Contenu
- [x] Modèles `Category`, `Tag`, `Article` avec Slugs automatiques.
- [x] Enregistrement dans l'admin Django.
- [x] Données de test générées.

### Phase 3 – Frontend (Layout & Home)
- [x] Layout de base Tailwind + Alpine.js + HTMX.
- [x] Page d'accueil dynamique avec cartes d'articles.
- [x] Page de détail de l'article avec typographie soignée.

### Phase 4 – Avancée (Interactions)
- [x] **Commentaires HTMX** : Ajout et affichage temps réel sans rechargement.
- [x] **Recherche HTMX** : "Search-as-you-type" dans la navigation.
- [x] Compteur de commentaires sur les vignettes d'articles.

---

## 🚀 Prochaines Étapes (Phase 5 – Qualité & Optimisation)

- [ ] **Optimisation SQL** : `select_related` et `prefetch_related`.
- [ ] **Mise en cache** : Activation de Redis sur les vues critiques.
- [ ] **Tests Unitaires** : Couverture des modèles et vues (pytest).
- [ ] **Pagination** : Infinite Scroll avec HTMX.

---

## 🛠️ Notes Techniques
- **Python** : 3.13.12
- **Django** : 6.0.4
- **Apps** : `core`, `users`, `weblog`, `comments`, `search`
- **Frontend** : TailwindCSS (CDN), HTMX 1.9.10, Alpine.js 3.x
