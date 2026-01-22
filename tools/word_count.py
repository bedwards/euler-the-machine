#!/usr/bin/env python3
"""Calculate word count and estimated reading time for markdown files."""

import sys
import re
from pathlib import Path

def count_words(text):
    """Count words in text, excluding markdown syntax."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove image/link syntax
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[[^\]]*\]\([^)]*\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove markdown headers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove emphasis markers
    text = re.sub(r'[*_]{1,2}', '', text)
    # Count words
    words = text.split()
    return len(words)

def estimate_reading_time(word_count, wpm=200):
    """Estimate reading time assuming average reading speed."""
    minutes = word_count / wpm
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    return hours, remaining_minutes, minutes

def main():
    if len(sys.argv) < 2:
        print("Usage: python word_count.py <file_or_directory>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        files = [path]
    else:
        files = list(path.glob('**/*.md')) + list(path.glob('**/*.html'))

    total_words = 0

    for f in files:
        with open(f) as fp:
            text = fp.read()
        words = count_words(text)
        total_words += words
        print(f"{f}: {words:,} words")

    print()
    print(f"{'='*50}")
    print(f"Total words: {total_words:,}")

    hours, minutes, total_minutes = estimate_reading_time(total_words)

    if hours > 0:
        print(f"Estimated reading time: {hours} hour(s) {minutes} minutes")
    else:
        print(f"Estimated reading time: {minutes} minutes")

    print(f"(Based on 200 words per minute average reading speed)")

    # Return structured data for programmatic use
    return {
        'total_words': total_words,
        'hours': hours,
        'minutes': minutes,
        'total_minutes': total_minutes
    }

if __name__ == '__main__':
    main()
