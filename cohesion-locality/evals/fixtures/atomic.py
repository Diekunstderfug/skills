def transfer(db, source, target, amount):
    with db.transaction():
        db.debit(source, amount)
        db.credit(target, amount)
