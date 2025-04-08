import redis
from config.local import redis_conf

connection_pool = redis.ConnectionPool(**redis_conf)

def redis_conn():
    return redis.Redis(connection_pool=connection_pool)

def check_username(username):
    with redis_conn() as r:
        return r.exists(username) == 0

def add_user(username, encoding):
    with redis_conn() as r:
        r.set(username, encoding)
    print(f'\033[92mUser [{username}] has been successfully registered\n\033[0m')

def get_info():
    with redis_conn() as r:
        users = []
        for key in r.scan_iter():
            users.append((key.decode('utf-8'), r.get(key)))
        return users
