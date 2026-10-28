from app.rate_limit import RateLimiter


def test_per_ip_limit_uses_a_sliding_minute():
    limiter = RateLimiter(per_minute=2, per_day=100)
    assert limiter.allow("1.1.1.1", now=0)
    assert limiter.allow("1.1.1.1", now=10)
    assert not limiter.allow("1.1.1.1", now=20)
    assert limiter.allow("2.2.2.2", now=20)  # other IPs are not affected
    assert limiter.allow("1.1.1.1", now=61)  # the first request has left the window


def test_daily_cap_applies_across_ips_and_resets_next_day():
    limiter = RateLimiter(per_minute=10, per_day=2)
    assert limiter.allow("1.1.1.1", now=0)
    assert limiter.allow("2.2.2.2", now=0)
    assert not limiter.allow("3.3.3.3", now=0)
    assert limiter.allow("3.3.3.3", now=86_400)


def test_rejected_requests_do_not_count():
    limiter = RateLimiter(per_minute=1, per_day=100)
    assert limiter.allow("1.1.1.1", now=0)
    for t in range(1, 50):
        assert not limiter.allow("1.1.1.1", now=t)
    assert limiter.allow("1.1.1.1", now=60.5)


def test_assess_endpoint_returns_429_without_calling_the_pipeline(monkeypatch):
    from fastapi.testclient import TestClient

    from app import main

    calls = []

    def fake_assess(text):
        calls.append(text)
        raise RuntimeError("fake pipeline")

    monkeypatch.setattr(main, "limiter", RateLimiter(per_minute=1, per_day=100))
    monkeypatch.setattr(main, "assess", fake_assess)
    client = TestClient(main.app, raise_server_exceptions=False)

    first = client.post("/assess", json={"text": "hello"})
    second = client.post("/assess", json={"text": "hello"})

    assert first.status_code == 502  # reached the (fake, failing) pipeline
    assert second.status_code == 429
    assert calls == ["hello"]
