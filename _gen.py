"""Génère les pages du site (HTML statique). `python3 _gen.py` puis déployer le dossier tel quel."""
import hashlib
from pathlib import Path

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f3eee8">
<meta name="google-site-verification" content="vz8DcHir2hpwtQemUgFwUirm2JJW7QrIQrmrnhKGtM4">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/img/logo-512.png">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="/img/favicon-64.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/img/loutre-nage.svg" as="image">
<link rel="preload" href="/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css?v={css}">
<script src="/site.js?v={js}"></script>
</head>
<body>
<div id="intro" aria-hidden="true"><div class="intro-in"><img class="swim" src="/img/loutre-nage.svg" alt="" width="340" height="126"><b>Enhydra</b></div></div>
<div id="progress" aria-hidden="true"></div>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><img src="/img/logo-192.png" alt="" width="36" height="36">Enhydra</a>
  <nav aria-label="Principal">
    <a class="opt" href="/#fonctions">Fonctions</a>
    <a class="opt" href="/#installer">Installer</a>
    <a href="https://github.com/nolanCrrd/Enhydra">GitHub</a>
  </nav>
</div></header>
<main>
"""

FOOT = """</main>
<footer><div class="wrap">
  <div>Enhydra, logiciel libre (AGPL-3.0) · fait par <a href="https://github.com/nolanCrrd">Nolan Correard</a></div>
  <nav aria-label="Informations">
    <a href="/confidentialite">Confidentialité</a>
    <a href="/conditions">Conditions d'utilisation</a>
    <a href="https://github.com/nolanCrrd/Enhydra">Code source</a>
    <a href="mailto:contact@nolancrrd.fr">Contact</a>
  </nav>
</div></footer>
</body>
</html>
"""

INDEX = """<section class="hero"><div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div><div class="wrap">
  <div>
    <h1 class="split"><span style="--i:0">Ton</span> <span style="--i:1">assistant</span> <span style="--i:2">personnel,</span> <span style="--i:3">chez</span> <span style="--i:4">toi.</span></h1>
    <p class="lead">Un chat avec une IA qui agit, une mémoire que tu possèdes, un coffre pour tes accès. Sur ton serveur, dans une appli que tu ouvres comme n'importe quelle autre.</p>
    <p class="rotor" aria-hidden="true">Il <b data-rotor="range tes notes|rappelle tes rendez-vous|garde tes mots de passe|prépare ton résumé du matin">range tes notes</b></p>
    <div class="cta">
      <a class="btn shine" href="#installer">Installer Enhydra</a>
      <a class="btn plain" href="#demo">Le voir en action</a>
    </div>
  </div>
  <div class="shots" aria-hidden="true" data-tilt>
    <img src="/img/hermes.webp" alt="" width="280" height="574">
    <img src="/img/accueil.webp" alt="" width="280" height="574">
  </div>
</div></section>

<section class="stats"><div class="wrap">
  <div class="pop"><b data-count="1">1</b><span>commande pour installer</span></div>
  <div class="pop" style="--d:.1s"><b data-count="0">0</b><span>cookie, traceur ou publicité</span></div>
  <div class="pop" style="--d:.2s"><b data-count="100" data-suffix=" %">100 %</b><span>de tes données chez toi</span></div>
</div></section>

<section id="demo"><div class="wrap demo">
  <div>
    <h2 class="reveal">Dis-le. C'est fait.</h2>
    <p class="intro reveal" style="--d:.08s">Tu écris comme à un ami. Hermes comprend, range, programme, et te répond avec une carte claire. Pas de menu à fouiller.</p>
    <div class="chips reveal" style="--d:.16s" role="tablist" aria-label="Exemples">
      <button class="chip on" data-scene="0" role="tab" aria-selected="true">Un rappel</button>
      <button class="chip" data-scene="1" role="tab" aria-selected="false">Une note</button>
      <button class="chip" data-scene="2" role="tab" aria-selected="false">Une tâche automatique</button>
    </div>
  </div>
  <div class="phone reveal pop-in" style="--d:.1s" aria-hidden="true">
    <div class="phone-bar"><img src="/img/logo-192.png" alt="" width="28" height="28"><b>Hermes</b><span class="dot"></span></div>
    <div class="chat" id="chat">
      <div class="row me on"><span class="avatar you">Toi</span><div class="msg me" id="m-me">Rappelle-moi demain à 9 h d'appeler le garage</div></div>
      <div class="row bot on"><img class="avatar" src="/img/logo-192.png" alt="" width="34" height="34"><div class="msg bot" id="m-bot">C'est noté. Je te le rappelle demain à 9 h.</div></div>
      <div class="row res on"><div class="cardmsg"><i class="ico"></i><span><b id="m-title">Appeler le garage</b><small id="m-meta">Demain · 9 h 00</small></span></div></div>
    </div>
  </div>
