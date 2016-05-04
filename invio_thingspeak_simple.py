# -*- coding: utf-8 -*-
import httplib, urllib #libreria http e url
import psutil #libreria per monitorare la macchina. Installare il plugin psutils con: sudo apt-get install python-psutil
import time
from time import localtime, strftime #libreria per fuso orario e timeout tra le operazioni
import socket #libreria di rete, in questo caso necessaria per ottenere il nome dell'host

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
        print ("Monitoraggio uso cpu e memoria libera della macchina virtuale " +(socket.gethostname()))+"\n"#nome della macchina --> modifica
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print "Cpu occupata: ", cpu_pc, "%","\n"
        print "Memoria virtuale usata: ",mem_usata,"%","\n"
        print "Numero pacchetti inviati: ",pacchetti_inv,"\n"
        print "Numero pacchetti ricevuti: ",pacchetti_ric,"\n"
        print "Timestamp: "+strftime("%a, %d %b %Y %H:%M:%S", localtime()),"\n"
        print "Risposta del server: ",response.status, response.reason,"\n"
        data = response.read()
        conn.close()
        if response.reason==("OK"):
            print ("La richiesta è andata a buon fine!"),"\n\n"
    except:
        print "Connessione fallita, riprovare." 

#ripeti operazione ogni 16 secondi (tempo minimo per l'API: 15 secondi)
if __name__ == "__main__":
    while True:
        Traccia_e_Invio_TS()
        time.sleep(16) 
