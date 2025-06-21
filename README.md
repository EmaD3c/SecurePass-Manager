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

curl -X POST http://localhost:8000/api/auth/add_password \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTkxMTc4NSwianRpIjoiNTFmOTdjOGEtZjIyYi00MzUxLWE4MGYtN2MzYjVkNGRjYjAxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjMiLCJuYmYiOj
E3NDE5MTE3ODUsImNzcmYiOiI5YjRkMjdmNS00YjY1LTQ0YmEtYjNjZC05MTYzZWU3NjUxNWYiLCJleHAiOjE3NDE5MTUzODV9.TX2YVpFD5Po8wyNWT0MLCDeaXEgLRsJzWSb3EaMRHjA" \
     -d '{                         
           "name": "MonMotDePasse",
           "password": "motdepasse123"
         }'

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
  
# list password 
curl -X GET http://localhost:8000/api/auth/list_passwords \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN"

     

code .

password generator : utilisation de secret et pas random pour plus de securiter 
