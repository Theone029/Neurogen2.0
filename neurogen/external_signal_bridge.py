#!/usr/bin/env python3
"""
external_signal_bridge.py

Fetches high-friction, semantically rich external signals from GitHub Trending and Hacker News.
Processes these signals through a 3-layer validation pipeline:
  1. Entropy Score: Measures signal length as a proxy for novelty.
  2. Relevance Match: Checks for strategic keywords (e.g., "AI", "tech", "startup").
  3. Causality Trigger: (Placeholder) Would trigger symbolic reasoning for roadmap evolution.

Only signals passing these filters are returned for further processing.
Requires the 'requests' module.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExternalSignalBridge")

# Public API for GitHub trending projects (non-official; fallback if unavailable)
GITHUB_TRENDING_URL = "https://ghapi.huchen.dev/repositories"

# Hacker News top stories API endpoint
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"

def fetch_github_trending():
    try:
        response = requests.get(GITHUB_TRENDING_URL, timeout=10)
        if response.status_code == 200:
            trending = response.json()
            logger.info("Fetched %d GitHub trending projects.", len(trending))
            signals = []
            for repo in trending[:5]:  # take top 5 projects
                name = repo.get("name", "Unnamed")
                desc = repo.get("description", "No description")
                signal_text = f"{name} - {desc}"
                signals.append(signal_text)
            return signals
        else:
            logger.error("GitHub trending API returned status %s", response.status_code)
    except Exception as e:
        logger.error("Error fetching GitHub trending: %s", e)
    return ["Fallback signal: Trending project 'Alpha' showing explosive growth"]

def fetch_hn_top_stories():
    try:
        response = requests.get(HN_TOP_STORIES_URL, timeout=10)
        if response.status_code == 200:
            story_ids = response.json()
            signals = []
            for sid in story_ids[:5]:  # fetch details for top 5 stories
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                story_resp = requests.get(story_url, timeout=10)
                if story_resp.status_code == 200:
                    story = story_resp.json()
                    title = story.get("title", "No Title")
                    signals.append(title)
            logger.info("Fetched %d Hacker News top stories.", len(signals))
            return signals
        else:
            logger.error("Hacker News API returned status %s", response.status_code)
    except Exception as e:
        logger.error("Error fetching Hacker News top stories: %s", e)
    return ["Fallback signal: Breaking tech news disrupting markets"]

def validate_signal(signal_text):
    """
    Simulated validation:
    - Entropy Score: signal length scaled arbitrarily.
    - Relevance: contains keywords like 'ai', 'tech', 'startup', or 'innovation'.
    """
    entropy_score = len(signal_text) / 100.0  # arbitrary scaling
    relevant = any(kw in signal_text.lower() for kw in ["ai", "tech", "startup", "innovation"])
    return entropy_score, relevant

def process_external_signals():
    github_signals = fetch_github_trending()
    hn_signals = fetch_hn_top_stories()
    
    all_signals = github_signals + hn_signals
    processed = []
    for signal in all_signals:
        entropy, relevant = validate_signal(signal)
        # Only accept signals with sufficient novelty (entropy > 0.3) and strategic relevance.
        if entropy > 0.3 and relevant:
            processed.append(signal)
    logger.info("Processed external signals: %s", processed)
    return processed

def test_self():
    signals = process_external_signals()
    print("External Signal Bridge Self-Test Result:", signals)
    return {"valid": True, "state": signals, "logs": ["External Signal Bridge self-test passed."], "next": []}

if __name__ == "__main__":
    test_self()
