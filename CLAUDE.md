# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an unofficial LinkedIn API wrapper for Python that uses LinkedIn's internal "Voyager" API endpoints. It allows programmatic access to LinkedIn profiles, connections, messages, jobs, companies, and more without requiring official API credentials. The library authenticates using regular LinkedIn account credentials and mimics browser behavior.

**Important**: This library is not officially supported by LinkedIn and may violate LinkedIn's Terms of Service.

## Development Commands

### Setup
```bash
# Install dependencies (requires poetry)
poetry install

# Install poetry dotenv plugin for environment variable management
poetry self add poetry-plugin-dotenv
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run only unit tests
poetry run pytest tests/unit

# Run only E2E tests (requires valid LinkedIn credentials in .env)
poetry run pytest tests/e2e

# Run a specific test file
poetry run pytest tests/unit/test_linkedin_api.py
```

### Linting
```bash
# Check code formatting
poetry run black --check .

# Fix code formatting
poetry run black .
```

### Configuration
Create a `.env` file based on `.env.example` with valid LinkedIn credentials for testing:
```
LINKEDIN_USERNAME=your_email@example.com
LINKEDIN_PASSWORD=your_password
TEST_PROFILE_ID=<urn_id>
TEST_PUBLIC_PROFILE_ID=<public_id>
TEST_CONVERSATION_ID=<conversation_id>
```

## Architecture

### Core Components

**Client Layer** (`linkedin_api/client.py`):
- `Client` class handles low-level HTTP requests and authentication
- Manages session cookies via `CookieRepository` for persistence
- Implements authentication flow via `/uas/authenticate` endpoint
- Stores metadata about the LinkedIn session (client application instance, page instance ID)
- Configurable user-agent and proxy support

**API Layer** (`linkedin_api/linkedin.py`):
- `Linkedin` class provides high-level API methods
- Each method corresponds to a LinkedIn feature (profiles, connections, messages, jobs, etc.)
- Implements request throttling via `default_evade()` to avoid rate limiting (random 2-5 second delays)
- Handles pagination for endpoints that return large result sets
- Constants define limits: `_MAX_POST_COUNT = 100`, `_MAX_UPDATE_COUNT = 100`, `_MAX_SEARCH_COUNT = 49`, `_MAX_REPEATED_REQUESTS = 200`

**Cookie Management** (`linkedin_api/cookie_repository.py`):
- `CookieRepository` persists authentication cookies to disk using pickle
- Validates cookie expiration via JSESSIONID token
- Raises `LinkedinSessionExpired` when cached cookies are invalid
- Default cookie storage location defined in `settings.COOKIE_PATH`

**Utilities** (`linkedin_api/utils/helpers.py`):
- URN parsing functions (`get_id_from_urn`, `get_urn_from_raw_update`)
- Post/feed parsing helpers for complex nested API responses
- Tracking ID generation for API requests

### LinkedIn Voyager API

LinkedIn's internal API uses the Rest-li protocol with complex query syntax:

**Endpoint Structure**:
```
https://www.linkedin.com/voyager/api/{resource}
```

**URN Format**: LinkedIn uses URNs (Uniform Resource Names) to identify entities:
- Profiles: `urn:li:fs_miniProfile:{id}` or `urn:li:fsd_profile:{id}`
- Companies: `urn:li:company:{id}`
- Messages: `urn:li:msg_conversation:{id}`

**Decoration Parameters**: Use Rest-li "decoration" syntax to specify which fields to fetch:
```
decoration=(name,groups*~(entityUrn,largeLogo,groupName,memberCount))
```

**GraphQL Endpoints**: Some newer endpoints use GraphQL with `queryId` parameters:
```
/graphql?variables=(...)&queryId=voyagerSearchDashClusters.{hash}
```

### Authentication Flow

1. Request initial session cookies from `/uas/authenticate` (GET)
2. Submit credentials to `/uas/authenticate` (POST) with session cookies
3. Receive authenticated cookies including JSESSIONID
4. Extract CSRF token from JSESSIONID and add to headers as `csrf-token`
5. Cache cookies to disk for reuse (unless `refresh_cookies=True`)

### Common Patterns

**ID Resolution**: Most API methods accept either `public_id` (e.g., "billy-g") or `urn_id` (internal ID). When only public_id is provided, use `_resolve_public_id_to_urn()` to resolve to URN (parses the profile HTML page). The old `get_profile()` method used for this is now deprecated.

**Pagination**: Methods that return lists typically:
- Use `start` and `count` parameters
- Loop until no more results or hitting `_MAX_REPEATED_REQUESTS` safety limit
- Accumulate results across requests before returning

**Error Handling**: API responses are checked for `status` field. Non-200 status codes result in logging and returning empty dict/list.

**Evade Detection**: Each request is preceded by `evade()` function call (default: random 2-5 second sleep) to mimic human behavior and avoid rate limiting.

