import sys
import os
import requests
import json
import subprocess

bloc = sys.argv[1]
RDNS = sys.argv[2]
print("Bloc inscrit : ", bloc)
#fabrication du domaine in-addr.arpa

API = "CHANGEME"
print("API : ", API)
DNS = "CHANGEME"
print("DNS : ", DNS)
#Detacher le CIDR du bloc pour garder le CIDR en variable
CIDR = bloc.split("/")[1]
print("CIDR : ", CIDR)
#On retire le CIDR du bloc 
bloc = bloc.split("/")[0]
#Inversion du bloc pour le DNS
bloc = bloc.split(".")
bloc.reverse()
bloc = ".".join(bloc)
domaine = bloc + ".in-addr.arpa"
print(domaine)
print("Bloc inversé : ", bloc)

#Calcul du nombre d'IP à faire avec le CIDR
nb_ip = 2**(32-int(CIDR))
nb_ip = nb_ip - 1
print("Nombre d'IP : ", nb_ip)
#Boucle for pour inscrire chaque IP du bloc dans le DNS
for i in range(0, nb_ip):
    #Config du sous domaine :
    sous_domaine = str(i) + "." + bloc + RDNS
    ip = str(i) + "." + bloc
    print("Sous domaine : ", sous_domaine)
    url = DNS + domaine
    commande = "curl -H 'Content-Type: application/json' -X PATCH --data '{\"rrsets\": [ {\"name\": \"" + ip + ".in-addr.arpa.\", \"type\": \"PTR\", \"ttl\": 86400, \"changetype\": \"REPLACE\", \"records\": [ {\"content\": \"" + sous_domaine + ".\", \"disabled\": false } ] } ] }' -H 'X-API-Key: " + API + "' " + url + " | jq ."
    print(commande)
    #execution de la commande
    subprocess.call(commande, shell=True)

    