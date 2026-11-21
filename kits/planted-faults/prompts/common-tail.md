
**Your reply.** When you have read everything and judged, reply with only one JSON object in a ```json fence, and nothing after it:

```json
{"seen": ["every image file name you opened"],
 "findings": [{"where": "the section and the part, in words a designer would recognise",
               "fault": "what is wrong, in plain words",
               "who_objects": "who would object, and why",
               "kind": "function | hierarchy | type | colour-surface | treatment | layout | trust-conversion | brief-fit | other",
               "severity": "P0 | P1 | P2 | P3"}]}
```

Report each distinct fault once, at the place it is worst; where one fault recurs, name every place in `where`. No praise, no recommendations without a fault, no summary. Where you find no fault, give an empty list.
