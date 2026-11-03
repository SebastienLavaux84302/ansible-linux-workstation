# Revoir une modification avant publication

Ce dépôt est un projet personnel expérimental. Avant de publier une nouvelle contribution, vérifier que son contenu est compréhensible, testable et peut être partagé.

## 1. Relire les fichiers

- Utiliser des exemples fictifs pour les inventaires, adresses, noms de domaine et identifiants.
- Ne pas ajouter de mots de passe, jetons, clés privées, certificats internes, images internes ni journaux de machines réelles.
- Relire aussi les commentaires, captures, noms de fichiers et chemins : ils peuvent révéler des informations propres à un environnement.
- Vérifier le droit de partager les contributions et les éventuelles dépendances de tiers.

La configuration `.gitignore` couvre certains fichiers locaux, mais elle ne détecte pas les secrets et ne retire pas les fichiers déjà suivis. Si un véritable secret a été exposé, le révoquer ou le renouveler et traiter également l'historique.

## 2. Vérifier la modification

Depuis la racine du dépôt, examiner les fichiers préparés :

```bash
git status --short
git diff --cached --stat
git diff --cached
git diff --cached --check
```

Exécuter les [tests décrits dans le README](../README.md#tests-locaux-du-rôle-de-dépôts), documenter les vérifications réalisées et préciser celles qui restent à effectuer sur une cible RHEL ou Satellite.

## 3. Contrôler le commit

Utiliser une identité Git adaptée à un dépôt public. GitHub propose une adresse personnelle `noreply` si l'on ne souhaite pas exposer son adresse habituelle. Après le commit :

```bash
git log -1 --format='%an <%ae>'
```

Une adresse `noreply` masque l'adresse personnelle utilisée dans le commit ; elle ne rend pas le compte anonyme. Après publication, relire les fichiers tels qu'ils apparaissent sur GitHub.
