Viral Username Generator

This script uses AI to automatically generate, filter, score, and check the availability of trendy usernames—ideal for Telegram handles, meme accounts, or personal projects.
Features

    Generates unique, meme-inspired usernames using OpenAI’s GPT-4o

    Filters out meaningless or random combinations

    Scores usernames based on virality (1–100 scale)

    Checks availability on:

 Telegram (https://t.me/username)

 Fragment (https://fragment.com/username/)

Setup

Clone the repository:

    git clone https://github.com/yourusername/viral-username-generator.git
    cd viral-username-generator

Install dependencies:

    pip install -r requirements.txt

Add your OpenAI API key:
Open the script and replace this line:

    OPENAI_API_KEY = "YOUR_API_KEY"

Usage

Run the script:

python parsnew.py

It will generate, filter, score, and display available usernames that pass the virality threshold.
Known Issue

Some usernames may appear as "banned" even though they are technically available.
This is a known bug — a fix is coming soon.
Sample Output

Generating usernames...
Filtering for meaningful usernames...
Evaluating virality scores...
19 usernames passed virality threshold ≥ 50
Checking availability 1/19: memeszn
...
Found 6 available usernames:
@memeszn
@vibecore
@cringify
...

Dependencies

    openai

    requests

    beautifulsoup4

These can be installed with pip or from the included requirements.txt.
AI Usage

The script uses OpenAI’s gpt-4o-mini model with adjusted temperature settings:

    Generation: temperature=0.8

    Filtering and scoring: temperature=0.0
