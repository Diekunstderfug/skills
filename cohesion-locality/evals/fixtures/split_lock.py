def can_withdraw(account, amount):
    with account.lock:
        return account.balance >= amount


def debit(account, amount):
    with account.lock:
        account.balance -= amount


def withdraw(account, amount):
    if can_withdraw(account, amount):
        debit(account, amount)
