# Publier la sélection sur GitHub

Cette page suppose que le contenu du dossier a été relu, que la personne qui publie a le droit de le faire et que les paramètres sont adaptés à un usage public. Aucun historique Git précédent n'est fourni avec cette sélection.

## 1. Vérifier les données

Relire le README et les rôles. Ne pas ajouter de vrais inventaires, données de connexion, images internes, fichiers chiffrés, fichiers de configuration spécifiques ou installateurs de tiers. Vérifier aussi les noms de fichiers et les commentaires : une information peut permettre d'identifier un environnement sans être un mot de passe.

La configuration `.gitignore` couvre quelques cas courants, mais ce n'est pas un outil de détection de secrets et elle n'enlève pas des fichiers déjà suivis par Git. En cas d'exposition d'un véritable secret, le révoquer ou le renouveler et traiter l'historique selon la procédure de l'hébergeur.

## 2. Préparer un nouveau dépôt

Dans un terminal, depuis ce dossier, initialiser un **nouveau** dépôt :

```bash
git init -b main
```

Configurer une identité Git adaptée à un dépôt public. Remplacer les deux valeurs ci-dessous par son propre pseudo et une adresse associée au compte GitHub, par exemple son adresse `noreply` personnelle :

```bash
git config --local user.name "VOTRE_PSEUDO"
git config --local user.email "VOTRE_ADRESSE_NOREPLY_GITHUB"
```

Préparer les fichiers de cette sélection, puis examiner exactement ce qui va être commité :

```bash
git add -- .gitignore README.md ansible.cfg docs inventories/example.yml playbooks roles
git status --short
git diff --cached --stat
git diff --cached
git diff --cached --check
```

Si une donnée ne doit pas être publiée, la retirer de la sélection et reprendre la revue avant de créer le commit. Quand tout est prêt :

```bash
git commit -m "Initial public Ansible workstation roles"
git log -1 --format='%an <%ae>'
```

Vérifier que l'identité affichée est bien celle souhaitée. Un compte GitHub public, son pseudo et ses commits sont visibles ; utiliser une adresse `noreply` n'anonymise pas le compte.

## 3. Créer et alimenter le dépôt GitHub

Dans GitHub, créer sur son compte personnel un dépôt vide nommé par exemple `ansible-linux-workstation`. Choisir sa visibilité seulement après avoir terminé la revue ; pour le publier, sélectionner **Public**. Ne pas préremplir le dépôt distant avec un README si le premier commit existe déjà localement.

Remplacer `VOTRE_COMPTE` dans les commandes suivantes par son identifiant GitHub :

```bash
git remote add origin https://github.com/VOTRE_COMPTE/ansible-linux-workstation.git
git push -u origin main
```

Utiliser le mode d'authentification GitHub habituel. Ne pas inscrire de mot de passe ou de jeton dans l'URL, le README ou l'historique de commandes. Vérifier ensuite les fichiers visibles sur GitHub et activer les protections adaptées à son compte.

## 4. Ajouter d'autres rôles

La sélection actuelle ne représente pas tous les rôles du projet initial. Pour chaque ajout : revoir son contenu et ses noms de fichiers, remplacer les paramètres réels par des variables ou exemples fictifs, vérifier les droits de redistribution de ses dépendances et installateurs, tester en environnement dédié, puis analyser de nouveau les modifications avant publication.
