# INV-grant-semantics — protected surface (see PROTECTED.md items 3–4).

- Visibility = skill tool list ∩ live grants (`when` matches step or
  'always') ∩ caller's held list (sub-flows). Absence, not refusal:
  invisible tools are not in the prompt at all.
- A `call` can only narrow: `child = [t for t in parent if t in requested]`.
- Dispatch order is visible → domain → limit; first failure is reported,
  logged, and counts against the limit.
Check: `python -m pytest tests_heddle -q -k "visibility or narrows"` exits
clean. Verified 2026-08-05 @ 893044f: 2 passed.
