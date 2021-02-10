Voici le repository pour la génération d'image du projet du Paris Digital Lab pour Sonergia.

Il contient :

- une cli qui permet de générer des images sythétiques
- une cli qui permet de tranferer des style d'un groupe d'image à un autre

# Setup generation d'image

LA génération d'image se fait avec l'application blender, une application open-source qui permet de faire de la modélisation 3D, pour lancer une génération il faut installer blender 2.9 et vérifier que l'application est en anglais ( changer la langue directement dans l'application si ce n'est pas le cas ).
Ensuite il faut installer quelques dépendances dans l'environement de blender avec les commandes :

```bash
/Applications/Blender.app/Contents/Resources/2.91/python/bin/python3.7m -m ensurepip

/Applications/Blender.app/Contents/Resources/2.91/python/bin/python3.7m -m pip install -U pip

/Applications/Blender.app/Contents/Resources/2.91/python/bin/python3.7m -m pip install lxml

/Applications/Blender.app/Contents/Resources/2.91/python/bin/python3.7m -m pip install opencv-python
```

Vérifiez que le chemin mène bien à votre installation blender (ces lignes de commande devraient marcher uniquement sur macOS )

# Generation d'image

Pour générer des images, utilisez la commande suivante dans le dossier src ( uniquement dans le dossier src ):

```bash
blender -b --python CLI_generate_images.py -- -a generate_train -y 300 -n 300
```

Les arguments sont les suivants :
-a :
soit "generate_train" pour générer un jeu de train, qui sera séparé à 70% pour l'entrainement et 30% pour la validation
soit "generate_test" pour générer un jeu de test

-y : le nombre d'images avec une protection à générer, à defaut en créé 200
-n : le nombre d'images sans protection à générer, à defaut en créé 200
-r : path vers le dossier ou vous voulez générer votre jeu, à defaut on créé un dossier EAF

( N'oubliez pas les -- avant les arguments, ils sont indispensables )

# Visualisation de l'annotation

Lancez avec la commande suivante

```bash
python CLI_visualise_annotation.py  -i "/path/to/images" -a "/path/to/annotation" -o "/path/to/output"
```

Les arguments sont les suivants :
-i : path vers le dossier d'images de base, à default: './EAF/VOC2021/JPEGImages'
-a : path vers le dossier d'annotations correspondant, à default: './EAF/VOC2021/Annotations'
-o : path vers le dossier ou mettre les images annotées, à default: './EAF/visualisation'

# Style

Pour ajouter des style à vos images il faut créér 3 dossiers :

- un dossier ou vous mettez vous images de bases ( par exemple les images générées)
- un dossier ou vous mettez les images qui vont servir de modèle pour le style
- un dossier ou recevoir les images stylisées

Lancez avec la commande suivante

```bash
python CLI_style.py -c "/path/to/contentimages" -s "/path/to/styleimages" -o "/path/to/output"
```

Les arguments sont les suivants :
-c : path vers le dossier d'images de base, à default: '../EAF/VOC2021/JPEGImages'
-s : path vers le dossier d'images de reférence pour le style
-o : path vers le dossier ou mettre les images stylisées

# Test du style

Vous pouvez lancer une commande pour test la CLI de style :

```bash
cd test
```

```bash
python test_style.py
```

# Test de la generation

La generation est plus difficile à tester car elle tourne sur l'environement blender

Pour tester, lancer la commande suivante dans le dossier src:

```bash
blender -b --python CLI_generate_images.py -- -a generate_train -y 1 -n 1
```

Un dossier EAF devraient apparaitre à la racine avec un dossier VOC2021 pret à servir de jeu d'entrainement

Vous pouvez visualiser les annotations avec la commande :

```bash
python CLI_visualise_annotation.py
```
