
## 2025-02-23 - Fast tape entry text serialization using yaml.CSafeDumper
**Learning:** `json.dumps` breaks YAML string formatting which is dangerous when output represents prompts or structured data. `yaml.safe_dump` is notoriously slow for large or frequent dictionaries. A major performance bottleneck can be resolved strictly by dropping in `yaml.CSafeDumper`, which utilizes C-extensions to make YAML serialization up to 4x faster without altering output format.
**Action:** When working with yaml serialization inside performance-critical paths, prefer `yaml.dump(..., Dumper=yaml.CSafeDumper)` over `yaml.safe_dump()`, keeping `yaml.SafeDumper` as a fallback.
