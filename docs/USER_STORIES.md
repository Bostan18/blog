# 👤 User Stories & Charte de Gouvernance

Ce document définit les parcours de progression des utilisateurs sur la plateforme **Le Quotidien** et les responsabilités associées à chaque rôle.

---

## 🗺️ Parcours de Progression (User Stories)

### 1. Le Lecteur Engagé (`VISITOR` ➔ `CONTRIBUTOR`)
> **En tant que** lecteur régulier,  
> **Je veux** me créer un compte,  
> **Afin de** participer aux débats via les commentaires et personnaliser mon expérience.

*   **Action :** Inscription via email ou OAuth.
*   **Résultat :** Attribution automatique du rôle `CONTRIBUTOR`.
*   **Droits :** Poster des commentaires (soumis à modération), gérer ses préférences de profil.

### 2. L'Aspirant Rédacteur (`CONTRIBUTOR` ➔ `WRITER`)
> **En tant que** contributeur passionné,  
> **Je veux** soumettre ma candidature à la rédaction,  
> **Afin de** pouvoir publier mes propres articles et analyses.

*   **Action :** Utilisation de l'onglet **"Postuler"** sur le Dashboard. Rédaction d'une lettre de motivation.
*   **Condition :** La section doit être activée dans le profil utilisateur.
*   **Validation :** Examen et approbation par un `EDITOR`.
*   **Droits :** Accès à l'éditeur Markdown, gestion de sa médiathèque personnelle.

### 3. Le Spécialiste (`WRITER` ➔ `CHRONIQUEUR`)
> **En tant que** rédacteur expert dans un domaine,  
> **Je veux** que mes articles soient mis en avant comme des opinions d'experts,  
> **Afin de** fidéliser un lectorat autour de ma "plume".

*   **Statut :** Statut éditorial (basé sur la rubrique "Chronique").
*   **Mise en avant :** Présence sur la page "La Rédaction" et section dédiée en Home.

### 4. Le Responsable de Rubrique (`WRITER` ➔ `EDITOR`)
> **En tant que** rédacteur expérimenté,  
> **Je veux** superviser une ou plusieurs rubriques,  
> **Afin de** garantir la ligne éditoriale et la qualité des contenus publiés par mes pairs.

*   **Action :** Demande de promotion ou nomination directe.
*   **Droits :** Modération globale des commentaires, gestion des abonnés newsletter, pilotage des rubriques, accès aux Analytics globaux.

---

## 📜 Charte de Gouvernance des Rôles

| Rôle | Accès Dashboard | Pouvoirs Clés | Gouvernance |
| :--- | :---: | :--- | :--- |
| **Visiteur** | ❌ | Lecture seule, abonnement newsletter. | - |
| **Contributeur**| ✅ (Profil) | Commentaires, personnalisation profil. | Auto-attribution à l'inscription. |
| **Rédacteur** | ✅ (Complet) | Rédaction Markdown, Médiathèque. | Sur candidature ou invitation. |
| **Éditeur** | ✅ (Admin) | Modération, Analytics, Rubriques, Newsletter. | Cooptation par les administrateurs. |
| **Admin** | ✅ (Total) | Gestion technique, rôles, configuration système. | Propriétaire du projet. |

---

## ⚙️ Paramètres de Carrière
La plateforme respecte la liberté des utilisateurs. Un membre de l'équipe peut à tout moment choisir de :
*   **Activer le recrutement :** Pour voir les opportunités de promotion.
*   **Désactiver le recrutement :** Pour simplifier son interface et se concentrer uniquement sur son rôle actuel.

---

## 📝 Notes pour le Développement
*   Toute modification de rôle doit être tracée (Audit Trail - V2).
*   L'approbation d'une demande de promotion doit déclencher une notification à l'utilisateur (V2).


Ce fichier servira de base solide pour la documentation officielle et la charte du site. Il récapitule :
   1. Les parcours de progression : du simple lecteur au rédacteur ou à l'éditeur.
   2. La charte de gouvernance : un tableau clair des droits et responsabilités par rôle.
   3. La philosophie du projet : notamment la liberté pour l'utilisateur d'activer ou non sa visibilité pour le recrutement.