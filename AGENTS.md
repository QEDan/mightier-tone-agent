# Agent instructions

When a user asks to create a guitar tone or Mighty Amp preset, follow the
`generate-tone-qr` skill in `skills/generate-tone-qr/SKILL.md`. Complete the
workflow by saving a new human-readable JSON definition in `tones/` and
generating its QR-code PNG with `gen_qr.py`. Do not stop after proposing a
preset or printing JSON in chat.

Display the generated QR code inline in the final chat response by default,
using the harness's image-attachment or image-display feature. Do not display
it if the user asks you not to. If inline display is unavailable, state that
and provide the PNG path.

Keep the external-LLM copy-and-paste workflow documented in `README.md`
available. If the user specifically asks for instructions or JSON to use
outside this repository, follow that request rather than generating files.
