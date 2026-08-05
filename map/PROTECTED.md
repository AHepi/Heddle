# PROTECTED — surfaces that must not change without the human authority's
# verbatim recorded words. Correctness evidence never substitutes.

1. **HEDDLE_0_1.md semantics.** The spec text. Code may be fixed to meet
   it; it is not edited to meet code.
2. **The JSONL event vocabulary** (heddle/runlog.py event names and the
   fields emitted at each site in heddle/interpreter.py). Old logs must
   stay interpretable forever — prefer adding events over renaming.
3. **The grant-intersection rule** (heddle/interpreter.py `_do_call`):
   child grants are a filter on the parent's list. Widening must remain
   inexpressible.
4. **The dispatch check order** (heddle/interpreter.py `_tool_call`):
   visible → domain → limit, first failure reported.
5. **The closed outcome contract** (heddle/loader.py + interpreter):
   a step returns only a declared outcome; free text never becomes control.

Tripwire: `git diff --name-only HEAD -- heddle/ map/ HEDDLE_0_1.md` pasted
at plan and validate — empty or explained. (Tool: protected_tripwire.)
