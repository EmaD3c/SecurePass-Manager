# SecurePass-Manager 

# register
curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "testpassword"}'

# login
curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "testpassword"}'

# add password
curl -X POST http://localhost:8000/api/auth/add_password \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN" \
     -d '{"name": "Netflix", "password": "1234"}'

# modify/update password
curl -X PUT http://localhost:8000/api/auth/update_password \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN" \
     -d '{"password_id": 1, "password": "newpassword"}'

# delete password
curl -X DELETE http://localhost:8000/api/auth/delete_password \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN" \
     -d '{"password_id": 1}'
     