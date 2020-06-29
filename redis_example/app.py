from redis_ex import app

app.run(
    host='localhost',
    port=8080,
    debug=True
)
