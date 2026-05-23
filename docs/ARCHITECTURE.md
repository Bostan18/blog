# Architecture technique proposée – Plateforme de contenu (Django + HTMX)

**Date** : 2026-04-11  
**Auteur** : Software Architect (revue de la vision "Monolithe Majestueux")  
**Version** : 1.0

---

## 1. Vue d’ensemble

**Style architectural retenu** : Monolithe Modulaire avec rendu côté serveur enrichi (HTMX)

### Justification

- **Productivité maximale** : Un seul codebase, cohérence transactionnelle forte, outillage Django complet (ORM, Admin, migrations).
- **Expérience utilisateur moderne** : HTMX apporte la réactivité d’une SPA sans la complexité d’une API REST séparée ni gestion d’état client lourde.
- **Faible complexité opérationnelle** : Déploiement d’un seul artefact, moins de surface d’attaque, monitoring simplifié.

### Alternatives écartées

| Alternative | Raison du rejet |
| :--- | :--- |
| **Architecture découplée** (React + DRF) | Complexité excessive pour un MVP solo ; gestion de deux bases de code, authentification multi-domaines, duplication de logique métier. |
| **Microservices** | Anti-pattern à cette échelle (over-engineering massif). |

---

## 2. Composants principaux & flux de données

```text
┌─────────────────────────────────────────────────────────────────┐
│ Navigateur Client                                               │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐     │
│ │  HTML/CSS   │ │    HTMX     │ │ Alpine.js / Hyperscript │     │
│ │ (Tailwind)  │ │   (AJAX)    │ │   (Interactions UI)     │     │
│ └──────┬──────┘ └──────┬──────┘ └───────────┬─────────────┘     │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Serveur d'Application (Gunicorn)                                │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ Application Django                                        │   │
│ │ ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────────┐│   │
│ │ │  URLs   │─▶│  Views  │─▶│ Models  │─▶│  Templates   ││   │
│ │ │(Router) │   │(Logique │   │  (ORM)  │   │ (Django +    ││   │
│ │ │         │   │ métier) │   │         │   │ HTMX partials)│   │
│ │ └─────────┘   └─────────┘   └────┬────┘   └──────────────┘│   │
│ │                                  │                        │   │
│ │ Apps modulaires :                │                        │   │
│ │ - core / users / blog /          │                        │   │
│ │   comments / search              │                        │   │
│ └─────────────────────────────────┼──────────────────────────┘   │
│                                   │                              │
│ ┌──────────────────────────┼──────────────────────────┐         │
│ │                          │                          │         │
│ ▼                          ▼                          ▼         │
│ ┌─────────────┐     ┌─────────────┐            ┌─────────┐      │
│ │ PostgreSQL  │     │    Redis    │            │ Celery  │      │
│ │  (Données   │     │  (Cache +   │            │ Worker  │      │
│ │ primaires)  │     │  Sessions)  │            │ (Async) │      │
│ └─────────────┘     └─────────────┘            └────┬────┘      │
│                                                     │           │
└────────────────────────────────────────────────────┼────────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────────┐
                                            │  Services Externes  │
                                            │ - Email (SMTP)      │
                                            │ - Stockage S3       │
                                            │ - Sentry            │
                                            └─────────────────────┘
```

### Interactions clés

1.  **Navigation classique** : Le navigateur demande une page → Django génère le HTML complet → réponse HTTP.
2.  **Interactions dynamiques (HTMX)** : Un clic sur "Charger plus" envoie une requête AJAX → Django renvoie un *partial* HTML → HTMX remplace le contenu cible dans le DOM.
3.  **Tâches asynchrones** : L'upload d'une image déclenche une tâche Celery (redimensionnement) → le worker traite en arrière-plan → mise à jour du statut via Redis ou base de données.

---

## 3. Stack technique détaillée

