import os
import requests
from dotenv import load_dotenv, find_dotenv
from linkedin_api.linkedin import Linkedin  
from linkedin_api.utils import helpers
from urllib.parse import urlparse, urlunparse
import random
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed





def clean_linkedin_url(linkedin_url):
    try:
        parsed_url = urlparse(linkedin_url)
        # Remove query parameters and reconstruct the URL
        cleaned_url = urlunparse(parsed_url._replace(query=""))
        return cleaned_url
    except Exception as e:
        print(f"Error cleaning URL {linkedin_url}: {e}")
        return linkedin_url

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


def handle_invitations(linkedin):

    # Fetch 10 invitations
    invitations = linkedin.get_invitations(limit=25)
    print(f"Found {len(invitations)} invitations.")

    invitations = [inv for inv in invitations if 'fromMember' in inv]

    # Process each invitation
    for invitation in invitations:
        try:
            # Extract necessary details
            invitation_urn = invitation['entityUrn']
            invitation_secret = invitation['sharedSecret']

            # Accept the invitation
            if linkedin.reply_invitation(invitation_urn, invitation_secret, action="accept"):
                print(f"Accepted invitation from {invitation['fromMember']['firstName']} {invitation['fromMember']['lastName']}.")

                # Send a "Thank you for connecting!" message
                recipient_id = invitation['fromMember']['entityUrn'].split(":")[-1]
                message = f"Hey {invitation['fromMember']['firstName']}, thanks for connecting.\n\nFollow me on substack for fundraising strategies and founder resources:\n\nhttps://danielolmedo.substack.com/"
                if not linkedin.send_message(message_body=message, recipients=[recipient_id]):
                    print(f"Sent message to {invitation['fromMember']['firstName']} {invitation['fromMember']['lastName']}.")
                else:
                    print(f"Failed to send message to {invitation['fromMember']['firstName']} {invitation['fromMember']['lastName']}.")
            else:
                print(f"Failed to accept invitation from {invitation['fromMember']['firstName']} {invitation['fromMember']['lastName']}.")
        except Exception as e:
            print(f"Error handling invitation: {e}")

def connections_batch(linkedin, linkedin_urls):
    for linkedin_url in linkedin_urls:
        try:
            cleaned_url = clean_linkedin_url(linkedin_url)
            print(f"Cleaned URL: {cleaned_url}")
            public_id = extract_public_id(cleaned_url)
            print(f"Public ID: {public_id}")
            if not public_id:
                print(f"Invalid LinkedIn URL: {cleaned_url}")
                continue

            profile = linkedin.get_profile(public_id=public_id)
            profile_urn = profile.get("profile_urn")
            profile_urn_id = helpers.get_id_from_urn(profile_urn)

            # Retrieve the first name from the profile
            first_name = profile.get("firstName")

            # Create a personalized message
            message = f"Hey {first_name}, are you fundraising? Would you like to receive the sample I mentioned in my email?"

            # Send the connection request with the personalized message
            connexion_request = linkedin.add_connection(profile_public_id=public_id, profile_urn=profile_urn_id, message=message)

            if connexion_request == False:
                print(f"Connection request sent successfully to {first_name} : {cleaned_url}")
            else:
                print(f"Failed to send connection request to {cleaned_url}")

            # Add a random delay between 5 and 10 seconds
            delay = random.randint(5, 10)
            print(f"Waiting for {delay} seconds before processing the next URL.")
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing URL {linkedin_url}: {e}")

def investor_batch(linkedin, linkedin_urls, messages):
    for linkedin_url, message in zip(linkedin_urls, messages):
        try:
            cleaned_url = clean_linkedin_url(linkedin_url)
            print(f"Cleaned URL: {cleaned_url}")
            public_id = extract_public_id(cleaned_url)
            print(f"Public ID: {public_id}")
            if not public_id:
                print(f"Invalid LinkedIn URL: {cleaned_url}")
                continue

            # Retrieve the profile to get the first name
            profile = linkedin.get_profile(public_id=public_id)
            first_name = profile.get("firstName")

            # Get profile network information
            network_info = linkedin.get_profile_network_info(public_profile_id=public_id)
            print(f"Network Info: {network_info}")

            # Create the personalized message
            personalized_message = message.replace("[firstName]", first_name)

            # Check the distance and decide whether to send a message or a connection request
            if network_info.get('distance', {}).get('value') == 'DISTANCE_1':
                # Send the message using recipients parameter
                recipient_id = profile.get("profile_urn").split(":")[-1]
                if linkedin.send_message(message_body=personalized_message, recipients=[recipient_id]):
                    print(f"Failed to send message to {first_name}.")
                else:
                    print(f"Message sent to {first_name}.")
            else:
                # Check if already following
                print(f"Following: {network_info.get('following', False)}")
                if network_info.get('following', False):
                    print(f"Already following {first_name}, probably PENDING connection request.")
                    continue
                # Send a connection request with the message
                profile_urn_id = helpers.get_id_from_urn(profile.get("profile_urn"))
                if linkedin.add_connection(profile_public_id=public_id, message=personalized_message, profile_urn=profile_urn_id):
                    print(f"Failed to send connection request to {first_name}.")
                else:
                    print(f"Connection request sent to {first_name}.")

            # Add a random delay between 5 and 10 seconds
            delay = random.randint(5, 10)
            print(f"Waiting for {delay} seconds before processing the next URL.")
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing URL {linkedin_url}: {e}")

