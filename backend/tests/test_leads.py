def test_create_and_list_lead(client):
    payload = {"name": "Ravi Kumar", "phone": "9876543210", "budget": "80 lakh", "location": "Gachibowli", "intent": "buy", "status": "new"}
    r = client.post("/api/leads", json=payload)
    assert r.status_code == 201
    lead = r.json()
    assert lead["name"] == "Ravi Kumar"
    assert lead["id"] is not None

    r2 = client.get("/api/leads")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1

    r3 = client.get(f"/api/leads/{lead['id']}")
    assert r3.status_code == 200

    r4 = client.patch(f"/api/leads/{lead['id']}", json={"status": "contacted"})
    assert r4.status_code == 200
    assert r4.json()["status"] == "contacted"

    r5 = client.delete(f"/api/leads/{lead['id']}")
    assert r5.status_code == 204


def test_search_lead(client):
    client.post("/api/leads", json={"name": "Priya", "location": "Madhapur", "status": "new"})
    r = client.get("/api/leads", params={"q": "Priya"})
    assert r.status_code == 200
    assert any("Priya" in (l.get("name") or "") for l in r.json()["items"])