################################################################################
# server/test/test_droid.py                                         2014-12-09 #
# Covoiturage Sopra - INSA Toulouse                               Félix Poisot #
################################################################################

# Simule rapidement les requêtes envoyées par l'application android.

# testé sous Python 3.4.1

from http.client import *

host = "felix-host.ddns.net"

# Notre SessionID
cookie = None


def mkReq(conn, command, payload):
   """command: url à taper sur le serveur.
      payload: données JSON à mettre dans le POST."""
   global cookie

   pl = None
   headers = {}
   if cookie:
      headers = {cookie[0]:cookie[1]}
   if payload:
      # encode(): utf-8 semble être l'encodage par défaut
      pl = payload.encode()
      headers["Content-Type"] = "application/json"
   
   conn.request("POST", "/android/"+command, pl, headers) 
   return conn.getresponse()
   
   
def parse_cookie(resp):
   """Extrait le header à renvoyer à chaque nouvelle requête"""
   global cookie
   
   for hd in resp.getheaders():
      if hd[0] == "Set-Cookie":
         cookie = ("cookie", hd[1].split(";")[0])

   
   
if __name__ == "__main__":

   conn = HTTPSConnection(host)
      
   print("login...")
   resp = mkReq(conn, "login", '{"name":"whatsthepassword","password":"password"}')
   parse_cookie(resp)
   print(resp.read())
   print("Got cookie: " + str(cookie))
 
   print("detailsAccount...")
   resp = mkReq(conn, "detailsAccount", '{"name":"someAccount"}')
   print(resp.read())
 
#   print("forgottenPsswd...")
#   req = mkReq("forgottenPsswd", '{"name":"name@some-mail.com"}')
#   resp = urlopen(req)
   
   print("logout...")
   resp = mkReq(conn, "logout", '{}')
   resp.read()
   print("done !")
   
   
   
   
   