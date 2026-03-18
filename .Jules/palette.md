## $(date +%Y-%m-%d) - Render Assistant Output as Markdown in CLI
**Learning:** Raw terminal strings from language models can be difficult to read, particularly when there are code snippets or formatted texts. For CLI applications, applying `rich.markdown.Markdown` transforms typical LLM text into neatly styled blocks with code syntax highlighting and distinct headers.
**Action:** When working on CLI tooling that echoes Assistant text, explicitly evaluate using a library like `rich` to render the Markdown rather than passing raw text strings straight to the terminal output.
