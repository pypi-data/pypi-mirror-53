# TODO

## Version 1.0

- [x] IO: ne pas enregistrer les lignes à None ; permettre la lecture de fichiers dont il manque des champs
- [x] Dissocier les valeurs par défaut quand on crée une nouvelle ligne des valeurs par défaut quand on clic sur une cellule à None
- [x] Trier selon la date par défaut
- [x] Del = supprimer la valeur d'une/plusieurs cellule(s) selectionnée(s) (remettre valeur à None) et selection cell + Ctrl+Del ou selection ligne = supprimer la ligne ; ATTENTION à la séléction multiple !
- [x] Selection mode : row -> (single) cell
- [ ] Plots
    - [ ] Barplots (réutiliser se qui a déjà été écrit dans le notebook "timemg.ipynb") : bet time, wake up, sleep duration, work in, work out, work duration
    - [ ] Utiliser un code couleur suivant les écarts à la norme
    - [ ] Matérialiser les débuts de semaine par une barre verticale
- [ ] Vérifier que modifier les données d'une cellule se fait bien via un appel direct à "model.set_data()" ; en profiter pour réviser le "flux" normal de lecture/écriture en MVC dans Qt5 (faire un diagramme)
- [ ] Ajouter les champs
     - [ ] "Mood" (attention : c'est une variable de type categorie -> combobox)
     - [ ] "Productivity"
     - [ ] "Transportation" (car / rer / bike)
- [ ] Collorer le fond des cellules (pastelle) en fonction de l'écart à la normale: vert, jaune, rouge
- [ ] Anticiper la v2: ajouter un onglet avec un chrono (juste un chrono avec boutons start, stop et reset)
- [ ] Nettoyer:
     - [ ] Renommer modules
     - [ ] Supprimer splitter
     - [ ] Ajouter tests unitaires
     - [ ] Ajouter documentation sphinx
     - [ ] Ajouter CI (.gitlab-ci.yml) + gitlab pages
     - [ ] Rendre data plus "pythonic" et plus simple en utilisant un DataFrame (???)
     - [x] Supprimer splitter et widgets inutiles
- [ ] Corriger l'apparance Qt5 dans XFCE:
     - gtk2-engines-qtcurve/cosmic 1.9-2 amd64
     - kde-style-qtcurve-qt5/cosmic 1.9-2 amd64
     - libqtcurve-utils2/cosmic 1.9-2 amd64
     - qt5ct/cosmic 0.35-1build1 amd64
     - qtcurve/cosmic 1.9-2 amd64
     - qtcurve-l10n/cosmic,cosmic 1.9-2 all

