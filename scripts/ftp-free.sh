#!/bin/sh

# initialisations
URL_FREE=http://dl.free.fr
USER_AGENT="Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.15) Gecko/20110303 Ubuntu/10.10 (maverick) Firefox/3.6.15"
REFERER=${URL_FREE}
ENTETE_ACCEPT='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
ENTETE_ACCEPT_LANGUAGE='Accept-Language: fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3'
ENTETE_ACCEPT_CHARSET='Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7'

PATTERN_RECUPERATION_ID='<form action='
PATTERN_RESULTAT_DEPOT="The document has moved"
PATTERN_SUIVI_DEPOT_TERMINE='proc&eacute;dure termin&eacute;e avec succ&egrave;s'
PATTERN_SUIVI_DEPOT_EN_COURS='Envoi en cours'
PATTERN_SUIVI_DEPOT_EN_ATTENTE='En attente de traitement'
PATTERN_SUIVI_DEPOT_CONTROLE='Calcul de la somme de contr&ocirc;le...'
PATTERN_SUIVI_DEPOT_MISE_EN_LIGNE='Mise en ligne du fichier'
PATTERN_SUIVI_DEPOT_ANTIVIRUS='Test antivirus'
PATTERN_FICHIER_DEPOSE="${PATTERN_SUIVI_DEPOT_TERMINE}"
PATTERN_DEMANDE_SUPPRESSION="${PATTERN_SUIVI_DEPOT_TERMINE}"
PATTERN_DEMANDE_SUPPRESSION_EFFECTIVE='Si vous souhaitez r&eacute;element supprimer le fichier'

PATTERN_ERREUR_INTERNE="Erreur 500 - Erreur interne du serveur"
PATTERN_DEMANDE_SUPPRESSION_EFFECTIVE2="Vous pouvez supprimer le fichier lorsque vous le d&eacute;sirez via l'adresse suivante:  "


usage() {
  echo "usage : $(basename $0) NomCompletFichier"
}

# debut du script
FICHIER=$1
if [ ! -f "${FICHIER}" ]; then
  usage
  exit 1
fi

echo "Etape 1 - recuperation d'un identifiant de depot sur ${URL_FREE}"
FICHIER_RECUPERATION_ID=$(mktemp)
curl -A "${USER_AGENT}" -H "${ENTETE_ACCEPT}" -H "${ENTETE_ACCEPT_LANGUAGE}" -H "${ENTETE_ACCEPT_CHARSET}" "${URL_FREE}" 1>"${FICHIER_RECUPERATION_ID}" 2>"${FICHIER_RECUPERATION_ID}.err"
if [ $? -ne 0 ]; then
  echo "Echec lors de la recuperation d'un identifiant"
  exit 1
