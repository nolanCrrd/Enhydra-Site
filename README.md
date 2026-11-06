# Site d'Enhydra

Site de présentation d'[Enhydra](https://github.com/nolanCrrd/Enhydra) : accueil, politique de confidentialité,
conditions d'utilisation. HTML et CSS statiques, sans framework ni suivi (aucun cookie, aucune mesure d'audience).

## Modifier

Les pages sont écrites dans `_gen.py` (texte, en français) ; le style est dans `style.css`.

```bash
python3 _gen.py        # régénère public/index.html, confidentialite.html, conditions.html, 404.html
```

Pour voir le résultat, lance un petit serveur dans `public/` (`python3 -m http.server`). Les liens
`/confidentialite` et `/conditions` s'ouvrent sans `.html` une fois le site en ligne (Apache, option MultiViews).

## Mettre en ligne (Apache, sur le serveur)

Le site est servi tel quel (dossier `public/`) par Apache sur `enhydra.nolancrrd.fr`, avec un certificat Let's Encrypt.
Le DNS de `enhydra.nolancrrd.fr` doit déjà pointer vers le serveur.

```bash
sudo git clone https://github.com/nolanCrrd/Enhydra-Site.git /opt/enhydra-site   # une fois
sudo bash /opt/enhydra-site/deploy/install.sh                                      # config Apache + certificat
```

`deploy/install.sh` est relançable : il ne refait le certificat que s'il manque, teste la configuration d'Apache avant
de la recharger, et désactive le site si elle est refusée. Pour mettre à jour le contenu ensuite, `git pull` dans
`/opt/enhydra-site` suffit (rien à recharger).

Les captures d'écran viennent de l'instance de démonstration d'Enhydra (`make demo`) : données fictives.
Les polices (Fraunces, Figtree) sont celles de l'application.