def message_batch(linkedin, linkedin_urls, message):
    for linkedin_url in linkedin_urls:
        try:
            cleaned_url = clean_linkedin_url(linkedin_url)
            print(f"Cleaned URL: {cleaned_url}")
            public_id = extract_public_id(cleaned_url)
            print(f"Public ID: {public_id}")
            if not public_id:
                print(f"Invalid LinkedIn URL: {cleaned_url}")
                continue

            # Retrieve the profile to get the first name
            profile = linkedin.get_profile(public_id=public_id)
            first_name = profile.get("firstName")

            # Get profile network information
            network_info = linkedin.get_profile_network_info(public_profile_id=public_id)
            print(f"Network Info: {network_info}")

            # Create the message
            personalized_message = message.replace("[firstName]", first_name)

            # Check the distance and decide whether to send a message or a connection request
            if network_info.get('distance', {}).get('value') == 'DISTANCE_1':
                # Send the message using recipients parameter
                recipient_id = profile.get("profile_urn").split(":")[-1]
                if linkedin.send_message(message_body=personalized_message, recipients=[recipient_id]):
                    print(f"Failed to send message to {first_name}.")
                else:
                    print(f"Message sent to {first_name}.")
            else:
                # Check if already following
                if network_info.get('following', False):
                    print(f"Already following {first_name}, probably PENDING connection request.")
                    continue
                # Send a connection request with the message
                profile_urn_id = helpers.get_id_from_urn(profile.get("profile_urn"))
                if linkedin.add_connection(profile_public_id=public_id, message=personalized_message, profile_urn=profile_urn_id):
                    print(f"Failed to send connection request to {first_name}.")
                else:
                    print(f"Connection request sent to {first_name}.")

            # Add a random delay between 5 and 10 seconds
            delay = random.randint(5, 10)
            print(f"Waiting for {delay} seconds before processing the next URL.")
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing URL {linkedin_url}: {e}")


def fetch_conversations(linkedin):
    """Fetch all conversations and their threads for the LinkedIn user.

    :param linkedin: LinkedIn object to interact with the LinkedIn API
    :return: List of conversations with their threads
    :rtype: list
    """
    try:
        # Fetch all conversations
        conversations = linkedin.get_conversations(start=60)
        all_conversations = []

        def fetch_thread(conversation):
            conversation_urn_id = conversation['dashEntityUrn'].split(':')[-1]
            # Fetch threads for each conversation
            threads = linkedin.get_conversation(conversation_urn_id)
            return {
                'conversation': conversation,
                'thread': threads.get('elements', [])
            }

        # Use ThreadPoolExecutor to fetch threads in parallel
        with ThreadPoolExecutor() as executor:
            future_to_conversation = {executor.submit(fetch_thread, conv): conv for conv in conversations.get('elements', [])}
            for future in as_completed(future_to_conversation):
                try:
                    all_conversations.append(future.result())
                except Exception as e:
                    print(f"Error fetching conversation thread: {e}")

        return all_conversations

    except Exception as e:
        print(f"Error fetching conversations: {e}")
        return []
    

def extract_conversation_dataframe(all_conversations):
    """Extracts conversation data for Excel storage.

    :param all_conversations: List of conversations with their threads
    :return: DataFrame with conversation data
    :rtype: pd.DataFrame
    """
    data = []

    for conversation in all_conversations:
        conversation_urn = conversation['conversation']['entityUrn']
        for message in conversation['thread']:
            message_content = message['eventContent']['com.linkedin.voyager.messaging.event.MessageEvent']['attributedBody']['text']
            sender_first_name = message['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile'].get('firstName', '')
            sender_last_name = message['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile'].get('lastName', '')
            
            data.append({
                'Conversation EntityUrn': conversation_urn,
                'Message Content': message_content,
                'Sender First Name': sender_first_name,
                'Sender Last Name': sender_last_name
            })

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    return df

def extract_thread_id(backendUrn: str) -> str:
    """
    Extracts the thread ID from a given backendUrn.

    :param backendUrn: The full URN string
    :type backendUrn: str
    :return: The extracted thread ID
    :rtype: str
    """
    prefix = "urn:li:messagingThread:"
    if backendUrn.startswith(prefix):
        return backendUrn[len(prefix):]
    return backendUrn  # or raise an error if the format is unexpected

def extract_user_urn(entity_urn: str) -> str:
    """
    Extracts the user URN from a given entity URN by removing the prefix.

    :param entity_urn: The full entity URN string
    :type entity_urn: str
    :return: The extracted user URN
    :rtype: str
    """
    prefix = "urn:li:fsd_profile:"
    if entity_urn.startswith(prefix):
        return entity_urn[len(prefix):]
    return entity_urn  # or raise an error if the format is unexpected


