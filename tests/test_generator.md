# Basic test
curl -X POST http://localhost:8000/api/auth/generate-password \
  -H "Content-Type: application/json" \
  -d '{"length":12, "upper":true, "lower":true, "digits":true, "special":true}'

# Test with specific parameter
curl -X POST http://localhost:8000/api/auth/generate-password \
  -H "Content-Type: application/json" \
  -d '{"length":16, "upper":false, "lower":true, "digits":true, "special":false}'

# validation test (must fail)
curl -X POST http://localhost:8000/api/auth/generate-password \
  -H "Content-Type: application/json" \
  -d '{"length":5, "upper":false, "lower":false, "digits":false, "special":false}'
