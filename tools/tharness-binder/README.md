# THarness Binder

THarness Binder is a small Rust desktop app for binding this THarness main framework to a target project folder.

It creates a lightweight `.tharness/` anchor and maintains an `AGENTS.md` startup bridge in the selected project. It does not copy `AIGC/`.

## Build

```powershell
cargo build --release --manifest-path tools\tharness-binder\Cargo.toml
```

The packaged executable is expected at the THarness root:

```text
THarness-Binder.exe
```