</div></section>

<section id="fonctions" class="alt"><div class="wrap">
  <h2 class="reveal">Ce que tu y trouves</h2>
  <p class="intro reveal" style="--d:.06s">Une seule application, sur ton téléphone et ton ordinateur, en français, avec un mode clair et un mode sombre.</p>
  <div class="grid">
    <div class="card pop"><h3>Hermes, ton assistant</h3><p>Écris-lui ou parle-lui : « Range cette note dans Recettes », « Rappelle-moi demain à 9 h d'appeler le garage ». Il ne se contente pas de répondre, il agit.</p></div>
    <div class="card pop" style="--d:.07s"><h3>Une mémoire à toi</h3><p>Tes notes en fichiers Markdown, rangées en dossiers, avec des liens entre elles. Tout marche sans réseau et repart tout seul au retour de la connexion.</p></div>
    <div class="card pop" style="--d:.14s"><h3>Un coffre verrouillé</h3><p>Tes mots de passe chiffrés, protégés par le mot de passe de ton compte. Il se referme dès que tu quittes l'appli. Hermes n'en lit un que quand tu lui demandes d'agir.</p></div>
    <div class="card pop" style="--d:.21s"><h3>Agenda et rappels</h3><p>Tâches, rendez-vous qui se répètent, rappels qui sonnent à l'heure, même appli fermée.</p></div>
    <div class="card pop" style="--d:.28s"><h3>Des tâches automatiques</h3><p>« Chaque matin à 7 h, fais-moi un résumé » : les résultats arrivent sur ton accueil, en cartes lisibles.</p></div>
    <div class="card pop" style="--d:.35s"><h3>Pour toute la famille</h3><p>Invite tes proches par un simple lien. Chacun a son compte et son propre Hermes, séparés des autres.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2 class="reveal">En images</h2>
  <p class="intro reveal" style="--d:.06s">Captures de l'instance de démonstration (données fictives).</p>
  <div class="gallery">
    <figure class="pop"><img src="/img/accueil.webp" alt="L'accueil d'Enhydra : tâches du jour et bouton pour parler à Hermes" width="280" height="574" loading="lazy"><figcaption><b>L'accueil</b>Ta journée en un coup d'œil</figcaption></figure>
    <figure class="pop" style="--d:.1s"><img src="/img/hermes.webp" alt="Une conversation avec Hermes" width="280" height="574" loading="lazy"><figcaption><b>Hermes</b>Il répond, et il agit</figcaption></figure>
    <figure class="pop" style="--d:.2s"><img src="/img/memoire.webp" alt="La Mémoire : notes et dossiers" width="280" height="574" loading="lazy"><figcaption><b>La Mémoire</b>Tes notes, rangées</figcaption></figure>
    <figure class="pop" style="--d:.3s"><img src="/img/coffre.webp" alt="Le Coffre verrouillé, qui demande le mot de passe du compte" width="280" height="574" loading="lazy"><figcaption><b>Le Coffre</b>Verrouillé par ton mot de passe</figcaption></figure>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="reveal">Ce qui le distingue</h2>
  <p class="intro reveal" style="--d:.06s">Les assistants IA vivent chez quelqu'un d'autre. Enhydra fait l'inverse.</p>
  <ul class="checks">
    <li class="slide"><b>Tes données restent chez toi.</b> Notes en fichiers, base SQLite, coffre chiffré : tu peux tout lire, sauvegarder et emporter.</li>
    <li class="slide" style="--d:.1s"><b>Un Hermes isolé par personne.</b> Mémoire, tâches et terminal séparés : personne ne voit les données des autres, pas même l'administrateur.</li>
    <li class="slide" style="--d:.2s"><b>Une commande pour installer</b>, une pour mettre à jour.</li>
    <li class="slide" style="--d:.3s"><b>Open source (AGPL-3.0).</b> Tu peux lire le code, le modifier et l'héberger.</li>
  </ul>
</div></section>

