<div align="center">

# LinkedIn API for Python

![Build](https://img.shields.io/github/actions/workflow/status/tomquirk/linkedin-api/ci.yml?label=Build&logo=github) [![Documentation](https://img.shields.io/readthedocs/linkedin-api?label=Docs)](https://linkedin-api.readthedocs.io) [![GitHub Release](https://img.shields.io/github/v/release/tomquirk/linkedin-api?label=PyPI&logo=python)](https://pypi.org/project/linkedin-api/) [![Discord](https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=ffffff)](https://discord.gg/hdd48NEB37)

Search profiles, send messages, find jobs and more in Python. No official API access required.

<p align="center">
    <a href="https://linkedin-api.readthedocs.io">Documentation</a>
    ·
    <a href="#quick-start">Quick Start</a>
    ·
    <a href="#how-it-works">How it works</a>
</p>

</div>

<br>

<h3 align="center">Sponsors</h3>

<p align="center">
<a href="https://bit.ly/4fUyE9J" target="_blank">
    <img width="450px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/scrapin-banner.png" alt="Scrapin">
  </a>
</p>

<p align="center" dir="auto" >
  <a href="https://bit.ly/3AFPGZd" target="_blank">
    <img height="45px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/proapis.png" alt="iScraper by ProAPIs">
  </a>
  <a href="https://bit.ly/3SWnB63" target="_blank">
    <img height="45px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/prospeo.png" alt="Prospeo">
  </a>
  <a href="https://bit.ly/3SRximo" target="_blank">
    <img height="45px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/proxycurl.png" alt="proxycurl">
  </a>
  <a href="https://bit.ly/3Mbksvd" target="_blank">
    <img height="45px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/lix.png" alt="Lix">
  </a>
  <a href="https://bit.ly/3WOIMrX" target="_blank">
    <img  height="70px" src="https://raw.githubusercontent.com/tomquirk/linkedin-api/main/docs/assets/logos/unipile.png" alt="Unipile">
  </a>
</p>

<p align="center"><a href="https://bit.ly/4cCjbIq" target="_blank">Become a sponsor</a></p>

<br>

## Features

- ✅ No official API access required. Just use a valid LinkedIn user account.
- ✅ Direct HTTP API interface. No Selenium, Pupeteer, or other browser-based scraping methods.
- ✅ Get and search people, companies, jobs, posts
- ✅ Send and retrieve messages
- ✅ Send and accept connection requests
- ✅ Get and react to posts

And more! [Read the docs](https://linkedin-api.readthedocs.io/en/latest/api.html) for all API methods.

> [!IMPORTANT]
> This library is not officially supported by LinkedIn. Using this library might violate LinkedIn's Terms of Service. Use it at your own risk.

## Installation

> [!NOTE]
> Python >= 3.10 required

###

```bash
pip install linkedin-api
```

Or, for bleeding edge:

```bash
pip install git+https://github.com/tomquirk/linkedin-api.git
```

### Quick Start

> [!TIP]
> See all API methods on the [docs](https://linkedin-api.readthedocs.io/en/latest/api.html).

The following snippet demonstrates a few basic linkedin_api use cases:

```python
from linkedin_api import Linkedin

# Authenticate using any Linkedin user account credentials
api = Linkedin('reedhoffman@linkedin.com', '*******')

# GET a profile
profile = api.get_profile('billy-g')

# GET a profiles contact info
contact_info = api.get_profile_contact_info('billy-g')

# GET 1st degree connections of a given profile
connections = api.get_profile_connections('1234asc12304')
```

## Commercial alternatives

> This is a sponsored section

<h3>
<a href="https://prospeo.io/api/linkedin-email-finder">
Prospeo
</a>
</h3>

Extract data and find verified emails in real-time with [Prospeo LinkedIn Email Finder API](https://prospeo.io/api/linkedin-email-finder).

<details>
  <summary>Learn more</summary>
Submit a LinkedIn profile URL to our API and get:

- Profile data extracted in real-time
- Company data of the profile
- Verified work email of the profile
- Exclusive data points (gender, cleaned country code, time zone...)
- One do-it-all request
- Stable API, tested under high load

Try it with 75 profiles. [Get your FREE API key now](https://prospeo.io/api/linkedin-email-finder).

</details>

<h3>
<a href="https://nubela.co/proxycurl/?utm_campaign=influencer%20marketing&utm_source=github&utm_medium=social&utm_term=-&utm_content=tom%20quirk">
Proxycurl
</a>
</h3>

Scrape public LinkedIn profile data at scale with [Proxycurl APIs](https://nubela.co/proxycurl/?utm_campaign=influencer%20marketing&utm_source=github&utm_medium=social&utm_term=-&utm_content=tom%20quirk).

<details>
  <summary>Learn more</summary>
  
- Scraping Public profiles are battle tested in court in HiQ VS LinkedIn case.
- GDPR, CCPA, SOC2 compliant
- High rate limit - 300 requests/minute
- Fast - APIs respond in ~2s
- Fresh data - 88% of data is scraped real-time, other 12% are not older than 29 days
- High accuracy
- Tons of data points returned per profile

Built for developers, by developers.

</details>

<h3>
<a href="https://www.unipile.com/communication-api/messaging-api/linkedin-api/?utm_campaign=git%20tom%20quirk">
Unipile
</a>
</h3>

Full [LinkedIn API](https://www.unipile.com/communication-api/messaging-api/linkedin-api/?utm_campaign=git%20tom%20quirk): Connect Classic/Sales Navigator/Recruiter, synchronize real-time messaging, enrich data and build outreach sequences…

<details>
  <summary>Learn more</summary>
  
- Easily connect your users in the cloud with our white-label authentication (captcha solving, in-app validation, OTP, 2FA).
- Real-time webhook for each message received, read status, invitation accepted, and more.
- Data extraction: get profile, get company, get post, extract search results from Classic + Sales Navigator + Recruiter
- Outreach sequences: send invitations, InMail, messages, and comment on posts…

Test [all the features](https://www.unipile.com/communication-api/messaging-api/linkedin-api/?utm_campaign=git%20tom%20quirk) with our 7-day free trial.

</details>

<h3>
<a href="https://bit.ly/4fUyE9J">
ScrapIn
</a>
</h3>

Scrape Any Data from LinkedIn, without limit with [ScrapIn API](https://bit.ly/4fUyE9J).

<details>
  <summary>Learn more</summary>
  
- Real time data (no-cache)
- Built for SaaS developers
- GDPR, CCPA, SOC2 compliant
- Interactive API documentation
- A highly stable API, backed by over 4 years of experience in data provisioning, with the added reliability of two additional data provider brands owned by the company behind ScrapIn.

Try it for free. [Get your API key now](https://bit.ly/4fUyE9J)

</details>

<h3>
<a href="https://bit.ly/3AFPGZd">
iScraper by ProAPIs, Inc.
</a>
</h3>

Access high-quality, real-time LinkedIn data at scale with [iScraper API](https://bit.ly/3AFPGZd), offering unlimited scalability and unmatched accuracy.

<details>

<summary>Learn more</summary>

- Real-time LinkedIn data scraping with unmatched accuracy
- Hosted datasets with powerful Lucene search access
- Designed for enterprise and corporate-level applications
- Handles millions of scrapes per day, ensuring unlimited scalability
- Trusted by top enterprises for mission-critical data needs
- Interactive API documentation built on OpenAPI 3 specs for seamless integration
- Backed by over 10 years of experience in real-time data provisioning
- Lowest price guarantee for high volume use

Get started [here](https://bit.ly/3AFPGZd).

</details>

> End sponsored section

## Development

### Dependencies

- [`poetry`](https://python-poetry.org/docs/)
- A valid Linkedin user account (don't use your personal account, if possible)

### Development installation

1. Create a `.env` config file (use `.env.example` as a reference)
2. Install dependencies using `poetry`:

   ```bash
   poetry install
   poetry self add poetry-plugin-dotenv
   ```

### Run tests

Run all tests:

```bash
poetry run pytest
```

Run unit tests:

```bash
poetry run pytest tests/unit
```

Run E2E tests:

```bash
poetry run pytest tests/e2e
```

### Lint

```bash
poetry run black --check .
```

Or to fix:

```bash
poetry run black .
```

### Troubleshooting

#### I keep getting a `CHALLENGE`

Linkedin will throw you a curve ball in the form of a Challenge URL. We currently don't handle this, and so you're kinda screwed. We think it could be only IP-based (i.e. logging in from different location). Your best chance at resolution is to log out and log back in on your browser.

**Known reasons for Challenge** include:

- 2FA
- Rate-limit - "It looks like you’re visiting a very high number of pages on LinkedIn.". Note - n=1 experiment where this page was hit after ~900 contiguous requests in a single session (within the hour) (these included random delays between each request), as well as a bunch of testing, so who knows the actual limit.

Please add more as you come across them.

#### Search problems

- Mileage may vary when searching general keywords like "software" using the standard `search` method. They've recently added some smarts around search whereby they group results by people, company, jobs etc. if the query is general enough. Try to use an entity-specific search method (i.e. search_people) where possible.

## How it works

This project attempts to provide a simple Python interface for the LinkedIn API.

> Do you mean the [legit LinkedIn API](https://developer.linkedin.com/)?

NO! To retrieve structured data, the [LinkedIn Website](https://linkedin.com) uses a service they call **Voyager**. Voyager endpoints give us access to pretty much everything we could want from LinkedIn: profiles, companies, connections, messages, etc. - anything that you can see on linkedin.com, we can get from Voyager.

This project aims to provide complete coverage for Voyager.

[How does it work?](#deep-dive)

### Deep dive

Voyager endpoints look like this:

```text
https://www.linkedin.com/voyager/api/identity/profileView/tom-quirk
```

Or, more clearly

```text
 ___________________________________ _______________________________
|             base path             |            resource           |
https://www.linkedin.com/voyager/api /identity/profileView/tom-quirk
```

They are authenticated with a simple cookie, which we send with every request, along with a bunch of headers.

To get a cookie, we POST a given username and password (of a valid LinkedIn user account) to `https://www.linkedin.com/uas/authenticate`.

### Find new endpoints

We're looking at the LinkedIn website and we spot some data we want. What now?

The following describes the most reliable method to find relevant endpoints:

1. `view source`
1. `command-f`/search the page for some keyword in the data. This will exist inside of a `<code>` tag.
1. Scroll down to the **next adjacent element** which will be another `<code>` tag, probably with an `id` that looks something like

   ```html
   <code style="display: none" id="datalet-bpr-guid-3900675">
     {"request":"/voyager/api/identity/profiles/tom-quirk/profileView","status":200,"body":"bpr-guid-3900675"}
   </code>
   ```

The value of `request` is the url! 🤘

You can also use the `network` tab in you browsers developer tools, but you will encounter mixed results.

### How Clients query Voyager

linkedin.com uses the [Rest-li Protocol](https://linkedin.github.io/rest.li/spec/protocol) for querying data. Rest-li is an internal query language/syntax where clients (like linkedin.com) specify what data they want. It's conceptually similar to the GraphQL.

Here's an example of making a request for an organisation's `name` and `groups` (the Linkedin groups it manages):

```text
/voyager/api/organization/companies?decoration=(name,groups*~(entityUrn,largeLogo,groupName,memberCount,websiteUrl,url))&q=universalName&universalName=linkedin
```

The "querying" happens in the `decoration` parameter, which looks like the following:

```text
(
    name,
    groups*~(entityUrn,largeLogo,groupName,memberCount,websiteUrl,url)
)
```

Here, we request an organisation name and a list of groups, where for each group we want `largeLogo`, `groupName`, and so on.

Different endpoints use different parameters (and perhaps even different syntaxes) to specify these queries. Notice that the above query had a parameter `q` whose value was `universalName`; the query was then specified with the `decoration` parameter.

In contrast, the `/search/cluster` endpoint uses `q=guided`, and specifies its query with the `guided` parameter, whose value is something like

```text
List(v->PEOPLE)
```

It could be possible to document (and implement a nice interface for) this query language - as we add more endpoints to this project, I'm sure it will become more clear if such a thing would be possible (and if it's worth it).

## Updated API Workflow (v2/v3 Methods)

LinkedIn deprecated several legacy Voyager API endpoints (the `/identity/profiles/` family now returns HTTP 410, and `/messaging/conversations` returns HTTP 500). The following documents the updated workflow using the new dash/GraphQL endpoints.

### Prerequisites

```python
from linkedin_api import Linkedin
import requests

# Option 1: Authenticate with credentials
api = Linkedin('your_email@example.com', 'your_password')

# Option 2: Authenticate with cookies (li_at + JSESSIONID from browser)
cookies_dict = {
    'li_at': 'YOUR_LI_AT_COOKIE',
    'JSESSIONID': 'YOUR_JSESSIONID_COOKIE',
}
jar = requests.cookies.RequestsCookieJar()
for key, value in cookies_dict.items():
    jar.set(key, value)

api = Linkedin(
    username='your_email@example.com',
    password='your_password',
    cookies=jar,
)
```

### Step 1: Get Your Mailbox URN

Many messaging methods require your own profile URN ID (`mailbox_urn`). The most reliable way to get it is to resolve your own public ID:

```python
# Recommended: resolve your own public ID to a URN
mailbox_urn = api._resolve_public_id_to_urn("your-public-id")
# Returns e.g. "ACoAABMCK14B..."

# Once you have it, store it — it never changes for a given account.
```

Alternatively, `get_globals()` can retrieve it from the global navigation data, but it relies on a GraphQL `queryId` hash that LinkedIn may rotate at any time:

```python
# Alternative (less reliable — queryId may go stale):
globals_data = api.get_globals()
# Navigate to: data > feedDashGlobalNavs > primaryItems > [...] > meMenu > profile > entityUrn
# Extract the ID after "urn:li:fsd_profile:"
```

### Step 2: Fetch a Profile — `get_profile_v2()`

Replaces the deprecated `get_profile()`. Uses the REST endpoint `/identity/dash/profiles/{urn}?decorationId=...FullProfile-76`.

**Input:**
```python
profile = api.get_profile_v2(public_id="billy-g")
# or
profile = api.get_profile_v2(urn_id="ACoAABMCK14B...")
```

**Output:**
```python
{
    "firstName": "Bill",
    "lastName": "Gates",
    "headline": "Co-chair, Bill & Melinda Gates Foundation",
    "summary": "Co-chair of the Bill & Melinda Gates Foundation...",
    "publicIdentifier": "billy-g",
    "entityUrn": "urn:li:fsd_profile:ACoAABMCK14B...",
    "urn_id": "ACoAABMCK14B...",
    "member_urn": "urn:li:member:12345678",
    "premium": True,
    "locationName": "Seattle, Washington, United States",
    "displayPictureUrl": "https://media.licdn.com/dms/image/...",
    "img_100_100": "...",
    "img_200_200": "...",
    "img_400_400": "...",
    "img_800_800": "...",
    "backgroundPictureUrl": "https://media.licdn.com/dms/image/...",
    "geoLocation": {"geoUrn": "urn:li:geo:12345", "postalCode": "98101"},
    "geoLocationName": "Seattle, Washington",
    "industryName": "Philanthropy",
    "industryUrn": "urn:li:fsd_industry:...",
    "address": None,
    "memorialized": False,
    "versionTag": "..."
}
```

### Step 3: Send a Connection Request — `add_connection()`

Send a personalized connection request. Requires either a `profile_urn` (recommended) or will resolve the public ID to a URN automatically.

**Input:**
```python
# Resolve URN first (recommended to avoid extra HTTP call)
urn_id = api._resolve_public_id_to_urn("billy-g")

# Send connection request
error = api.add_connection(
    profile_public_id="billy-g",
    profile_urn=urn_id,
    message="Hi Bill, I'd love to connect!",  # max 300 chars
)
```

**Output:**
```python
False   # Success (no error)
True    # Failure (error occurred)
```

### Step 4: Fetch Unread Conversations — `get_conversations_v3()`

Fetch conversations with full participant info, last message, and read status. Supports filtering by read/unread and pagination.

**Input:**
```python
result = api.get_conversations_v3(
    mailbox_urn="ACoAABMCK14B...",  # your profile URN ID
    count=20,                        # max 25 per request
    read=False,                      # None=all, False=unread, True=read
)
```

**Output:**
```python
{
    "conversations": [
        {
            "conversation_urn": "urn:li:msg_conversation:(urn:li:fsd_profile:ACoAABMCK14B...,2-YWIzN...==)",
            "thread_id": "2-YWIzN...==",
            "read": False,
            "unread_count": 1,
            "last_activity_at": 1770210328991,   # epoch ms
            "participants": [
                {
                    "urn_id": "ACoAAB6AUv0B...",
                    "firstName": "Sarah",
                    "lastName": "Smith",
                    "headline": "Software Engineer at Google",
                    "profileUrl": "https://www.linkedin.com/in/sarahsmith"
                }
            ],
            "last_message": {
                "text": "Thanks for connecting!",
                "sender_urn_id": "ACoAAB6AUv0B...",
                "is_from_me": False,
                "delivered_at": 1770210328991
            }
        },
        ...
    ],
    "next_cursor": "MCY1"  # pass to next call for pagination, None if no more
}
```

**Pagination:** Loop until `next_cursor` is `None`:
```python
all_conversations = []
cursor = None
while True:
    result = api.get_conversations_v3(
        mailbox_urn=mailbox_urn, count=25, read=False, next_cursor=cursor
    )
    all_conversations.extend(result["conversations"])
    cursor = result["next_cursor"]
    if not cursor:
        break
```

### Step 5: Read a Conversation Thread — `get_thread_v2()`

Fetch the full message history for a conversation.

**Input:**
```python
# Use thread_id from get_conversations_v3()
thread = api.get_thread_v2(
    mailbox_urn="ACoAABMCK14B...",         # your profile URN ID
    messaging_thread_urn="2-YWIzN...==",   # thread_id from conversation
)
```

**Output:**
```python
{
    "data": {
        "messengerMessagesBySyncToken": {
            "elements": [
                {
                    "body": {"text": "Thanks for connecting!"},
                    "sender": {
                        "hostIdentityUrn": "urn:li:fsd_profile:ACoAAB6AUv0B..."
                    },
                    "deliveredAt": 1770210328991,
                    ...
                },
                ...
            ],
            ...
        }
    }
}
```

**Accessing messages:**
```python
messages = thread["data"]["messengerMessagesBySyncToken"]["elements"]
for msg in messages:
    sender = msg["sender"]["hostIdentityUrn"]
    text = msg["body"]["text"]
    print(f"{sender}: {text}")
```

### Step 6: Send a Reply — `send_message_v2()`

Send a message to an existing conversation.

**Input:**
```python
error = api.send_message_v2(
    message_body="Happy to connect! How are you?",
    mailbox_urn="ACoAABMCK14B...",  # your profile URN ID
    conversation_urn="urn:li:msg_conversation:(urn:li:fsd_profile:ACoAABMCK14B...,2-YWIzN...==)",
    # use conversation_urn from get_conversations_v3()
)
```

**Output:**
```python
False   # Success (no error)
True    # Failure (error occurred)
```

### Step 7: Mark as Read — `mark_conversation_as_read_v2()`

Mark a conversation as read after processing it.

**Input:**
```python
error = api.mark_conversation_as_read_v2(
    conversation_urn="urn:li:msg_conversation:(urn:li:fsd_profile:ACoAABMCK14B...,2-YWIzN...==)",
)
```

**Output:**
```python
False   # Success (no error)
True    # Failure (error occurred)
```

### Complete End-to-End Example

This example fetches unread conversations, reads the thread, sends a reply, and marks the conversation as read:

```python
from linkedin_api import Linkedin
import requests

# Authenticate
cookies_dict = {'li_at': 'YOUR_LI_AT', 'JSESSIONID': 'YOUR_JSESSIONID'}
jar = requests.cookies.RequestsCookieJar()
for k, v in cookies_dict.items():
    jar.set(k, v)
api = Linkedin('email@example.com', 'password', cookies=jar)

# Your mailbox URN ID (from get_globals() or your profile)
mailbox_urn = "ACoAABMCK14B..."

# 1. Fetch unread conversations
result = api.get_conversations_v3(mailbox_urn=mailbox_urn, count=10, read=False)

for conv in result["conversations"]:
    names = ", ".join(p["firstName"] + " " + p["lastName"] for p in conv["participants"])
    print(f"Conversation with {names} (unread: {conv['unread_count']})")
    print(f"  Last message: {conv['last_message']['text'][:80]}")

    # 2. Read the full thread
    thread = api.get_thread_v2(
        mailbox_urn=mailbox_urn,
        messaging_thread_urn=conv["thread_id"],
    )
    messages = thread["data"]["messengerMessagesBySyncToken"]["elements"]
    for msg in messages:
        print(f"  > {msg['body']['text'][:100]}")

    # 3. Send a reply
    first_name = conv["participants"][0]["firstName"]
    error = api.send_message_v2(
        message_body=f"Hey {first_name}, thanks for reaching out!",
        mailbox_urn=mailbox_urn,
        conversation_urn=conv["conversation_urn"],
    )
    if not error:
        print("  Reply sent!")

    # 4. Mark as read
    api.mark_conversation_as_read_v2(conversation_urn=conv["conversation_urn"])
```

### Deprecated Methods

The following methods are **broken** and should not be used:

| Method | Issue | Replacement |
|--------|-------|-------------|
| `get_profile()` | `/identity/profiles/` returns HTTP 410 | `get_profile_v2()` |
| `send_message()` | `/messaging/conversations` returns HTTP 500 | `send_message_v2()` |
| `get_conversation_details()` | Legacy response format changed | `get_conversations_v3()` |
| `get_profile_contact_info()` | Uses dead `/identity/profiles/` | No replacement yet |
| `get_profile_skills()` | Uses dead `/identity/profiles/` | No replacement yet |
| `get_profile_network_info()` | Uses dead `/identity/profiles/` | No replacement yet |
| `remove_connection()` | Uses dead `/identity/profiles/` | No replacement yet |

### Release a new version

1. Bump `version` in `pyproject.toml`
1. `poetry build`
1. `poetry publish -r test-pypi`
1. `poetry publish`
1. Draft release notes in GitHub.

## Disclaimer

This library is not endorsed or supported by LinkedIn. It is an unofficial library intended for educational purposes and personal use only. By using this library, you agree to not hold the author or contributors responsible for any consequences resulting from its usage.
