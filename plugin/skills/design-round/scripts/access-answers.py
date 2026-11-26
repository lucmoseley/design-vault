import collections

QUESTIONS = (
    ("vault.contrast", "text contrast (WCAG 1.4.3)"),
    ("vault.control-edges", "control edges (WCAG 1.4.11)"),
    ("vault.target-size", "target size (WCAG 2.5.8)"),
    ("vault.colour-script", "links told apart by colour alone (WCAG 1.4.1, G183)"),
    ("vault.keyboard", "reached by keyboard (WCAG 2.1.1)"),
    ("vault.focus", "focus shown, not hidden under a bar (WCAG 2.4.7, 2.4.11)"),
    ("vault.pause", "a pause for motion over 5 s (WCAG 2.2.2)"),
    (
        "vault.contrast-ladder",
        "icons, state marks and thin faces by the contrast ladder",
    ),
    ("vault.controls-on-photo", "controls on a photo and the current page dot"),
    ("vault.fill-text", "text polarity on a fill"),
    ("vault.chart-contrast", "chart marks against what is next to them (WCAG 1.4.11)"),
    ("vault.forced-colours-edge", "control edges under forced colours"),
    ("vault.theme-contrast", "contrast in each colour scheme the page ships"),
    ("vault.skip-link", "a skip link first (WCAG 2.4.1)"),
    ("vault.visual-order", "parts shown in their source order (WCAG 1.3.2, 2.4.3)"),
    ("vault.scroller-focus", "scrolling boxes reached by Tab (WCAG 2.1.1)"),
    ("vault.roving-focus", "a composite widget one Tab stop, arrows inside (APG)"),
    ("vault.menu-focus", "focus in a menu a button opens (APG)"),
    ("vault.carousel-focus", "focus in a declared carousel (APG)"),
    ("vault.ring-outline", "focus rings drawn with outline"),
    ("vault.focus-colour-kept", "the focus colour kept for focus"),
    ("vault.focus-visible", "focus rings on :focus-visible"),
)


Judged = collections.namedtuple("Judged", "faults unmeasured exempt notes")


def unjudged():
    return Judged([], [], [], [])


def answers(found, questions=QUESTIONS):
    out = {}
    for qid, _ in questions:
        faults, unmeasured, exempt, notes = {}, {}, {}, {}
        for name, judged in found:
            for merged, findings in (
                (faults, judged[qid].faults),
                (exempt, judged[qid].exempt),
            ):
                here = {}
                for f in findings:
                    details = here.setdefault(f["subject"], [])
                    if f["detail"] not in details:
                        details.append(f["detail"])
                for subject, details in here.items():
                    held = merged.setdefault(
                        subject,
                        {"subject": subject, "detail": "; ".join(details), "at": []},
                    )
                    held["at"].append(name)
            for why in judged[qid].unmeasured:
                unmeasured.setdefault(why, []).append(name)
            for note in judged[qid].notes:
                notes.setdefault(note, []).append(name)
        answer = "fail" if faults else "cannot measure" if unmeasured else "pass"
        out[qid] = {
            "answer": answer,
            "faults": list(faults.values()),
            "unmeasured": [{"reason": why, "at": at} for why, at in unmeasured.items()],
            "exempt": list(exempt.values()),
            "notes": [{"note": note, "at": at} for note, at in notes.items()],
        }
    return out