## Key API Methods

### Profile Operations
- `get_profile(public_id=None, urn_id=None)` - **DEPRECATED** (returns `{}`, endpoint is HTTP 410)
- `get_profile_v2(public_id=None, urn_id=None)` - Full profile data via `/identity/dash/profiles/` REST endpoint
- `_resolve_public_id_to_urn(public_id)` - Resolve public ID to URN via HTML page parsing
- `get_profile_contact_info()` - **BROKEN** (uses deprecated `/identity/profiles/` endpoint)
- `get_profile_skills()` - **BROKEN** (uses deprecated `/identity/profiles/` endpoint)
- `get_profile_network_info()` - **BROKEN** (uses deprecated `/identity/profiles/` endpoint)
- `get_profile_connections(urn_id)` - 1st degree connections (working, wraps `search_people`)
- `get_profile_experiences(urn_id)` - Work history (working, uses GraphQL endpoint)

### Search Operations
- `search(params, limit, offset)` - Generic search (all entity types)
- `search_people()` - People search with extensive filters (company, school, location, etc.)
- `search_companies()` - Company search
- `search_jobs()` - Job search with filters (experience, type, location, remote, etc.)

### Messaging Operations
- `get_conversations()` - List conversations (legacy REST endpoint, working)
- `get_conversations_v2()` - List conversations (GraphQL, working but limited — no unread filter, no embedded messages)
- `get_conversations_v3(mailbox_urn, read=None, ...)` - **RECOMMENDED** — List conversations with embedded messages, participant info, unread filter (`read=False`), pagination via `nextCursor`. Max count per request: 25. Response under `messengerConversationsBySearchCriteria`.
- `get_conversation()` - Get messages in conversation (legacy REST, working)
- `get_thread_v2(mailbox_urn, messaging_thread_urn)` - Get messages in thread (GraphQL, working). Response under `messengerMessagesBySyncToken`.
- `send_message()` - **BROKEN** (legacy `/messaging/conversations` endpoints return 500)
- `send_message_v2(message_body, mailbox_urn, conversation_urn)` - **RECOMMENDED** — Send message via `/voyagerMessagingDashMessengerMessages?action=createMessage`. Uses full conversation URN from `get_conversations_v3()`.
- `mark_conversation_as_seen()` - Mark as seen (legacy, may be broken)
- `mark_conversation_as_read_v2(conversation_urn)` - **RECOMMENDED** — Mark conversation as read via `/voyagerMessagingDashMessengerConversations` PATCH endpoint.

### Connection Operations
- `add_connection(profile_public_id, message="", profile_urn=None)` - Send connection request (working — uses `_resolve_public_id_to_urn` for URN resolution)
- `remove_connection(public_profile_id)` - **BROKEN** (uses deprecated `/identity/profiles/` endpoint)
- `get_invitations()` - Fetch pending invitations
- `reply_invitation(urn, secret, action="accept")` - Accept/reject invitation

### Post/Feed Operations
- `get_profile_posts()` - Posts from a profile
- `get_post_comments()` - Comments on a post
- `get_feed_posts()` - User's feed posts sorted by recent
- `react_to_post(post_urn_id, reaction_type="LIKE")` - React to post

### Company Operations
- `get_company(public_id)` - Company data
- `get_company_updates()` - Company posts/news
- `follow_company()` - Follow/unfollow company

## Important Notes

### Rate Limiting & Challenges
- LinkedIn may present a CHALLENGE if suspicious activity is detected
- Known triggers: 2FA, rate limiting (>900 requests/hour observed), new IP addresses
- The library does NOT handle challenges - manual browser login/logout may be required
- Conservative `_MAX_REPEATED_REQUESTS = 200` limit helps avoid triggering challenges

### API Versioning
LinkedIn has multiple API versions in use:
- **Dead**: `/identity/profiles/` REST endpoints — return HTTP 410 (Gone)
- **Dead/Broken**: `/messaging/conversations` REST endpoints — return HTTP 500 (send) or changed response format (read)
- **Working (legacy REST)**: `/identity/dash/profiles/` — used by `get_profile_v2()`
- **Working (new dash REST)**: `/voyagerMessagingDashMessengerMessages`, `/voyagerMessagingDashMessengerConversations` — used by `send_message_v2()`, `mark_conversation_as_read_v2()`
- **Working (GraphQL)**: `/voyagerMessagingGraphQL/graphql` with `queryId` — used by `get_conversations_v3()`, `get_thread_v2()`
- **Working (GraphQL)**: `/graphql` with `queryId` — used by `get_profile_experiences()`

When adding new endpoints, use `voyager-intercept.py` to discover the current API calls LinkedIn makes in the browser.

