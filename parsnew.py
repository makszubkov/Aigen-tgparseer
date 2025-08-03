import time
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# === SETTINGS ===
OPENAI_API_KEY = "YOUR_API_KEY"  # ← INSERT YOUR OpenAI KEY HERE
TOTAL_TO_GENERATE = 50
VIRALITY_THRESHOLD = 50
MAX_USERNAME_LENGTH = 9

client_ai = OpenAI(api_key=OPENAI_API_KEY)

def generate_usernames_ai(count):
    prompt = (
        f"Generate {count} unique, trendy, and meme-inspired usernames. "
        "Use only lowercase Latin letters, no digits or symbols. Length: 5 to 9 characters. "
        "Return as a comma-separated list only. No numbers or special characters."
    )

    result = []
    seen = set()
    while len(result) < count:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a username generator inspired by internet trends and memes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        text = response.choices[0].message.content
        new_names = [re.sub(r'[^a-z]', '', name.strip().lower()) for name in text.split(",")]
        filtered = [u for u in new_names if 5 <= len(u) <= MAX_USERNAME_LENGTH and u not in seen]
        result.extend(filtered)
        seen.update(filtered)
    return result[:count]

def filter_meaningful(usernames):
    prompt = (
        "From the following list of usernames, select only the ones that are meaningful, "
        "sound like real words, slang, or internet terms. Exclude any gibberish or random combinations.\n\n"
        + "\n".join(usernames) +
        "\n\nReturn only the valid usernames as a comma-separated list. No extra commentary."
    )

    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in language and internet culture."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    text = response.choices[0].message.content
    clean = [re.sub(r'[^a-z]', '', name.strip().lower()) for name in text.split(",")]
    return [u for u in clean if u in usernames]

def evaluate_virality(usernames):
    prompt = (
        "Rate the virality of each username below from 1 to 100, based on how catchy, trendy, or meme-friendly it is.\n"
        "Format: username - score (only integers)\n\n"
        + "\n".join(usernames)
    )

    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a trend expert specializing in viral content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    scores = {}
    for line in response.choices[0].message.content.splitlines():
        parts = line.split("-")
        if len(parts) == 2:
            name = parts[0].strip().lower()
            try:
                score = int(parts[1].strip())
                scores[name] = score
            except:
                continue
    return scores

def check_availability(username):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Check Telegram
    try:
        tg_resp = requests.get(f"https://t.me/{username}", headers=headers, timeout=10)
        if "If you have Telegram, you can contact" in tg_resp.text:
            return False
    except Exception as e:
        print(f"[Telegram error] {username}: {e}")
        return False

    # Check Fragment
    try:
        fr_resp = requests.get(f"https://fragment.com/username/{username}", headers=headers, timeout=10)
        if "unavailable" not in fr_resp.text.lower():
            return False
    except Exception as e:
        print(f"[Fragment error] {username}: {e}")
        return False

    return True

def main():
    print("🔍 Generating usernames...")
    raw_usernames = generate_usernames_ai(TOTAL_TO_GENERATE)

    print("🧠 Filtering for meaningful usernames...")
    meaningful = filter_meaningful(raw_usernames)

    print("📊 Evaluating virality scores...")
    scores = evaluate_virality(meaningful)

    filtered = [name for name in meaningful if scores.get(name, 0) >= VIRALITY_THRESHOLD]

    print(f"✅ {len(filtered)} usernames passed virality threshold ≥ {VIRALITY_THRESHOLD}")

    available = []
    for i, name in enumerate(filtered, 1):
        print(f"🔎 Checking availability {i}/{len(filtered)}: {name}")
        if check_availability(name):
            available.append(name)
        time.sleep(1)

    print(f"\n🎉 Found {len(available)} available usernames:")
    for u in available:
        print(f"@{u}")

if __name__ == "__main__":
    main()
