# Ansible Linux Workstation

Projet Ansible pour préparer une station de travail Linux, avec une attention particulière aux environnements **Red Hat Enterprise Linux 9 et Satellite déconnectés d’Internet**. Il regroupe un rôle principal pour la station et quelques rôles d'infrastructure conservés à titre expérimental.

> Projet en cours d'amélioration. Tester d'abord dans un laboratoire ou sur une machine de test : certaines tâches modifient les dépôts, les paquets, les services ou la configuration du système.

## Fonctionnalités

Le rôle `role_fpga_workstation` permet notamment de :

- vérifier et activer les dépôts Satellite disponibles via `subscription-manager` ;
- installer des paquets depuis les dépôts disponibles et afficher le suivi par paquet ;
- installer facultativement GNOME, xrdp et configurer le pare-feu ;
- configurer, si on l'active, un fond d'écran GNOME verrouillé et un logo de bureau avec dconf.

L'hôte doit avoir accès à Satellite ou à une Capsule, et les RPM **ainsi que leurs dépendances** doivent être présents dans la Content View et l'environnement utilisés. Le projet ne fournit ni dépôts ni logiciels tiers.

Trois autres rôles issus du projet initial sont inclus pour étude : `role_ntp` (chrony), `role_change_patch_management_timer` (dnf-automatic) et `role_kernel` (configuration dracut relative à l'image de secours). Ils ne sont pas inclus dans le playbook d'exemple et doivent être revus et testés avant utilisation.

## Organisation

```text
ansible.cfg
inventories/example.yml
playbooks/workstation.yml
roles/
  role_fpga_workstation/
  role_ntp/
  role_change_patch_management_timer/
  role_kernel/
docs/
```

La version publique est une sélection anonymisée du projet : elle ne contient pas les inventaires réels, les variables d'environnement de l'infrastructure initiale ni les fichiers binaires fournis par des tiers. D'autres rôles du projet initial ne sont pas inclus dans cette première version, dans l'attente d'une revue et d'une généralisation complémentaires.

## Prérequis

- Un contrôleur Ansible compatible avec les modules utilisés. La vérification locale de cette sélection a été effectuée avec `ansible-core` 2.16 ; la compatibilité avec les autres versions reste à vérifier.
- Un accès SSH et les privilèges nécessaires sur une machine de test RHEL 9.
- Pour les dépôts gérés par Satellite : une machine déjà enregistrée auprès de Satellite ou d'une Capsule, des dépôts disponibles pour cet hôte et des RPM réellement présents côté serveur.
- Pour l'installation des paquets : les dépendances nécessaires dans les dépôts utilisés. Les noms et versions possibles dépendent de la version de RHEL et de la Content View.

## Démarrage sur une machine de test

L'inventaire `inventories/example.yml` contient un nom d'hôte fictif et une liste volontairement courte de paquets. Il désactive GNOME, xrdp, le pare-feu et la personnalisation du bureau. **Ne pas utiliser cet inventaire tel quel en production.**

1. Copier cet exemple vers un inventaire local, puis adapter l'hôte, l'utilisateur et les ID de dépôts à votre environnement. Les inventaires locaux sont ignorés par Git.

   ```bash
   cp inventories/example.yml inventories/local.yml
   ```

2. Vérifier la syntaxe du playbook :

   ```bash
   ansible-playbook -i inventories/local.yml playbooks/workstation.yml --syntax-check
   ```

3. Sur une machine de test, lancer uniquement le diagnostic DNF :

   ```bash
   ansible-playbook -i inventories/local.yml playbooks/workstation.yml \
     --limit workstation-example --tags diagnostic
   ```

   Le diagnostic ne lance pas d'installation de paquets, mais peut télécharger et rafraîchir les métadonnées. Il utilise temporairement les dépôts indiqués dans `fpga_repos`.

4. Pour activer les dépôts déclarés avec `subscription-manager`, avant toute installation :

   ```bash
   ansible-playbook -i inventories/local.yml playbooks/workstation.yml \
     --limit workstation-example --tags repositories
   ```

   Cette commande modifie durablement l'état des dépôts sur la cible. Avec `--check`, elle affiche ceux qui seraient activés sans les activer.

5. Après vérification des dépôts et de la liste des paquets, lancer les tâches de paquets :

   ```bash
   ansible-playbook -i inventories/local.yml playbooks/workstation.yml \
     --limit workstation-example --tags packages
   ```

Les ID de dépôts diffèrent d'un environnement à l'autre. `fpga_repos` doit contenir les ID réels proposés à la machine, y compris les dépôts complémentaires nécessaires. Par défaut, DNF peut également utiliser les autres dépôts déjà activés ; `fpga_exclusive_repos: true` limite les transactions du rôle aux dépôts indiqués.

La liste par défaut du rôle contient de nombreux paquets, dont certains issus de dépôts tiers ou demandant des versions et architectures précises. L'exemple la remplace volontairement par une liste réduite. Les paquets sont installés individuellement par défaut pour afficher leur progression : cela prend plus de temps et les paquets déjà traités restent installés si une étape échoue. Définir `fpga_package_progress: false` revient à une transaction groupée.

## Options GNOME et bureau

L'activation de `fpga_install_gnome`, `fpga_install_xrdp` ou `fpga_configure_firewall` change les logiciels, les services et éventuellement l'accès réseau. `fpga_set_graphical_target` modifie la cible systemd du prochain démarrage. Vérifier les variables avant de lancer le rôle complet.

Pour personnaliser le bureau, placer ses propres fichiers `wallpaper.png` et `logo.png` dans `roles/role_fpga_workstation/files/`, puis activer `fpga_personnaliser_bureau`. Les images ne sont pas fournies. Le logo s'affiche si l'extension GNOME **Background Logo** est active dans la session. Consulter [la documentation du bureau](docs/personnalisation-bureau.md) avant activation.

## Données sensibles et partage

Ne pas committer d'inventaire réel, mot de passe, jeton, clé privée, base de mots de passe, image interne ou fichier contenant des noms, adresses ou chemins propres à une infrastructure. Ansible Vault peut aider à protéger les secrets, mais les fichiers chiffrés ne doivent pas être publiés par défaut. Le fichier `.gitignore` ne protège pas les données déjà suivies par Git et ne remplace pas une revue avant publication.

Un [guide de publication sur GitHub](docs/publication-github.md) décrit les étapes de revue et de création d’un nouveau dépôt.

Aucun historique Git du projet d'origine n'était présent dans les fichiers utilisés pour préparer cette sélection. Cette version doit être importée dans un nouveau dépôt sans réutiliser d'historique non audité.

## Assistance par intelligence artificielle

Ce projet a été élaboré et amélioré avec l'assistance de **GPT-6.1 Terra**, notamment pour la revue et le débogage de rôles Ansible, certaines modifications du rôle workstation, la personnalisation GNOME, l'anonymisation et la documentation. Le code initial n'est pas présenté comme entièrement généré par une IA. La revue, la validation et les décisions de publication relèvent du mainteneur humain.

## État et licence

Le rôle workstation a fait l'objet de vérifications de syntaxe et de tests locaux simulés ; il n'a pas été validé ici de bout en bout sur une installation RHEL/Satellite réelle. Les autres rôles inclus restent à tester. Certaines fonctionnalités dépendent de logiciels et services tiers.

Aucune licence de redistribution n'a encore été choisie pour ce dépôt. Le titulaire des droits doit vérifier les conditions applicables aux différentes contributions et aux éventuels composants tiers avant d'en ajouter une ou de publier le code.
