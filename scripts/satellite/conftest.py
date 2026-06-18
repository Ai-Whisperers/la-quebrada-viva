# Keep pytest from collecting the exploratory STAC liveness probe — it's a
# CLI diagnostic invoked manually, makes live network calls on import, and
# exits nonzero by design when endpoints are down. None of that belongs in
# the unit-test grid.
collect_ignore = ["test_stac.py"]
