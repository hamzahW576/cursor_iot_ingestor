class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_body(self, client):
        body = client.get("/health").json()
        assert body["status"] == "healthy"
        assert "version" in body
        assert "app_name" in body
