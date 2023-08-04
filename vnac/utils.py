from string import punctuation


def clean_str(s: str):
    return s.strip().strip(punctuation)
