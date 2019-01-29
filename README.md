## How use API

For generate requests use Postman.

For create, update and delete you must autorized. For this send GET or POST request to http://127.0.0.1:5000/login with request body "username=Test&password=123456" for example.

### Get posts

Send GET request to http://127.0.0.1:5000/api/1.0/blog

Response format = json

### Create post

Send PUT request to http://127.0.0.1:5000/api/1.0/blog/create with request body "title=Test&body=Test text" for example.

### Update post

Send POST request to http://127.0.0.1:5000/api/1.0/blog/<int:id> with request body "title=Test&body=Test text" for example.

### Delete post

Send DELETE request to http://127.0.0.1:5000/api/1.0/blog/<int:id>
