$ python app.py

$ curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare how Dumbledore and Snape viewed Harry role in defeating Voldemort"}'
