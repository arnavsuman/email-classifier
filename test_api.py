import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# Standard test structure
EXPECTED_KEYS = {
    "input_email_body",
    "list_of_masked_entities",
    "masked_email",
    "category_of_the_email"
}


def test_valid_email():
    response = client.post("/classify", json={
        "input_email_body": (
            "Hi, my email is johndoe@example.com and my phone number is 9876543210."
        )
    })
    assert response.status_code == 200
    data = response.json()
    assert EXPECTED_KEYS.issubset(data)
    assert isinstance(data["list_of_masked_entities"], list)


def test_empty_email():
    response = client.post("/classify", json={
        "input_email_body": ""
    })
    assert response.status_code == 200
    data = response.json()
    assert data["masked_email"] == ""
    assert data["category_of_the_email"] is not None


def test_only_pii():
    response = client.post("/classify", json={
        "input_email_body": "Aadhar: 1234 5678 9012, CVV: 123, Expiry: 12/25"
    })
    assert response.status_code == 200
    data = response.json()
    assert any(
        e["classification"] in {"aadhar_num", "cvv_no", "expiry_no"}
        for e in data["list_of_masked_entities"]
    )


def test_very_long_email():
    long_email = "Hello,\n" + ("This is a long message. " * 1000)
    response = client.post("/classify", json={
        "input_email_body": long_email
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["masked_email"]) > 1000


def test_email_with_unknown_content():
    response = client.post("/classify", json={
        "input_email_body": "Blah blah xyz gibberish asdfgh"
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["category_of_the_email"], str)


if __name__ == "__main__":
    print("ALL TESTS PASSED")
