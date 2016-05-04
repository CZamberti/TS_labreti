# -*- coding: utf-8 -*-
import httplib, urllib #libreria http e url
import psutil #libreria per monitorare la macchina. Installare il plugin psutils con: sudo apt-get install python-psutil
import time
from time import localtime, strftime #libreria per fuso orario e timeout tra le operazioni
import socket #libreria di rete, in questo caso necessaria per ottenere il nome dell'host

class bcolors: #colori di stato
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Traccia_e_Invio_TS():
    cpu_pc = psutil.cpu_percent()#variabile percentuale cpu occupata
    mem_usata = psutil.virtual_memory().percent #variabile memoria usata
    pacchetti_inv = psutil.net_io_counters().packets_sent #variabile pacchetti inviati
    pacchetti_ric = psutil.net_io_counters().packets_recv #variabile pacchetti ricevuti

    #invio al server tramite la api key personale e riempio i vari campi
    params = urllib.urlencode ({'field1': cpu_pc, 'field2': mem_usata, 'field3': pacchetti_inv,'field4':pacchetti_ric,'key':'7BNU1GRMMFADSQ9H'}) 
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    
    #stampo nel terminale i valori e lo stato della risposta
    try:
        print (bcolors.BOLD+bcolors.WARNING+"Monitoraggio uso cpu e memoria libera della macchina virtuale " +(socket.gethostname()))+bcolors.ENDC+"\n"#nome della macchina --> modifica
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print bcolors.BOLD+bcolors.OKBLUE+"Cpu occupata: "+bcolors.ENDC,cpu_pc, "%"+"\n"
        print bcolors.BOLD+bcolors.OKBLUE+"Memoria virtuale usata: "+bcolors.ENDC,mem_usata,"%"+"\n"
        print bcolors.BOLD+bcolors.OKBLUE+"Numero pacchetti inviati: "+bcolors.ENDC,pacchetti_inv,"\n"
        print bcolors.BOLD+bcolors.OKBLUE+"Numero pacchetti ricevuti: "+bcolors.ENDC,pacchetti_ric,"\n"
        print bcolors.BOLD+bcolors.OKBLUE+"Timestamp: "+bcolors.ENDC,strftime("%a, %d %b %Y %H:%M:%S", localtime()),"\n"
        print bcolors.BOLD+bcolors.OKBLUE+"Risposta del server: "+bcolors.ENDC,response.status, response.reason,"\n"
        data = response.read()
        conn.close()
        if response.reason==("OK"):
            print (bcolors.BOLD+bcolors.OKGREEN+"La richiesta è andata a buon fine!"+bcolors.ENDC),"\n\n"
    except:
        print bcolors.BOLD+bcolors.FAIL+"Connessione fallita, riprovare." +bcolors.ENDC  

#ripeti operazione ogni 30 secondi (tempo minimo per l'API: 15 secondi)
if __name__ == "__main__":
    while True:
        Traccia_e_Invio_TS()
        time.sleep(30) 
