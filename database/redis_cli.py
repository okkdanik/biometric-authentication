import redis
from config.local import redis_conf

def redis_conn():
    return redis.Redis(**redis_conf)

def check_username(username):
    r = redis_conn()
    return r.exists(username) == 0

def add_user(username, encoding):
    r = redis_conn()
    r.set(username, encoding)
    print(f'User [{username}] has been successfully registered\n')

def get_info():
    r = redis_conn()
    users = [(user.decode('utf-8'), r.get(user)) for user in r.keys()]

    return users