def get_entity_urn_from_globals(globals_data):
    """Retrieve the entityUrn from the global navigation data."""
    primary_items = globals_data.get('data', {}).get('feedDashGlobalNavs', {}).get('primaryItems', [])

    for item in primary_items:
        me_menu = item.get('meMenu')
        if me_menu and 'profile' in me_menu:
            return me_menu['profile'].get('entityUrn')

    print("entityUrn not found in globals")
    return None

# Vérifier la récupération des variables
username = "asdasd@test.com"
password = "asdasd"
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

linkedin_url_test = "https://www.linkedin.com/in/gregorymuschel/"

cleaned_url = clean_linkedin_url(linkedin_url_test)
print(f"Cleaned URL: {cleaned_url}")


### Création du client et du script
cookies_dict = {
    'li_at': "AQEDARMCK14DI_4WAAABm74VIzQAAAGcLVi1N04AaPpzRrY0iZ4Ja_UdjxhJbzw3mCUzv-pUyJQsThcqoryZxQG8YPrrBA41kCUDMkfUtYjxCRXb-PrPaINAM96q3qcy4bpAxFes-czRm9-WWXY6reHh",
    'JSESSIONID': "ajax:8279155946033820893",
}
    
cookies = dict_to_cookiejar(cookies_dict)

# Enable debug mode to see detailed logs
linkedin = Linkedin(username=username, password=password, cookies=cookies, useragent=useragent, debug=True)

#handle_invitations(linkedin)


linkedin_urls = [
    "https://www.linkedin.com/in/pachos",
    "https://www.linkedin.com/in/siddharthgg"
]

messages = [
    "Hello [firstName], I would like to connect with you on LinkedIn.",
    "Hi [firstName], let's connect on LinkedIn!"
]

# Comment out conversation testing code
# globals_data = linkedin.get_globals()
# entity_urn = get_entity_urn_from_globals(globals_data)
# user_urn = extract_user_urn(entity_urn)
# print(f"User URN: {user_urn}")

# conversations = linkedin.get_conversations(limit=20)

# conversationsv2 = linkedin.get_conversations_v2(mailbox_urn=user_urn)

# thread_id = extract_thread_id(conversationsv2['data']['messengerConversationsByCategoryQuery']['elements'][0]['backendUrn'])

# thread = linkedin.get_thread_v2(mailbox_urn="ACoAABMCK14BZYQEFee5Ir7zBXRulzkHn_aCgio", messaging_thread_urn=thread_id)

# Example usage
#all_conversations = fetch_conversations(linkedin)
#conversation_data_df = extract_conversation_dataframe(all_conversations)

# Save to Excel
#conversation_data_df.to_excel('conversation_data.xlsx', index=False)




# message = "Hello [firstName], I would like to connect with you on LinkedIn."

# for conversation in conversations.get('elements', []):
#     print(conversation.get('dashEntityUrn'))

#message_batch(linkedin, linkedin_urls, message)

print("\n=== Starting Connection Request Test ===")
print(f"Target URL: {linkedin_url_test}")

public_id = extract_public_id(linkedin_url_test)
print(f"Extracted Public ID: {public_id}")

print("\nResolving URN from HTML...")
# Directly resolve the URN without calling get_profile() since that API is deprecated
profile_urn_id = linkedin._resolve_public_id_to_urn(public_id)

if not profile_urn_id:
    print("[FAIL] Failed to resolve URN from HTML")
    exit(1)

print(f"[OK] Resolved URN ID: {profile_urn_id}")

# Test get_profile() end-to-end with the new URN-based endpoint
print("\n=== Testing get_profile() ===")
print("Testing with public_id (triggers _resolve_public_id_to_urn + /identity/profiles/{urn_id})...")
try:
    profile = linkedin.get_profile(public_id=public_id)
    if profile:
        print(f"[OK] get_profile() returned data. Keys: {list(profile.keys())}")
        print(f"  Name: {profile.get('firstName', '?')} {profile.get('lastName', '?')}")
        print(f"  URN ID: {profile.get('urn_id', '?')}")
        print(f"  Public ID: {profile.get('public_id', '?')}")
    else:
        print("[FAIL] get_profile() returned empty dict")
except KeyError as e:
    print(f"[FAIL] get_profile() threw KeyError: {e}")
    print("  The /identity/profiles/{{urn_id}} endpoint likely returns a different structure than /profileView")
    # Fetch the raw response to see what we actually get
    print("\n  Fetching raw response to inspect structure...")
    raw_res = linkedin._fetch(f"/identity/profiles/{profile_urn_id}")
    raw_data = raw_res.json()
    print(f"  Raw response keys: {list(raw_data.keys()) if isinstance(raw_data, dict) else 'not a dict'}")
    import json
    print(f"  Raw response (truncated): {json.dumps(raw_data, indent=2)[:2000]}")
except Exception as e:
    print(f"[FAIL] get_profile() threw {type(e).__name__}: {e}")

print("\n=== Test Complete ===\n")




