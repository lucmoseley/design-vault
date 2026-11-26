def generated_boxes(send, wanted):
    # #189
    from playwright.sync_api import Error as PlaywrightError

    out = []
    for expression, pseudo in wanted:
        try:
            element = send("Runtime.evaluate", {"expression": expression})
            node = send("DOM.describeNode", {"objectId": element["result"]["objectId"]})
            matching = [
                p
                for p in node["node"].get("pseudoElements", [])
                if p["pseudoType"] == pseudo
            ]
            quads = (
                send(
                    "DOM.getContentQuads",
                    {"backendNodeId": matching[0]["backendNodeId"]},
                )["quads"]
                if matching
                else []
            )
        except (PlaywrightError, KeyError):
            out.append(None)
            continue
        out.append(
            [[min(q[0::2]), min(q[1::2]), max(q[0::2]), max(q[1::2])] for q in quads]
        )
    return out
