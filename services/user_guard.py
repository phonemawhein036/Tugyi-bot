from database import get_user, add_user, reset_daily_if_needed
from config import DAILY_LIMIT
from datetime import datetime


def check_user_status(update):
    user = update.effective_user
    add_user(user.id, user.username)

    reset_daily_if_needed(user.id)
    data = get_user(user.id)

    if data[6] == 1:
        return "banned"

    # Expiry check
    expiry = data[4]
    if expiry:
        if datetime.now() > datetime.fromisoformat(expiry):
            return "expired"

    # Daily limit
    daily_count = data[2]
    is_vip = data[6]

    if not is_vip and daily_count >= DAILY_LIMIT:
        return "limit"

    return "ok"
