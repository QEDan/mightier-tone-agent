# Tone Definitions Library

This directory contains human-readable JSON tone definitions for [Mightier
Amp](https://github.com/tuntorius/mightier_amp) and compatible NUX Mighty
modeling devices. Each new tone created manually or by a coding agent should
be saved as a JSON file here.

## Generate a QR code

From the repository root, compile a tone and write its QR code:

```bash
python3 gen_qr.py tones/funk49.json tones/funk49.png
```

The PNG is generated output and is ignored by Git. Open it in the Mightier Amp
app's QR scanner to sync the preset to your device.

For a coding agent to create the JSON and QR code from a tone description, see
the repository instructions in `AGENTS.md`. To use an external LLM instead,
follow the copy-and-paste workflow in `../README.md` and `../prompt_template.md`.

## Included Presets

| File | Tone / Song | Artist | Amp Model | Cab Model | Main EFX |
|---|---|---|---|---|---|
| [`back_in_black.json`](back_in_black.json) | Back in Black | AC/DC (Angus Young) | Plexi 100 | M1960AX | RC Boost |
| [`funk49.json`](funk49.json) | Funk #49 | James Gang (Joe Walsh) | Deluxe Rvb | DR112 | Rose Comp, T Screamer, 6-Band EQ |
| [`nitro.json`](nitro.json) | Nitro | Dick Dale | Twin Reverb | TR212 | RC Boost, Spring Reverb, 6-Band EQ |
| [`the_fly.json`](the_fly.json) | The Fly | U2 (The Edge) | Brit 800 | M1960AV | Dist One, Phase 90 |
| [`unchained.json`](unchained.json) | Unchained | Van Halen (Eddie Van Halen) | Plexi 100 | GB412 | RC Boost, Flanger |
| [`settings.json`](settings.json) | Multi-Preset Pack | Multi-artist collection | Various | Various | Various |
| [`foxylady.json`](foxylady.json) | Foxy Lady | Jimi Hendrix | Plexi 100 | GB412 | Muff Fuzz, Spring Reverb |

## File Naming Convention

- Use lowercase `snake_case`: `<artist_or_song_name>.json` (e.g. `srv_pride_and_joy.json`, `comfortably_numb_solo.json`).
- Keep tone files focused on a specific tone or song section.

## Contributing Tones

We welcome contributions! Create a tone with a coding agent using
`AGENTS.md`, or use the external-LLM prompt in [`../prompt_template.md`](../prompt_template.md).
Save the JSON file in this directory and verify it with
`python3 gen_qr.py tones/your_tone.json --dump-json`. Generate and test its QR
code before submitting a Pull Request.
