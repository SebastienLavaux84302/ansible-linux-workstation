# Personnalisation du bureau GNOME

La fonctionnalité `06_personnalisation_bureau.yml` est désactivée par défaut. Ajouter ses propres images dans `roles/role_fpga_workstation/files/` :

- `wallpaper.png`, ou un autre nom défini par `fpga_wallpaper_fichier` ;
- `logo.png`, ou un autre nom défini par `fpga_logo_fichier`.

Activer ensuite `fpga_personnaliser_bureau: true` dans un inventaire privé et tester sur une machine dédiée avec `--tags bureau`. Ce tag inclut l'activation et le diagnostic des dépôts dans le playbook fourni. Les paquets `dconf` et `gnome-shell-extension-background-logo` doivent être disponibles dans les dépôts utilisés.

Le fond et ses paramètres sont verrouillés avec dconf. Les réglages de gestion d'énergie de l'exemple mettent l'action du bouton d'alimentation et la mise en veille automatique sur `nothing` ; désactiver cette partie avec `fpga_bureau_gestion_energie: false` si ce comportement ne convient pas. Les réglages de confirmation de déconnexion et de verrouillage des animations sont également configurables.

Le logo ne s'affiche que si l'extension Background Logo est active dans la session. La liste des extensions utilisateur n'est pas forcée. L'option `fpga_bureau_definir_extensions_par_defaut` permet de fixer une liste par défaut pour les profils concernés, mais elle remplace la valeur système de cette liste et peut ne pas s'appliquer aux utilisateurs ayant leur propre liste.

Le rôle n'écrase pas le logo fourni par le système et ne redémarre pas GDM. Après modification des profils, déconnecter et reconnecter la session. Pour vérifier le verrouillage avec l'utilisateur graphique :

```bash
gsettings get org.gnome.desktop.background picture-uri
gsettings writable org.gnome.desktop.background picture-uri
gsettings writable org.gnome.desktop.background picture-options
gnome-extensions list --enabled
```

Les commandes `writable` doivent retourner `false`. Le profil dconf effectif, les autres bases et les configurations concurrentes peuvent modifier le résultat. Les paramètres des sessions et les extensions dépendent des versions de GNOME et de RHEL : vérifier sur la machine cible.
