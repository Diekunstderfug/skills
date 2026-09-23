def handle_request(supervisor, payload):
    job_id = supervisor.submit(payload)
    return {"job_id": job_id}
