# Site d'Enhydra

Site de présentation d'[Enhydra](https://github.com/nolanCrrd/Enhydra) : accueil, politique de confidentialité,
conditions d'utilisation. HTML et CSS statiques, sans framework ni suivi (aucun cookie, aucune mesure d'audience).

## Modifier

Les pages sont écrites dans `_gen.py` (texte, en français) ; le style est dans `style.css`.

```bash
python3 _gen.py        # régénère index.html, confidentialite.html, conditions.html, 404.html
```

Pour voir le résultat, ouvre `index.html` dans un navigateur, ou lance un petit serveur dans ce dossier
(`python3 -m http.server`). Les liens `/confidentialite` et `/conditions` s'ouvrent sans `.html` une fois le site
en ligne (Cloudflare Pages le fait tout seul).

## Mettre en ligne (Cloudflare Pages, gratuit)

```bash
npx wrangler pages deploy . --project-name enhydra-site --branch main
```

Puis, dans Cloudflare : Workers et Pages → `enhydra-site` → Domaines personnalisés → ton domaine, et crée chez ton
hébergeur de DNS l'entrée `CNAME` demandée (vers `enhydra-site.pages.dev`).

Les captures d'écran viennent de l'instance de démonstration d'Enhydra (`make demo`) : données fictives.
Les polices (Fraunces, Figtree) sont celles de l'application.
