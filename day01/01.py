"""Solve challenge 1"""
import requests

# Whoops! Looks like input is user-specific
r = requests.get("https://adventofcode.com/2022/day/1/input")
r.content[:100]
r.status_code  # 400 error

# No matter, use a requests Session
# session cookie was easy to find in Firefox network tools
ses = requests.Session()
ses.cookies.set("session", "536xxxx")  # Redacted
r = ses.get("https://adventofcode.com/2022/day/1/input")

# Look at the data
r.content[:100]
r.text[:100]
len(r.text)

# Hmm, let's do this the laziest way possible

max_seen = 0
# `[:-1]` at the end handles the trailing newline, there's
# a better way to do this, but this was fast
for ix, chunk in enumerate(r.text.split("\n\n")[:-1]):
    cal = sum(map(int, chunk.split("\n")))
    if cal > max_seen:
        max_seen = cal
        max_ix = ix

print(f"{max_ix}: {max_seen}")
