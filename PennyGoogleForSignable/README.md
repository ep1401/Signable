# PennyGoogle

## To run this application on your local computer:

(1) In addition to the Python modules required for COS 333 assignments, install these modules:

requests
oauthlib

(2) Create a self-signed certificate consisting of files key.pem and cert.pem in your application directory.  To do that, execute this command on a Unix-like computer:

$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
…
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:NJ
Locality Name (eg, city) []:Princeton
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Princeton University
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:
$

(3) Create a project Google account (i.e., a gmail address) for your project team.  Use your project Google account exclusively for Google authentication setup and subsequent app testing on your local computer.

(4) Register the app (https://localhost:5000) as a client of Google.
   Log into Google using your project Google account
   Browse to https://console.developers.google.com/apis/credentials
   Click CREATE PROJECT
   For Project name enter Penny
   Click CREATE
   Click CONFIGURE CONSENT SCREEN
   For User Type choose External
   Click CREATE
   For App name enter Penny
   For User support email enter your your project gmail address
   For Developer contact information enter your project gmail address
   Click SAVE AND CONTINUE a few times to finish the consent
   Click Credentials
   Click Create Credentials, OAuth client ID, Web Application
   In Authorized JavaScript origins:
      Click ADD URI
      Enter https://localhost:5000
         Typically you also would add a URI for your app on Render.
   In Authorized redirect URIs:
      Click ADD URI
      Enter https://localhost:5000/login/callback
      Typically you also would add a callback URI for your app on Render.

Google provides GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET. Take note of them!

(5) Create these three environment variables:

On Mac & Linux:
export APP_SECRET_KEY=<yourappsecretkey>
export GOOGLE_CLIENT_ID=<yourgoogleclientid>
export GOOGLE_CLIENT_SECRET=<yourgoogleclientsecret>

On MS Windows:
set APP_SECRET_KEY=<yourappsecretkey>
set GOOGLE_CLIENT_ID=<yourgoogleclientid>
set GOOGLE_CLIENT_SECRET=<yourgoogleclientsecret>

(6) Run the test server.
   python runserver.py

(7) Browse to https://localhost:5000