| Composant | Technologie | Justification |
| :--- | :--- | :--- |
| **Langage / Framework** | Python 3.12 + Django 5.x | Maturité, écosystème riche, parfait pour le développement rapide. |
| **Frontend Interactif** | HTMX + Alpine.js | HTMX pour l'AJAX sans JS lourd. Alpine.js pour l'UI purement client (dropdowns). |
| **Styles** | TailwindCSS | Utilitaire, design rapide, évite le CSS "maison" difficile à maintenir. |
| **Base de données** | PostgreSQL 16 | Full-Text Search natif, support JSONB, intégrité des données. |
| **Cache & Sessions** | Redis | Cache, stockage de sessions, et broker de messages pour Celery. |
| **Tâches asynchrones** | Celery | Standard Django pour l'envoi d’emails et les traitements longs. |
| **Stockage de médias** | django-storages (S3) | Découple les assets pour la scalabilité et les backups. |
| **Serveur WSGI** | Gunicorn | Robuste, performant, configuration simple. |
| **Reverse Proxy** | Nginx | Terminaison SSL, compression, fichiers statiques. |
| **Conteneurisation** | Docker | Environnement identique (dev/prod), onboarding instantané. |

---

## 4. Diagramme d’architecture (Mermaid)

```mermaid
graph TD
    subgraph Client
        Browser[Navigateur Web]
    end

    subgraph "Serveur (VPS ou PaaS)"
        subgraph "Conteneurs Docker"
            Nginx[Nginx (Reverse Proxy)]
            Gunicorn[Gunicorn (WSGI Server)]
            DjangoApp[Django Application]
            CeleryWorker[Celery Worker]
            CeleryBeat[Celery Beat (Scheduler)]
            PostgreSQL[(PostgreSQL)]
            Redis[(Redis)]
        end
    end

    subgraph "Services Cloud"
        S3[AWS S3 / DigitalOcean Spaces]
        Email[SMTP / SendGrid]
        Sentry[Sentry (Monitoring)]
    end

    Browser --> Nginx
    Nginx --> Gunicorn
    Gunicorn --> DjangoApp
    DjangoApp --> PostgreSQL
    DjangoApp --> Redis
    DjangoApp --> CeleryWorker
    CeleryWorker --> Redis
    CeleryBeat --> Redis
    CeleryWorker --> Email
    DjangoApp --> S3
    DjangoApp --> Sentry
```

---

## 5. Risques & stratégies de mitigation

| Risque | Probabilité | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| **Goulot d'étranglement ORM** | Élevée | Performance | `django-debug-toolbar` en dev. Utiliser `select_related()` et `prefetch_related()`. |
| **Surcharge de la recherche** | Moyenne | Ralentissement | Index GIN PostgreSQL. Si > 100k articles, migration vers Typesense/Meilisearch. |
| **Blocage du worker web** | Faible | Mauvaise UX | Toutes les opérations > 200ms passent par Celery. Monitoring avec `django-celery-results`. |
| **Complexité déploiement** | Moyenne | Perte de temps | Standardisation Docker dès le J1. Fichier `docker-compose.prod.yml` distinct. |
| **Dépendance au JS (HTMX)** | Très faible | UX dégradée | Vues Django conçues pour fonctionner aussi en requête HTTP standard. |

---

## 6. Roadmap de développement validée

| Phase | Durée | Livrables clés | État |
| :--- | :--- | :--- | :--- |
| **Phase 0 – Fondations** | J1-2 | Docker Compose, `django-environ`, structure modulaire par apps. | ✅ Terminé |
| **Phase 1 – Identité** | J3-5 | Custom User Model, authentification, rôles (Admin/Rédacteur). | ✅ Terminé |
| **Phase 2 – Contenu** | Semaine 2 | Modèles Catégories, Articles (slugs auto), Tags. `django-storages`. | ✅ Terminé |
| **Phase 3 – Frontend** | Semaine 3 | Intégration TailwindCSS. Interactions HTMX (infinite scroll, filtrage). | ✅ Terminé |
| **Phase 4 – Avancée** | Semaine 4 | Recherche Full-Text. Commentaires via HTMX. Configuration Celery. | ✅ Terminé |
| **Phase 5 – Qualité** | Semaine 5 | Mise en cache Redis. Tests unitaires (pytest). Optimisation requêtes. | 🚀 En cours |
| **Phase 6 – Déploiement** | Semaine 6 | GitHub Actions, VPS (Gunicorn/Nginx), monitoring Sentry. | ⏳ À venir |