<section id="installer"><div class="wrap narrow">
  <h2 class="reveal">Installer chez toi</h2>
  <p class="intro reveal" style="--d:.06s">Il te faut un serveur Linux avec 4 Go de mémoire (un petit VPS suffit) et, pour l'application Android, un nom de domaine.</p>
  <div class="codebox reveal" style="--d:.1s"><pre><code>curl -fsSL https://raw.githubusercontent.com/nolanCrrd/Enhydra/main/install.sh | sudo bash</code></pre><button class="copy" type="button" data-copy="curl -fsSL https://raw.githubusercontent.com/nolanCrrd/Enhydra/main/install.sh | sudo bash">Copier</button></div>
  <p class="reveal" style="--d:.14s">L'installateur s'occupe de tout : Docker si besoin, secrets, HTTPS automatique, choix de ton fournisseur d'IA et de ton modèle, puis ton compte administrateur. Tu peux le relancer sans rien casser.</p>
  <p class="reveal" style="--d:.18s">Mise à jour en une commande :</p>
  <div class="codebox reveal" style="--d:.2s"><pre><code>sudo /opt/enhydra/update.sh</code></pre><button class="copy" type="button" data-copy="sudo /opt/enhydra/update.sh">Copier</button></div>
  <p class="reveal" style="--d:.24s">Guide complet, application Android, sauvegardes : <a href="https://github.com/nolanCrrd/Enhydra">le dépôt sur GitHub</a>.</p>
</div></section>
"""

CONF = """<div class="wrap narrow doc">
<h1>Politique de confidentialité</h1>
<p class="date">Dernière mise à jour : 6 novembre 2026</p>

<p class="notice">En bref : Enhydra est un logiciel que chacun installe sur son propre serveur. Son éditeur n'a accès à aucune donnée des instances. Ce site ne dépose aucun cookie et ne mesure aucune audience.</p>

<h2>1. Qui est concerné</h2>
<p>Enhydra est un logiciel libre édité par Nolan Correard. Il existe en deux sens : ce site de présentation, et les <b>instances</b> d'Enhydra, installées et gérées par des particuliers sur leur propre serveur. La personne qui héberge une instance est responsable des données qui s'y trouvent (c'est à elle qu'il faut s'adresser pour exercer ses droits sur son compte).</p>

<h2>2. Ce site</h2>
<ul>
<li>Aucun cookie, aucun traceur, aucun outil de mesure d'audience, aucun formulaire.</li>
<li>Le site est hébergé par Cloudflare, qui conserve des journaux techniques (adresse IP, date) pour la sécurité et le fonctionnement du service.</li>
</ul>

<h2>3. Ce que contient une instance Enhydra</h2>
<p>Selon l'usage de chaque personne : identifiant, nom affiché et mot de passe (conservé sous forme hachée, jamais en clair) ; conversations avec l'assistant Hermes et pièces jointes ; notes ; tâches et rendez-vous ; mots de passe rangés dans le Coffre (chiffrés) ; réglages et abonnements aux notifications. Tout est stocké sur le serveur de l'hébergeur, pas chez l'éditeur du logiciel.</p>

<h2>4. Services tiers</h2>
<ul>
<li><b>Fournisseur d'intelligence artificielle</b> : pour répondre, Hermes envoie le contenu de la conversation (et, si tu le lui demandes, des notes ou des éléments de ton agenda) au fournisseur choisi par l'hébergeur ou par toi (Anthropic, OpenAI, OpenRouter, etc.). Sa propre politique de confidentialité s'applique.</li>
<li><b>Notifications</b> : un relais gratuit sur Cloudflare Workers réveille le téléphone. Il ne voit passer qu'un identifiant technique, jamais le texte des messages.</li>
</ul>

<h2>4 bis. Connexion à Google Agenda (si tu l'actives)</h2>
<p>Si tu connectes ton compte Google à Enhydra, l'application te demande l'autorisation de lire et modifier les rendez-vous de ton agenda Google (autorisation « Google Agenda »). Elle ne demande rien d'autre.</p>
<ul>
<li><b>À quoi ça sert</b> : synchroniser tes rendez-vous entre Google Agenda et l'agenda d'Enhydra. Rien d'autre.</li>
<li><b>Où c'est stocké</b> : sur le serveur qui héberge ton instance. L'éditeur d'Enhydra n'y a pas accès.</li>
<li><b>Partage</b> : les données Google ne sont ni vendues, ni louées, ni transmises à des tiers, ni utilisées pour de la publicité. Seul ton assistant Hermes peut les lire, pour répondre à tes demandes ; il peut alors transmettre ce qu'il lit au fournisseur d'IA que tu as choisi (point 4), uniquement pour te répondre.</li>
<li><b>Respect de la politique de Google</b> : l'utilisation par Enhydra des informations reçues des API Google respecte la <a href="https://developers.google.com/terms/api-services-user-data-policy">politique relative aux données utilisateur des services d'API Google</a>, y compris les exigences d'utilisation limitée.</li>
<li><b>Arrêter</b> : « Couper la liaison » dans Enhydra, ou retire l'accès sur <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>. Les rendez-vous déjà copiés dans Enhydra restent dans ton agenda Enhydra jusqu'à ce que tu les supprimes.</li>
</ul>

<h2>5. Tes droits</h2>
<p>Tu peux demander l'accès, la correction, l'export ou la suppression de tes données à la personne qui héberge ton instance. L'export des notes est intégré à l'application, et la suppression d'un compte efface ses données de l'instance. Pour toute question sur ce site ou sur le logiciel : <a href="mailto:contact@nolancrrd.fr">contact@nolancrrd.fr</a>.</p>

<h2>6. Sécurité</h2>
<p>Les mots de passe sont hachés, le Coffre est chiffré, la communication passe par HTTPS. Le logiciel est libre : son code peut être lu et vérifié par tous sur <a href="https://github.com/nolanCrrd/Enhydra">GitHub</a>.</p>

<h2>7. Modifications</h2>
<p>Cette page peut évoluer ; la date en haut indique la dernière mise à jour.</p>
</div>
"""

COND = """<div class="wrap narrow doc">
<h1>Conditions d'utilisation</h1>
<p class="date">Dernière mise à jour : 6 novembre 2026</p>

<h2>1. Le logiciel</h2>
<p>Enhydra est un logiciel libre distribué sous licence <a href="https://www.gnu.org/licenses/agpl-3.0.html">GNU AGPL-3.0</a>. Tu peux l'installer, l'étudier, le modifier et le partager selon les termes de cette licence. Le code source est sur <a href="https://github.com/nolanCrrd/Enhydra">GitHub</a>.</p>

<h2>2. Une instance, un hébergeur</h2>
<p>Chaque instance d'Enhydra est installée et gérée par une personne (l'hébergeur), qui décide de qui peut y avoir un compte. En utilisant une instance, tu acceptes ses règles. Les conditions de cette page s'appliquent au logiciel et à ce site, pas à un service que l'éditeur fournirait : l'éditeur n'héberge pas les instances des autres.</p>

<h2>3. Ce que tu fais avec l'assistant</h2>
<p>L'assistant Hermes est une intelligence artificielle : il peut se tromper. Relis ce qu'il écrit et vérifie ses actions importantes avant de t'y fier. Tu restes responsable de l'usage que tu en fais et des accès que tu lui confies.</p>

<h2>4. Aucune garantie</h2>
<p>Le logiciel est fourni « en l'état », sans garantie d'aucune sorte, comme le prévoit la licence. Fais des sauvegardes de ton instance. Dans la limite permise par la loi, l'éditeur n'est pas responsable des pertes de données ou des dommages liés à l'usage du logiciel.</p>

<h2>5. Services de tiers</h2>
<p>L'usage de services de tiers depuis Enhydra (fournisseur d'IA, Google Agenda…) reste soumis aux conditions de ces services.</p>

