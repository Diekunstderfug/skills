def _can_withdraw(account, amount):
    return account.balance >= amount


def _debit(account, amount):
    account.balance -= amount


def withdraw(account, amount):
    with account.lock:
        if _can_withdraw(account, amount):
            _debit(account, amount)
