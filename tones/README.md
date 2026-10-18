# Tone Definitions Library

This directory contains human-readable JSON tone definitions for use with [Mightier Amp](https://github.com/tuntorius/mightier_amp) and NUX Mighty modeling devices (including Mighty Plug Pro MP-3, Mighty Space, Mighty Plug MP-2, and Mighty Lite MKII).

## Generating QR Codes from Tones

To generate a QR code from any tone file in this directory:

```bash
# Basic usage (defaults output to <tone_name>.png):
python3 gen_qr.py tones/funk49.json

# Or specify a custom output filename:
python3 gen_qr.py tones/nitro.json nitro_qr.png
```

Once generated, open the **Mightier Amp** app on your phone, tap the QR scanner icon, and scan the PNG file directly from your monitor.

## Included Presets

| File | Tone / Song | Artist | Amp Model | Cab Model | Main EFX |
|---|---|---|---|---|---|
| [`back_in_black.json`](file:///home/mazur/linstore/repos/mightier-tone-agent/tones/back_in_black.json) | Back in Black | AC/DC (Angus Young) | Plexi 100 | M1960AX | RC Boost |
| [`funk49.json`](file:///home/mazur/linstore/repos/mightier-tone-agent/tones/funk49.json) | Funk #49 | James Gang (Joe Walsh) | Deluxe Rvb | DR112 | Rose Comp, T Screamer, 6-Band EQ |
| [`nitro.json`](file:///home/mazur/linstore/repos/mightier-tone-agent/tones/nitro.json) | Nitro | Dick Dale | Twin Reverb | TR212 | RC Boost, Spring Reverb, 6-Band EQ |
| [`settings.json`](file:///home/mazur/linstore/repos/mightier-tone-agent/tones/settings.json) | Multi-Preset Pack | Multi-artist collection | Various | Various | Various |
| [`nitro_fixed.json`](file:///home/mazur/linstore/repos/mightier-tone-agent/tones/nitro_fixed.json) | Nitro (Low-level) | Dick Dale | Twin Reverb | TR212 | Raw device payload format example |

## File Naming Convention

- Use lowercase `snake_case`: `<artist_or_song_name>.json` (e.g. `srv_pride_and_joy.json`, `comfortably_numb_solo.json`).
- Keep tone files focused on a specific tone or song section.

## Contributing Tones

We welcome contributions! To submit a new tone:
1. Create a tone using an AI agent (Cursor, Claude Code, Copilot) or the prompt template in [`PROMPT_TEMPLATE.md`](file:///home/mazur/linstore/repos/mightier-tone-agent/PROMPT_TEMPLATE.md).
2. Save your JSON file in this directory (`tones/`).
3. Verify that `python3 gen_qr.py tones/your_tone.json` compiles cleanly without warnings or errors.
4. Test the generated QR code with your amp and guitar to make sure it sounds great!
5. Submit a Pull Request.
