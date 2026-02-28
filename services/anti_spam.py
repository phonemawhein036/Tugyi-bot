import time

user_last_action = {}

COOLDOWN = 10  # seconds

def check_spam(user_id):
    now = time.time()

    if user_id in user_last_action:
        if now - user_last_action[user_id] < COOLDOWN:
            return False

    user_last_action[user_id] = now
    return True
