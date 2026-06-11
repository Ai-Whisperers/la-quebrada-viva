"""Diagnostic / audit helpers — dormant subpackage.

Intentionally NOT imported by any other lqv/* module. Each helper is opt-in,
run by hand after a scene build (`scripts/smoke_test.sh` then a manual
``python -c "from lqv.util import ten_rules_check; ten_rules_check.run()"``).
Keeping these out of the build path means they can never change render
byte-identity.

Why this exists:
* The 10 design rules and the RNG-seed invariant are easy to break silently.
* Catching a violation in a deterministic post-build audit is much cheaper
  than diffing two PNG renders by eye.
* Audits run inside Blender's Python (need bpy), so they can't live in pytest.
"""
