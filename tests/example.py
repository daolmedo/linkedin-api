import os
import requests
from dotenv import load_dotenv, find_dotenv
from linkedin_api.linkedin import Linkedin  
from linkedin_api.utils import helpers

def extract_public_id(linkedin_url):
   
    if not linkedin_url:
        return None
    
    if "https://www.linkedin.com/in/" in linkedin_url:
        
        public_id = linkedin_url.split("/in/")[-1]
        
        public_id = public_id.rstrip('/')
        return public_id
    return None

def dict_to_cookiejar(cookie_dict):
    jar = requests.cookies.RequestsCookieJar()
    for key, value in cookie_dict.items():
        jar.set(key, value)
    return jar

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Vérifier la récupération des variables
username = "asdasd@test.com"
password = "asdasd"
useragent = " ".join([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/131.0.0.0 Safari/537.36"
])


linkedin_url_test = "https://www.linkedin.com/in/ankurnagpal/"


### Création du client et du script
cookies_dict = {
    'li_at': "AQEDARMCK14CTi6xAAABlDGIPDwAAAGUVZTAPE0AP6TRvIxNAnDNa2KttIBXiRLNzhIHML7OIzp3EDUtGHxSfyZXArFeld8q0TTR73ZACNRTFvf2u0ykyD6BmLvU6L9hE55TF8xC-Bz8bYqqFACxSL8p",
    'JSESSIONID': "ajax:8279155946033820893",
}
    
cookies = dict_to_cookiejar(cookies_dict)

linkedin = Linkedin(username=username, password=password, cookies=cookies, useragent=useragent)

public_id = extract_public_id(linkedin_url_test)

profile = linkedin.get_profile(public_id=public_id)

# Obtain URN_ID of profil
profile_urn = profile.get("profile_urn")
profile_urn_id = helpers.get_id_from_urn(profile_urn);

connexion_request = linkedin.add_connection(profile_public_id = public_id, profile_urn =  profile_urn_id)

if connexion_request == False:
    print("Connection request successfuly sent")
else:
    print("Something went wrong")




