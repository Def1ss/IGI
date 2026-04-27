"""
Task 2: Text analysis with regex
"""

import re
import zipfile


def analyze_text(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Split into words
    words = re.findall(r'\b\w+\b', text.lower())

    # Sentence types
    decl = inter = imper = 0
    for s in sentences:
        if s.endswith('?'):
            inter += 1
        elif s.endswith('!'):
            imper += 1
        else:
            decl += 1

    # Average lengths
    avg_sent_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0

    # Smileys
    smileys = re.findall(r'[:;][-]*[\(\)\[\]]+', text)

    # Emails with names
    emails = re.findall(r'([A-Za-z\s]+)[\s<]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)

    # Replace $v_(i)$ -> v[i] (i is single digit or letter)
    replaced = re.sub(r'\$v_\(([a-zA-Z0-9])\)\$', r'v[\1]', text)

    # Words with odd length
    odd_words = [w for w in words if len(w) % 2 == 1]

    # Shortest word starting with i
    i_words = [w for w in words if w.startswith('i')]
    shortest_i = min(i_words, key=len) if i_words else ""

    # Duplicate words (without Counter)
    word_counts = {}
    for w in words:
        word_counts[w] = word_counts.get(w, 0) + 1
    dups = {w: c for w, c in word_counts.items() if c > 1}

    return {
        "total_sentences": len(sentences),
        "declarative": decl,
        "interrogative": inter,
        "imperative": imper,
        "avg_sentence_len": round(avg_sent_len, 2),
        "avg_word_len": round(avg_word_len, 2),
        "smileys": smileys,
        "emails": emails,
        "replaced_text": replaced,
        "odd_words_count": len(odd_words),
        "odd_words": odd_words[:10],
        "shortest_i_word": shortest_i,
        "duplicate_words": dups,
    }


def run():
    print("\n=== TASK 2: TEXT ANALYSIS ===")

    sample = """Hello! This is a sample text. Do you like it? I hope so :)
    Here is email: John Doe <john@example.com>. Replace $v_(1)$ and $v_(a)$.
    Interesting interesting! Word appears twice. Hello hello world."""

    print("Sample text:")
    print(sample)

    results = analyze_text(sample)

    print("\nResults:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    # Save to file and zip
    with open("analysis_result.txt", "w", encoding="utf-8") as f:
        for k, v in results.items():
            f.write(f"{k}: {v}\n")

    with zipfile.ZipFile("result.zip", "w") as z:
        z.write("analysis_result.txt")

    print("\nSaved to analysis_result.txt and zipped to result.zip")