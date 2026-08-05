# REC-add-flow-item — adding an eighth flow item type.

1. Spec first: the item's shape and its rules go in HEDDLE_0_1.md §3 (a
   protected surface — get the human's verbatim approval recorded in the
   REQ- doc BEFORE code).
2. Validator: one case in `_validate_items` (heddle/validate.py), reporting
   every malformed instance with line numbers.
3. Interpreter: one case in `_walk` (heddle/interpreter.py) — the spec's
   "adding a construct is adding a case to one dispatch function".
4. `show`: one branch in cli.py's walk so the item is inspectable pre-run.
5. Tests: one happy-path, one validation-failure, one determinism check.
   Mutation-prove the validation test: break the flow, watch it go red.
6. Same commit: this REC's stamp, SUB-interpreter, SUB-validate, SUB-cli,
   RESULTS entry. Gate green or nothing lands.
