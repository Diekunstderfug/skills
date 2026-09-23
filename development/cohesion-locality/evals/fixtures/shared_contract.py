def send_receipt(client, email, receipt):
    return client.send(email.strip().lower(), receipt)


def send_alert(client, email, alert):
    return client.send(email, alert)