### Search Limitations
- General keyword searches may return grouped results (people, companies, jobs mixed)
- Prefer entity-specific search methods (`search_people`, `search_companies`, `search_jobs`)
- Max search count appears to be 49 results per request (`_MAX_SEARCH_COUNT`)

### Finding New Endpoints
To discover new Voyager endpoints:
1. Open LinkedIn in browser, view source
2. Search for relevant keyword in page source
3. Look for adjacent `<code>` tag with structure: `{"request":"/voyager/api/...","status":200}`
4. Alternatively, use browser DevTools Network tab (less reliable due to async loading)
5. Use `voyager-intercept.py` (Selenium + CDP) — see "In-Progress Work" section below

## In-Progress Work

### `get_profile()` Deprecation (DONE)
- **Status**: Completed
- `get_profile()` in `linkedin_api/linkedin.py` (line ~824) is now deprecated
- It emits a `DeprecationWarning` and logs a warning, then returns `{}`
- All the old dead code that parsed `data["profile"]`, `data["positionView"]`, etc. has been removed
- The `/identity/profiles/` endpoint family returns HTTP 410 (Gone)
- Callers should use `_resolve_public_id_to_urn()` for URN resolution and specific methods like `get_profile_experiences()`, `get_profile_skills()`, `get_profile_contact_info()` for data

### `voyager-intercept.py` — Browser Network Interceptor (DONE)
- **Status**: Completed — both URL/header capture and response body capture work
- **File**: `voyager-intercept.py` in project root
- Uses Selenium 4.36 + Chrome DevTools Protocol (CDP) performance logs
- Launches Chrome with `li_at`/`JSESSIONID` cookies, opens DevTools, navigates to LinkedIn
- Captures all `voyager/api` and `voyagerGraphQL` network requests
- **Two-phase approach**:
  - Phase 1: Poll performance logs in a background thread to capture URLs/headers/status
  - Phase 2: After user presses ENTER, replay profile-related GET URLs via `fetch()` from the page context to capture response bodies
- Successfully captured 6 response bodies (up to 111KB) including REST and GraphQL profile endpoints
- `RESPONSE_BODY_LIMIT` set to 500,000 characters

### `get_profile_v2()` Implementation (DONE)
- **Status**: Completed and tested
- **Method**: `get_profile_v2(public_id=None, urn_id=None)` in `linkedin_api/linkedin.py`
- Uses the REST endpoint `/identity/dash/profiles/{urn}?decorationId=com.linkedin.voyager.dash.deco.identity.profile.FullProfile-76`
- Requires `accept: application/vnd.linkedin.normalized+json+2.1` header
- Accepts `public_id` or `urn_id`; resolves public_id via `_resolve_public_id_to_urn()` if needed
- Returns a clean dict with: `firstName`, `lastName`, `headline`, `summary`, `publicIdentifier`, `entityUrn`, `urn_id`, `member_urn`, `displayPictureUrl`, `img_*` variants, `backgroundPictureUrl`, `geoLocation`, `geoLocationName`, `location`, `industryName`, `industryUrn`, `premium`, `memorialized`, `versionTag`
- Tested successfully with multiple profiles (own profile + third-party)

### `get_conversations_v3()` Implementation (DONE)
- **Status**: Completed and tested
- **Method**: `get_conversations_v3(mailbox_urn, count=20, next_cursor=None, read=None, categories=None, first_degree_connections=False)`
- Uses `voyagerMessagingGraphQL/graphql` with queryId `messengerConversations.737b27144cf922499202658a5345016f`
- **Max count per request**: 25 (API rejects higher values)
- **Unread filter**: `read=False` for unread only, `read=True` for read only, `None` for all
- Response key: `messengerConversationsBySearchCriteria` (unwrapped automatically)
- Each conversation includes: `messages.elements` (last message with body text), `conversationParticipants` (with `hostIdentityUrn`), `read`, `unreadCount`, `entityUrn`, `backendUrn`
- Participant `preview` (names) comes back as `None` from direct API calls — use `hostIdentityUrn` to resolve via `get_profile_v2()` if needed
- Pagination via `nextCursor` in `metadata`
- Tested: paginated through 450+ unread conversations across 18 pages

### `send_message_v2()` Implementation (DONE)
- **Status**: Completed and tested
- **Method**: `send_message_v2(message_body, mailbox_urn, conversation_urn)`
- Uses `POST /voyagerMessagingDashMessengerMessages?action=createMessage`
- `conversation_urn` is the full `entityUrn` from `get_conversations_v3()` (e.g. `urn:li:msg_conversation:(urn:li:fsd_profile:xxx,2-yyy==)`)
- Headers: `accept: application/json`, `Content-Type: text/plain;charset=UTF-8`
- Returns `False` on success, `True` on error