<h2>6. Données personnelles</h2>
<p>Voir la <a href="/confidentialite">politique de confidentialité</a>.</p>

<h2>7. Contact</h2>
<p><a href="mailto:contact@nolancrrd.fr">contact@nolancrrd.fr</a></p>
</div>
"""

NOTFOUND = """<div class="wrap narrow doc">
<h1>Page introuvable</h1>
<p>Cette page n'existe pas (ou plus). <a href="/">Retour à l'accueil</a>.</p>
</div>
"""

PAGES = {
    "index.html": ("Enhydra · Ton assistant personnel, chez toi", "Un chat avec une IA qui agit, une mémoire que tu possèdes, un coffre pour tes accès. Libre, auto-hébergé, en français.", INDEX),
    "confidentialite.html": ("Politique de confidentialité · Enhydra", "Ce que contient une instance Enhydra, ce qui est partagé avec des tiers, et comment arrêter.", CONF),
    "conditions.html": ("Conditions d'utilisation · Enhydra", "Les conditions d'utilisation du logiciel libre Enhydra.", COND),
    "404.html": ("Page introuvable · Enhydra", "Page introuvable.", NOTFOUND),
}

root = Path(__file__).parent / "public"


def digest(name: str) -> str:
    """Empreinte du fichier : l'adresse change quand il change, un navigateur ne garde jamais une vieille version."""
    return hashlib.sha1((root / name).read_bytes()).hexdigest()[:8]


CSS, JS = digest("style.css"), digest("site.js")
for name, (title, desc, body) in PAGES.items():
    (root / name).write_text(HEAD.format(title=title, desc=desc, css=CSS, js=JS) + body + FOOT, encoding="utf-8")
    print("écrit", name)