fi
URI_DEPOT=$(grep "${PATTERN_RECUPERATION_ID}" ${FICHIER_RECUPERATION_ID} | cut -d \" -f 2)
if [ -z "${URI_DEPOT}" ]; then
  echo "Echec lors de la recuperation d'un identifiant - URI de depot vide"
  exit 1
fi
echo "URI_DEPOT : ${URI_DEPOT}"
echo "URL_DEPOT : ${URL_FREE}${URI_DEPOT}"

echo "Etape 2 - depot du fichier ${FICHIER} sur ${URL_FREE}${URI_DEPOT}"
FICHIER_RESULTAT_UPLOAD=$(mktemp)
echo "FICHIER_RESULTAT_UPLOAD : ${FICHIER_RESULTAT_UPLOAD}"
curl -A "${USER_AGENT}" -e "${REFERER}" -H "${ENTETE_ACCEPT}" -H "${ENTETE_ACCEPT_LANGUAGE}" -H "${ENTETE_ACCEPT_CHARSET}" -F "ufile=@${FICHIER};filename=${FICHIER};type=application/octet-stream" -F mail1="" -F mail2="" -F mail3="" -F mail4="" -F message="" -F password="" "${URL_FREE}${URI_DEPOT}" 1>"${FICHIER_RESULTAT_UPLOAD}" 2>"${FICHIER_RESULTAT_UPLOAD}.err"
if [ $? -ne 0 ]; then
  echo "Echec lors du depot du fichier"
  exit 1
fi
URL_SUIVI_DEPOT=$(grep "${PATTERN_RESULTAT_DEPOT}" ${FICHIER_RESULTAT_UPLOAD} | cut -d \" -f 2)
if [ -z "${URL_SUIVI_DEPOT}" ]; then
  echo "Echec lors du depot du fichier - URL de suivi vide"
  exit 1
fi
echo "URL_SUIVI_DEPOT : ${URL_SUIVI_DEPOT}"

echo "Etape 3 - suivi du depot du fichier ${FICHIER} via l'URL ${URL_SUIVI_DEPOT}"
sleep 5
FICHIER_RESULTAT_SUIVI=$(mktemp)
echo "FICHIER_RESULTAT_SUIVI : ${FICHIER_RESULTAT_SUIVI}"
iteration=1
while true
do
  echo "Suivi du depot - iteration numero ${iteration}"
  curl -A "${USER_AGENT}" -e "${REFERER}" -H "${ENTETE_ACCEPT}" -H "${ENTETE_ACCEPT_LANGUAGE}" -H "${ENTETE_ACCEPT_CHARSET}" "${URL_SUIVI_DEPOT}" 1>"${FICHIER_RESULTAT_SUIVI}" 2>"${FICHIER_RESULTAT_SUIVI}.err"
  if [ $? -ne 0 ]; then
    echo "Echec lors du suivi du depot"
    exit 1
  fi
  if [ $(grep -c "${PATTERN_SUIVI_DEPOT_TERMINE}" ${FICHIER_RESULTAT_SUIVI}) -eq 1 ]; then
    break
  elif [ $(grep -c -E "(${PATTERN_SUIVI_DEPOT_CONTROLE}|${PATTERN_SUIVI_DEPOT_MISE_EN_LIGNE}|${PATTERN_SUIVI_DEPOT_EN_COURS}|${PATTERN_SUIVI_DEPOT_EN_ATTENTE}|${PATTERN_SUIVI_DEPOT_ANTIVIRUS})" ${FICHIER_RESULTAT_SUIVI}) -eq 1 ]; then
    sleep 5
  else
    echo "Echec lors du suivi du depot - fichier ni traite ni en cours de traitement"
    exit 1
  fi
  iteration=$((iteration+1))
done
URL_FICHIER_DEPOSE=$(grep "${PATTERN_FICHIER_DEPOSE}" ${FICHIER_RESULTAT_SUIVI} | awk ' BEGIN { FS="</*a[^>]*>" } { print $2 } ')
URL_DEMANDE_SUPPRESSION=$(grep "${PATTERN_DEMANDE_SUPPRESSION}" ${FICHIER_RESULTAT_SUIVI} | awk ' BEGIN { FS="</*a[^>]*>" } { print $4 } ')
if [ -z "${URL_DEMANDE_SUPPRESSION}" ]; then
  echo "Echec lors du depot du fichier - URL de demande de suppression du fichier vide"
  #exit 1
fi

echo "Etape 4 - recuperation URL de suppression effective du fichier depose"
FICHIER_RESULTAT_DEMANDE_SUPPRESSION=$(mktemp)
echo "FICHIER_RESULTAT_DEMANDE_SUPPRESSION : ${FICHIER_RESULTAT_DEMANDE_SUPPRESSION}"
curl -A "${USER_AGENT}" -e "${REFERER}" -H "${ENTETE_ACCEPT}" -H "${ENTETE_ACCEPT_LANGUAGE}" -H "${ENTETE_ACCEPT_CHARSET}" "${URL_DEMANDE_SUPPRESSION}" 1>"${FICHIER_RESULTAT_DEMANDE_SUPPRESSION}" 2>"${FICHIER_RESULTAT_DEMANDE_SUPPRESSION}.err"
if [ $? -ne 0 ]; then
  echo "Echec lors de la recuperation de l'URL suppression effective du fichier depose"
  #exit 1
fi

TEST_SUPPRESSION_FICHIER_SERVEUR=$(grep "${PATTERN_ERREUR_INTERNE}" ${FICHIER_RESULTAT_DEMANDE_SUPPRESSION})
echo "TEST_SUPPRESSION_FICHIER_SERVEUR=$TEST_SUPPRESSION_FICHIER_SERVEUR"
if [ -z "${TEST_SUPPRESSION_FICHIER_SERVEUR}" ]; then
    # Pas de pbme de serveur
    URL_SUPPRESSION_FICHIER_DEPOSE=$(grep "${PATTERN_DEMANDE_SUPPRESSION_EFFECTIVE}" ${FICHIER_RESULTAT_DEMANDE_SUPPRESSION} | awk ' BEGIN { FS="<a href=\"" } { print $2 } '| cut -d \" -f 1)
else
    # Pbme de serveur
    URL_SUPPRESSION_FICHIER_DEPOSE=$(grep "${PATTERN_DEMANDE_SUPPRESSION_EFFECTIVE2}" ${FICHIER_RESULTAT_SUIVI} | awk ' BEGIN { FS="<a class=\"underline\" href=\"" } { print $3 } ' | cut -d \" -f 1)
fi
if [ -z "${URL_SUPPRESSION_FICHIER_DEPOSE}" ]; then
    echo "Echec lors de la recuperation de l'URL suppression effective du fichier depose - URL effective vide"
    #exit 1
fi

echo "Etape 5 - resultats"
echo "Fichier d'origine : ${FICHIER}"
echo "URL Fichier depose : ${URL_FICHIER_DEPOSE}"
echo "URL pour suppression du fichier : ${URL_FREE}${URL_SUPPRESSION_FICHIER_DEPOSE}"
