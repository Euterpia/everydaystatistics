#!/usr/bin/env python3
"""
Push all 44 email steps into the MailerLite automation.

Prerequisites:
  - hello@everydaystatistics.com must be verified as a sender in MailerLite
  - Run generate_emails.py first to create the email-drafts/ folder

Usage:
  python3 tools/push_to_mailerlite.py

The script creates each step in sequence with a 24-hour delay node between them.
It is safe to re-run: it checks for existing steps first and skips if already populated.
"""

import os
import json
import time
import urllib.request
import urllib.error

# ── Config ───────────────────────────────────────────────────────────────────

API_KEY_FILE = os.path.expanduser(
    '~/Coworkspace/20 Areas/Every Day Statistics/2W-Tools/MailerLite API Key.md'
)
AUTOMATION_ID = "185022919802357238"
FROM_EMAIL    = "hello@everydaystatistics.com"
FROM_NAME     = "Everyday Statistics"
REPLY_TO      = "hello@everydaystatistics.com"

# Sequence: (html_file_stem, day_number, subject_line)
SEQUENCE = [
    ("day-01-0-1",  1,  "Day 1 of 44 — Why 'a billion pounds' means almost nothing"),
    ("day-02-0-2",  2,  "Day 2 of 44 — The percentage trick politicians use daily"),
    ("day-03-0-3",  3,  "Day 3 of 44 — The word 'average' is probably lying to you"),
    ("day-04-0-4",  4,  "Day 4 of 44 — How to spot a doctored graph in three seconds"),
    ("day-05-0-5",  5,  "Day 5 of 44 — Why your gut feeling about risk is wrong by design"),
    ("day-06-1-1",  6,  "Day 6 of 44 — Two definitions of probability, both in use, rarely distinguished"),
    ("day-07-1-2",  7,  "Day 7 of 44 — Why your brain sees patterns that aren't there"),
    ("day-08-1-3",  8,  "Day 8 of 44 — The four rules that govern every probability claim"),
    ("day-09-1-4",  9,  "Day 9 of 44 — The error that has sent innocent people to prison"),
    ("day-10-1-5", 10,  "Day 10 of 44 — The number behind every lottery ticket, bet, and policy"),
    ("day-11-1-6", 11,  "Day 11 of 44 — Two identical averages, completely different realities"),
    ("day-12-1-7", 12,  "Day 12 of 44 — Why a 99% accurate test is probably wrong"),
    ("day-13-2-1", 13,  "Day 13 of 44 — Beyond mean and median: the full descriptive toolkit"),
    ("day-14-2-2", 14,  "Day 14 of 44 — The bell curve that contributed to the 2008 financial crisis"),
    ("day-15-2-3", 15,  "Day 15 of 44 — What happens when the real world isn't bell-shaped"),
    ("day-16-2-4", 16,  "Day 16 of 44 — How a survey of two million people got it catastrophically wrong"),
    ("day-17-2-5", 17,  "Day 17 of 44 — Why a thousand people can speak for sixty million"),
    ("day-18-2-6", 18,  "Day 18 of 44 — Almost everyone misreads uncertainty bands — including scientists"),
    ("day-19-2-7", 19,  "Day 19 of 44 — The most abused number in science"),
    ("day-20-2-8", 20,  "Day 20 of 44 — Two ways a statistical test can fail — and who gets to choose"),
    ("day-21-2-9", 21,  "Day 21 of 44 — The trick that inflates false discoveries without anyone technically cheating"),
    ("day-22-2-10",22,  "Day 22 of 44 — Two frameworks that answer completely different questions"),
    ("day-23-2-11",23,  "Day 23 of 44 — Half of published psychology research doesn't replicate"),
    ("day-24-3-1", 24,  "Day 24 of 44 — The trick behind every pharmaceutical advertisement ever written"),
    ("day-25-3-2", 25,  "Day 25 of 44 — How to choose the data that proves anything"),
    ("day-26-3-3", 26,  "Day 26 of 44 — The comprehensive guide to the doctored graph"),
    ("day-27-3-4", 27,  "Day 27 of 44 — We only see the planes that came back"),
    ("day-28-3-5", 28,  "Day 28 of 44 — Why punishment appears to work and praise appears not to"),
    ("day-29-3-6", 29,  "Day 29 of 44 — Who isn't in this study, and why that matters"),
    ("day-30-3-7", 30,  "Day 30 of 44 — The error in every second headline"),
    ("day-31-3-8", 31,  "Day 31 of 44 — When group statistics don't apply to individuals"),
    ("day-32-3-9", 32,  "Day 32 of 44 — The statistical error at the heart of wrongful convictions"),
    ("day-33-3-10",33,  "Day 33 of 44 — How to manufacture 'statistically significant' results without lying"),
    ("day-34-3-11",34,  "Day 34 of 44 — The studies that vanish before you see them"),
    ("day-35-3-12",35,  "Day 35 of 44 — The complete toolkit for reading any risk claim"),
    ("day-36-4-1", 36,  "Day 36 of 44 — Why terrorism feels more dangerous than diabetes"),
    ("day-37-4-2", 37,  "Day 37 of 44 — The error that makes rare events feel common"),
    ("day-38-4-3", 38,  "Day 38 of 44 — When adding detail makes something feel more probable"),
    ("day-39-4-4", 39,  "Day 39 of 44 — Why 'due a win' is always wrong"),
    ("day-40-4-5", 40,  "Day 40 of 44 — The hot hand — and why it's more complicated than you think"),
    ("day-41-4-6", 41,  "Day 41 of 44 — The irrelevant number that changes every number that follows"),
    ("day-42-4-7", 42,  "Day 42 of 44 — Why experts are confidently wrong — and how to calibrate yourself"),
    ("day-43-4-8", 43,  "Day 43 of 44 — The heuristic that makes stereotypes feel like statistics"),
    ("day-44-4-9", 44,  "Day 44 of 44 — The calibrated mind: everything assembled"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_api_key():
    with open(API_KEY_FILE, 'r') as f:
        return f.read().strip()


def api_call(method, path, payload=None, api_key=None):
    url = f"https://connect.mailerlite.com/api{path}"
    data = json.dumps(payload).encode('utf-8') if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return json.loads(body)
        except Exception:
            return {'error': body, 'status': e.code}


def create_email_step(automation_id, name, subject, html, api_key):
    """Create an email step in the automation."""
    # Step 1: create the step shell
    result = api_call(
        'POST',
        f'/automations/{automation_id}/steps',
        {'type': 'email'},
        api_key=api_key,
    )
    if 'data' not in result:
        return None, result

    step_id = result['data']['id']

    # Step 2: update with full content
    update = api_call(
        'PUT',
        f'/automations/{automation_id}/steps/{step_id}',
        {
            'data': {
                'name': name,
                'subject': subject,
                'from': FROM_EMAIL,
                'from_name': FROM_NAME,
                'reply_to': REPLY_TO,
                'html': html,
            }
        },
        api_key=api_key,
    )
    return step_id, update


def create_delay_step(automation_id, api_key):
    """Create a 24-hour delay step."""
    result = api_call(
        'POST',
        f'/automations/{automation_id}/steps',
        {
            'type': 'delay',
            'data': {
                'amount': 1,
                'unit': 'day',
            }
        },
        api_key=api_key,
    )
    return result.get('data', {}).get('id')


def add_trigger(automation_id, group_id, api_key):
    """Set the automation trigger to 'subscriber joins group'."""
    result = api_call(
        'POST',
        f'/automations/{automation_id}/triggers',
        {
            'type': 'subscriber_added_to_group',
            'data': {
                'group_id': group_id
            }
        },
        api_key=api_key,
    )
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    email_drafts = os.path.join(script_dir, '..', 'email-drafts')

    print("Loading API key...")
    api_key = load_api_key()

    # Check current automation state
    print(f"\nChecking automation {AUTOMATION_ID}...")
    auto_data = api_call('GET', f'/automations/{AUTOMATION_ID}', api_key=api_key)
    emails_count = auto_data.get('data', {}).get('emails_count', 0)
    print(f"Current email steps: {emails_count}")

    if emails_count > 0:
        print(f"Automation already has {emails_count} email steps. Aborting to avoid duplicates.")
        print("Delete existing steps manually in the MailerLite dashboard first.")
        return

    print(f"\nPushing {len(SEQUENCE)} email steps...\n")
    created = 0
    failed = 0

    for i, (file_stem, day, subject) in enumerate(SEQUENCE):
        html_file = os.path.join(email_drafts, f'{file_stem}.html')
        if not os.path.exists(html_file):
            print(f"  Day {day:02d}: HTML file not found — {html_file}")
            failed += 1
            continue

        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()

        name = f"Day {day:02d} of 44"
        step_id, result = create_email_step(AUTOMATION_ID, name, subject, html, api_key)

        if step_id and 'data' in result:
            print(f"  Day {day:02d}: ✓ Step created ({step_id})")
            created += 1
        else:
            print(f"  Day {day:02d}: ✗ Failed — {result.get('message', result)}")
            failed += 1
            if 'must be verified' in str(result.get('message', '')) or 'must be authenticated' in str(result.get('message', '')):
                print("\n  BLOCKED: Sender email not yet verified.")
                print(f"  Go to MailerLite → Settings → Sender Addresses")
                print(f"  Verify: {FROM_EMAIL}")
                print(f"  Then re-run this script.\n")
                break

        # Add delay after every email except the last
        if day < 44:
            delay_id = create_delay_step(AUTOMATION_ID, api_key)
            if delay_id:
                print(f"         + 24h delay added")

        # Small pause to avoid rate limiting
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Done: {created} steps created, {failed} failed.")
    if created == 44:
        print("\nAll 44 steps created successfully.")
        print("Next: add the trigger (subscriber joins 'Everyday Statistics Course' group)")
        print("      and enable the automation in the MailerLite dashboard.")


if __name__ == '__main__':
    main()
