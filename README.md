```bash
curl http://localhost:5000/users

curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"name":"Harsha","email":"harsha@gmail.com"}'

curl -X PUT http://localhost:5000/users/1 \
-H "Content-Type: application/json" \
-d '{"name":"Harsha Reddy","email":"harsha123@gmail.com"}'

curl -X DELETE http://localhost:5000/users/1
'''
