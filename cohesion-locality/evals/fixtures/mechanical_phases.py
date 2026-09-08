def init(config):
    return {"rate": config.tax_rate, "width": config.paper_width}


def process(state, amount):
    return {**state, "tax": amount * state["rate"]}


def finish(state):
    return str(state["tax"]).rjust(state["width"])
