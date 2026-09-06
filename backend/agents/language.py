LANGUAGE_NAME = {"bn": "বাংলা (Bengali)", "en": "English"}


def language_directive(lang: str) -> str:
    """Appended to an LLM system prompt so its user-facing output — not its
    reasoning about Bangla source data — respects the user's language
    preference. Written in Bangla since that's the tool prompts' base
    language, but names the target language explicitly so it works
    regardless of which one is requested."""
    name = LANGUAGE_NAME.get(lang, LANGUAGE_NAME["bn"])
    return f"\n\nতোমার চূড়ান্ত উত্তর অবশ্যই {name} ভাষায় লিখবে।"
