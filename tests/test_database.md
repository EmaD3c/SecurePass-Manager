# test database 
psql -h localhost -p 8001 -U postgres -d postgres
docker exec -it db psql -U postgres -d postgres

# search for users by email adress
postgres=# SELECT * FROM users WHERE email = 'test@example.com';

# search for all users
SELECT * FROM users; ! NOT WORKING !

# search for all passwords
SELECT id, name, password FROM passwords; 