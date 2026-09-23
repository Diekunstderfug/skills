class UserOperations:
    def discount(self, user, subtotal):
        return subtotal * (0.9 if user.is_member else 1)

    def write_csv(self, users, stream):
        import csv
        writer = csv.writer(stream)
        writer.writerow(["name", "email"])
        writer.writerows((u.name, u.email) for u in users)
