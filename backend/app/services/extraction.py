"""Deterministic lead extraction. Never invent missing fields."""
import re

BUDGET_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(lakh|lac|crore|cr|l)\b", re.I)
PHONE_RE = re.compile(r"(?:\+?91[-\s]?)?(\d{10})")
BHK_RE = re.compile(r"(\d+)\s*bhk", re.I)
PROPERTY_TYPES = ["apartment", "flat", "villa", "plot", "house", "independent house", "penthouse"]
INTENT_BUY = re.compile(r"\bbuy|purchase|own\b", re.I)
INTENT_RENT = re.compile(r"\brent|lease|rental\b", re.I)
LOCATIONS = ["gachibowli", "madhapur", "kondapur", "hitech city", "hyderabad", "bangalore", "pune", "mumbai", "delhi"]


def extract_lead(transcript: str) -> dict:
    t = transcript or ""
    lower = t.lower()

    # name: "my name is X" or "I am X"
    name = None
    m = re.search(r"(?:my name is|i am|i'm|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", t, re.IGNORECASE)
    if m:
        name = m.group(1).strip()

    phone = None
    pm = PHONE_RE.search(t)
    if pm:
        phone = pm.group(1)

    budget = None
    bm = BUDGET_RE.search(t)
    if bm:
        budget = f"{bm.group(1)} {bm.group(2)}".strip()

    bhk = None
    bhm = BHK_RE.search(t)
    if bhm:
        bhk = f"{bhm.group(1)} BHK"

    property_type = None
    for pt in PROPERTY_TYPES:
        if pt in lower:
            property_type = pt.title()
            break

    location = None
    for loc in LOCATIONS:
        if loc in lower:
            location = loc.title()
            break

    intent = None
    if INTENT_BUY.search(t):
        intent = "buy"
    elif INTENT_RENT.search(t):
        intent = "rent"

    notes = None
    # capture "need X" tail
    nm = re.search(r"need\s+(.+?)(?:\.|$)", t, re.I)
    if nm:
        notes = nm.group(1).strip()

    return {
        "name": name,
        "phone": phone,
        "budget": budget,
        "location": location,
        "property_type": property_type,
        "bhk": bhk,
        "intent": intent,
        "notes": notes,
    }
