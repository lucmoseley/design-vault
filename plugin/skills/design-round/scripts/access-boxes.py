"""access-boxes.py — the boxes of a page's generated text, the ::before and
::after content check-access.py measures for contrast (#189). No DOM call
gives a pseudo-element's box, so they are read from Chromium's DevTools
protocol, which lists each element's pseudo-elements with one quad per line
they set. A module of its own so its tests call what check-access.py calls.
Its only I/O is the DevTools commands it sends through the `send` it is given.

A box is [left, top, right, bottom] in CSS px from the window's top left, as
getClientRects() gives a text node's.
"""


def generated_boxes(send, wanted):
    """Each wanted pseudo-element's boxes, one a line: [] where it draws
    nothing, None where its box cannot be found. `send(method, params)` sends
    one DevTools command to the page and raises Playwright's Error where the
    browser refuses it; `wanted` holds an (expression, pseudo) pair for each,
    a JavaScript expression for its element and "before" or "after"."""
    # Imported here, not at the top, so a machine without Playwright reaches
    # check-flow.py's run_browser(), which names the install, before this runs.
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
            # No pseudo-element, or one with no quads, has no box: a replaced
            # element's, or one under display: none.
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
