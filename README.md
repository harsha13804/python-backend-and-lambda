```bash
curl http://localhost:5000/users

curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"name":"Harsha","email":"harsha@gmail.com"}'

curl -X PUT http://localhost:5000/users/1 \
-H "Content-Type: application/json" \
-d '{"name":"Harsha Reddy","email":"harsha123@gmail.com"}'

curl -X DELETE http://localhost:5000/users/1

curl https://dzklajxzr64bad75ziphjgd5ha0rlwyy.lambda-url.us-east-1.on.aws/users

curl -X POST https://dzklajxzr64bad75ziphjgd5ha0rlwyy.lambda-url.us-east-1.on.aws/users \
-H "Content-Type: application/json" \
-d '{"name":"Harsha","email":"harsha@gmail.com"}'

curl -X PUT https://dzklajxzr64bad75ziphjgd5ha0rlwyy.lambda-url.us-east-1.on.aws/users/2 \
-H "Content-Type: application/json" \
-d '{"name":"Harsha Reddy","email":"harsha123@gmail.com"}'

curl -X DELETE https://dzklajxzr64bad75ziphjgd5ha0rlwyy.lambda-url.us-east-1.on.aws/users/5
