import re


def extract_score(text):
    try:
        # 🔍 Match multiple formats
        match = re.search(r"score\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)

        if match:
            score = int(match.group(1))

            # 🔒 Ensure valid range
            if 0 <= score <= 10:
                return score

        return 0

    except Exception as e:
        print("Score parsing error:", e)
        return 0