### `mark_conversation_as_read_v2()` Implementation (DONE)
- **Status**: Completed and tested
- **Method**: `mark_conversation_as_read_v2(conversation_urn)`
- Uses `POST /voyagerMessagingDashMessengerConversations?ids=List({encoded_urn})`
- Payload: `{"entities": {conversation_urn: {"patch": {"$set": {"read": true}}}}}`
- Returns `False` on success, `True` on error

### `add_connection()` Fix (DONE)
- **Status**: Completed
- Previously called deprecated `get_profile()` for URN resolution when `profile_urn` was not provided
- Now uses `_resolve_public_id_to_urn()` instead

### Full Messaging Workflow (VERIFIED)
The following end-to-end workflow has been tested and works:
```python
# 1. Get unread conversations
convos = linkedin.get_conversations_v3(mailbox_urn=my_urn, read=False)
# 2. Pick a conversation, get thread
conv = convos['elements'][2]
conv_urn = conv['entityUrn']
thread_id = conv['backendUrn'].replace('urn:li:messagingThread:', '')
thread = linkedin.get_thread_v2(mailbox_urn=my_urn, messaging_thread_urn=thread_id)
# 3. Reply
linkedin.send_message_v2('Happy to connect!', mailbox_urn=my_urn, conversation_urn=conv_urn)
# 4. Mark as read
linkedin.mark_conversation_as_read_v2(conversation_urn=conv_urn)
```

### Discovered Messaging Endpoints (from captures)
- **Send message**: `POST /voyagerMessagingDashMessengerMessages?action=createMessage`
- **Mark as read**: `POST /voyagerMessagingDashMessengerConversations?ids=List({urn})` with PATCH payload
- **Mark all seen**: `POST /voyagerMessagingDashMessagingBadge?action=markAllMessagesAsSeen`
- **Delivery ack**: `POST /voyagerMessagingDashMessengerMessageDeliveryAcknowledgements?action=sendDeliveryAcknowledgement`
- **Presence**: `POST /messaging/dash/presenceStatuses`
- **List conversations (unread)**: `voyagerMessagingGraphQL/graphql?queryId=messengerConversations.737b27...` with `read:false`
- **List conversations (initial)**: `voyagerMessagingGraphQL/graphql?queryId=messengerConversations.0d5e67...` (sync token based)
- **Get messages**: `voyagerMessagingGraphQL/graphql?queryId=messengerMessages.5846ee...`

### Discovered Profile Endpoints (from captures)

When visiting a profile page, LinkedIn makes these voyager API calls:

**By vanityName (public ID) — GraphQL `voyagerIdentityDashProfiles`:**
| queryId hash | Notes |
|---|---|
| `.34ead06db82a2cc9a778fac97f69ad6a` | Primary profile data (called with and without `includeWebMetadata`) |
| `.a1a483e719b20537a256b6853cdca711` | Secondary profile data |
| `.2ca312bdbe80fac72fd663a3e06a83e7` | Additional profile data (with `includeWebMetadata`) |

**By profileUrn — GraphQL `voyagerIdentityDashProfiles`:**
| queryId hash | Notes |
|---|---|
| `.81ad6d6680eb4b25257eab8e73b7189b` | Profile by URN (visited profile) |
| `.7bab95a76318a84301169b923d563eb1` | Profile by URN (own profile) |
| `.da93c92bffce3da586a992376e42a305` | Profile by URN (own profile, with `includeWebMetadata`) |

**REST endpoint (still alive!):**
- `/identity/dash/profiles/{urn}?decorationId=com.linkedin.voyager.dash.deco.identity.profile.FullProfile-76`
- Note: this is `/identity/dash/profiles/` (NOT `/identity/profiles/` which is dead)

**Profile extras:**
- `voyagerIdentityDashProfileCards` — two different queryId hashes
- `voyagerIdentityDashOpenToCards` — open-to-work info
- `voyagerIdentityDashProfilePhotoFrames` — photo frames
- `voyagerLearningDashLearningRecommendations` — learning recs (uses `vieweeId` param)

**Key observations:**
- All GraphQL profile endpoints use `accept: application/vnd.linkedin.normalized+json+2.1`
- CSRF token comes from JSESSIONID cookie (e.g., `csrf-token: ajax:8279155946033820893`)
- `x-restli-protocol-version: 2.0.0` is always sent
- `x-li-page-instance` changes per page view (format: `urn:li:page:d_flagship3_profile_view_base;{base64}`)
- `x-li-track` contains client metadata JSON (version, OS, display info)

### Environment Notes
- Python 3.9 (at `C:\Users\Daniel\AppData\Local\Programs\Python\Python39`)
- `pyproject.toml` says `python = "^3.10"` — mismatch, but everything works
- Selenium 4.36 installed globally (not via poetry)
- Playwright is installed but browsers are NOT downloaded (`playwright install chromium` was never run)
- OS: Windows (paths use backslashes)
