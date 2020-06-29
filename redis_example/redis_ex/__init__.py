from flask import Flask

from redis_ex.redis_handler.redis_handler import RedisCacheManager

app = Flask(__name__)
app.config.from_object('config')

# Initialized app with Redis Cache
cache = RedisCacheManager(app=app, strict=True)

from redis_ex import views
