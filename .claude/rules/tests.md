---
paths:
  - "tests/**"
---

# Test rules

- One test per behavior. If a test needs "and" in its name, split it.
- Name tests after the behavior: `test_median_excludes_open_requests`, not `test_median_2`.
- Do not mock the code under test. Build small `Request` rows instead.
- No network access and no reading files outside `data/sample_311.csv`.
- Assert on values, not on types or "no exception raised".
