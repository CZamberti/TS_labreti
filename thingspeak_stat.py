import time;
import httplib, urllib #libreria http e ur
import psutil #libreria per monitorare la macchina.

while True:
    post = urllib.urlencode (
      { "field1": psutil.cpu_percent(),                  # percentuale cpu occupata
        "field2": psutil.virtual_memory().percent,       # memoria usata
        "field3": psutil.net_io_counters().packets_sent, # pacchetti inviati
        "field4": psutil.net_io_counters().packets_recv, # variabile pacchetti ricevuti
        "key":"71PZRVYSK1J4FFQ0"}                        # WRITE KEY
        )
    print post
    headers = {
      "Content-type": "application/x-www-form-urlencoded"
      } 
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", post, headers)
        conn.close()
    except:
        print "Connessione fallita: dato non resistrato." 
    time.sleep(60) 
