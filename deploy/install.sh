#!/usr/bin/env bash
# Met le site en ligne sur enhydra.nolancrrd.fr (Apache + certificat Let's Encrypt). À lancer en root :
#   sudo bash /opt/enhydra-site/deploy/install.sh
# Relançable sans risque. Les mises à jour du site n'ont pas besoin de ce script : `git pull` suffit.
set -euo pipefail

DOMAIN="enhydra.nolancrrd.fr"
SITE="/opt/enhydra-site"
CONF="/etc/apache2/sites-available/enhydra-site.conf"
CERT="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
EMAIL="${LETSENCRYPT_EMAIL:-contact@nolancrrd.fr}"

[ "$(id -u)" -eq 0 ] || { echo "Lance ce script avec sudo."; exit 1; }
[ -f "$SITE/public/index.html" ] || { echo "Site introuvable dans $SITE/public"; exit 1; }
for m in rewrite headers expires ssl negotiation; do a2enmod -q "$m"; done

if [ ! -f "$CERT" ]; then
  echo "Pas encore de certificat : site en HTTP le temps de l'obtenir."
  cat > "$CONF" <<HTTP
<VirtualHost *:80>
    ServerName $DOMAIN
    DocumentRoot $SITE/public
    <Directory $SITE/public>
        Require all granted
    </Directory>
</VirtualHost>
HTTP
  a2ensite -q enhydra-site
  apache2ctl configtest
  systemctl reload apache2
  certbot certonly --webroot -w "$SITE/public" -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"
fi

cp "$SITE/deploy/enhydra-site.conf" "$CONF"
a2ensite -q enhydra-site
if ! apache2ctl configtest; then
  a2dissite -q enhydra-site # une configuration cassée ne doit pas gêner un prochain rechargement d'Apache
  echo "La configuration d'Apache est refusée : site désactivé, rien n'a changé pour les autres sites."
  exit 1
fi
systemctl reload apache2

echo
curl -fsS -o /dev/null -w "https://$DOMAIN -> HTTP %{http_code}\n" "https://$DOMAIN/" || echo "Le site ne répond pas encore en HTTPS."
echo "Terminé."
