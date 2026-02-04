"""
Voyager API Interceptor — Selenium + Chrome DevTools Protocol network capture tool.

Launches Chrome with your LinkedIn session cookies, captures all voyager API
request URLs/headers via CDP performance logs, then replays profile-related
requests via fetch() to capture response bodies.

Usage:
    python voyager-intercept.py

Requirements:
    pip install selenium
"""

import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---------------------------------------------------------------------------
# LinkedIn session cookies — copy your li_at and JSESSIONID values here.
# These are the same cookies used in linkedin-test.py.
# ---------------------------------------------------------------------------
COOKIES = {
    "li_at": "AQEDARMCK14DI_4WAAABm74VIzQAAAGcLVi1N04AaPpzRrY0iZ4Ja_UdjxhJbzw3mCUzv-pUyJQsThcqoryZxQG8YPrrBA41kCUDMkfUtYjxCRXb-PrPaINAM96q3qcy4bpAxFes-czRm9-WWXY6reHh",
    "JSESSIONID": "ajax:8279155946033820893",
}

OUTPUT_FILE = "voyager-captures.json"

RELEVANT_HEADERS = {
    "accept",
    "content-type",
    "csrf-token",
    "x-restli-protocol-version",
    "x-li-lang",
    "x-li-track",
    "x-li-page-instance",
}

RESPONSE_BODY_LIMIT = 500_000

# Keywords that identify endpoints worth replaying for response body capture
REPLAY_KEYWORDS = [
    "IdentityDashProfiles",
    "identity/dash/profiles",
    "IdentityDashProfileCards",
    "IdentityDashOpenToCards",
    "ProfilePhotoFrames",
    "messengerConversations",
    "MessagingDash",
    "messaging/conversations",
    "messagingThread",
    "messengerMessages",
]


def is_voyager_url(url):
    return "voyager/api" in url or "voyagerGraphQL" in url


def is_replay_url(url):
    return any(kw in url for kw in REPLAY_KEYWORDS)


def filter_headers(headers):
    if not headers or not isinstance(headers, dict):
        return {}
    return {k: v for k, v in headers.items() if k.lower() in RELEVANT_HEADERS}


def replay_url(driver, url, headers):
    """Use fetch() from the page context to re-request a URL and get the body."""
    # Build headers object for fetch, using the captured request headers
    fetch_headers = {}
    for k, v in headers.items():
        fetch_headers[k] = v

    script = """
    const [url, headersObj] = arguments;
    return fetch(url, {
        method: 'GET',
        headers: headersObj,
        credentials: 'include'
    })
    .then(r => r.text().then(body => ({status: r.status, body: body})))
    .catch(e => ({status: -1, body: e.toString()}));
    """
    try:
        result = driver.execute_async_script(
            """
            const [url, headersObj, callback] = [arguments[0], arguments[1], arguments[arguments.length - 1]];
            fetch(url, {
                method: 'GET',
                headers: headersObj,
                credentials: 'include'
            })
            .then(r => r.text().then(body => callback({status: r.status, body: body.substring(0, %d)})))
            .catch(e => callback({status: -1, body: e.toString()}));
            """ % RESPONSE_BODY_LIMIT,
            url,
            fetch_headers,
        )
        return result
    except Exception as e:
        return {"status": -1, "body": str(e)}


def main():
    chrome_options = Options()
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    )
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)

    captures = []
    pending_requests = {}
    pending_responses = {}

    try:
        driver.get("https://www.linkedin.com")
        time.sleep(2)

        driver.add_cookie({
            "name": "li_at",
            "value": COOKIES["li_at"],
            "domain": ".linkedin.com",
            "path": "/",
        })
        driver.add_cookie({
            "name": "JSESSIONID",
            "value": COOKIES["JSESSIONID"],
            "domain": ".linkedin.com",
            "path": "/",
        })

        print("Navigating to linkedin.com/feed ...")
        driver.get("https://www.linkedin.com/feed/")

        print(
            "\nBrowser is open. Navigate to the page you want to capture "
            "(e.g. inbox > filter by Unread, or a profile page).\n"
            "When done browsing, come back here and press ENTER to replay "
            "captured requests and save response bodies. (Do NOT close the browser!)\n"
        )

        # Background: poll performance logs in a thread
        import threading
        stop_event = threading.Event()

        def poll_logs():
            while not stop_event.is_set():
                try:
                    logs = driver.get_log("performance")
                except Exception:
                    break

                for log_entry in logs:
                    try:
                        message = json.loads(log_entry["message"])["message"]
                        method = message["method"]
                        params = message.get("params", {})

                        if method == "Network.requestWillBeSent":
                            request = params.get("request", {})
                            url = request.get("url", "")
                            if is_voyager_url(url):
                                request_id = params.get("requestId")
                                pending_requests[request_id] = {
                                    "timestamp": datetime.now().isoformat(),
                                    "method": request.get("method", "GET"),
                                    "url": url,
                                    "request_headers": filter_headers(
                                        request.get("headers", {})
                                    ),
                                    "request_post_data": request.get("postData"),
                                }

                        elif method == "Network.responseReceived":
                            request_id = params.get("requestId")
                            if request_id in pending_requests:
                                response = params.get("response", {})
                                entry = pending_requests.pop(request_id)
                                entry["response_status"] = response.get("status")
                                entry["response_body"] = None
                                captures.append(entry)

                                url = entry["url"]
                                print(
                                    f"[{entry['method']}] {entry['response_status']} "
                                    f"{url[:120]}{'...' if len(url) > 120 else ''}"
                                )

                    except (json.JSONDecodeError, KeyError):
                        continue

                time.sleep(0.3)

        log_thread = threading.Thread(target=poll_logs, daemon=True)
        log_thread.start()

        # Wait for user to press Enter
        input("\n>>> Press ENTER when done browsing to capture bodies and save...\n")
        stop_event.set()
        log_thread.join(timeout=2)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        if "disconnected" not in str(e).lower() and "no such window" not in str(e).lower():
            print(f"Error: {e}")

    # ------------------------------------------------------------------
    # Phase 2: Replay profile-related GET requests to capture bodies
    # ------------------------------------------------------------------
    profile_captures = [
        c for c in captures
        if c["response_status"] == 200
        and c["method"] == "GET"
        and is_replay_url(c["url"])
    ]

    if profile_captures:
        print(f"\n--- Replaying {len(profile_captures)} requests to capture response bodies ---\n")
        try:
            for entry in profile_captures:
                result = replay_url(driver, entry["url"], entry["request_headers"])
                entry["response_body"] = result.get("body", "<replay failed>")
                replay_status = result.get("status", "?")
                url = entry["url"]
                body_preview = (entry["response_body"] or "")[:150]
                print(
                    f"  [REPLAY] {replay_status} {url[:100]}..."
                )
                print(f"    Body: {body_preview}...")
        except Exception as e:
            print(f"  Replay failed (browser closed?): {e}")

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(captures, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(captures)} captured requests to {OUTPUT_FILE}")

    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
