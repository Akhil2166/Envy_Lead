from app.services.extraction import extract_lead


def test_extract_basic():
    t = "My name is Ravi Kumar. I am looking to buy a 2 BHK apartment in Gachibowli. My budget is 80 lakh. Please call me on 9876543210. I need covered parking."
    d = extract_lead(t)
    assert d["name"] == "Ravi Kumar"
    assert d["phone"] == "9876543210"
    assert d["budget"] == "80 lakh"
    assert d["location"] == "Gachibowli"
    assert d["bhk"] == "2 BHK"
    assert d["property_type"] == "Apartment"
    assert d["intent"] == "buy"


def test_extract_does_not_invent():
    d = extract_lead("Hello, just browsing.")
    assert d["name"] is None
    assert d["phone"] is None
    assert d["budget"] is None