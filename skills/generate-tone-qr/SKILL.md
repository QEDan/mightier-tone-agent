---
name: generate-tone-qr
description: Create a Mighty Amp guitar tone from a user's description, save a compatible tone JSON file under tones/, and generate its QR-code PNG. Use when asked to design, create, or generate a tone or preset in this repository.
---

# Generate a tone and QR code across coding harnesses

Turn the user's tone description into a new Mighty Amp preset definition and
generate a scannable QR image. Finish with both a JSON file in `tones/` and its
QR PNG; do not only return JSON in chat.

## Procedure

1. Read `README.md`, `tones/README.md`, `prompt_template.md`, and the relevant
   sections of `mightier_amp_settings.md`. Follow the model names, available
   parameters, and JSON structure documented there and supported by `gen_qr.py`.
2. Translate the requested sound into the closest available device models and
   settings. If web research is available, use it for artist/song-specific
   gear details and distinguish confirmed information from approximation. Do
   not invent sources or claim research you did not perform. When the request
   is a general style rather than a specific recording, use a sensible musical
   interpretation without attributing it to an artist.
3. Choose a descriptive, lowercase `snake_case` filename based on the song,
   artist, or requested tone, such as `srv_pride_and_joy.json`. Check `tones/`
   first; do not overwrite an existing tone. Save a single-preset JSON object
   with a descriptive `name`, `device: "mighty_plug_pro"`, a valid `signal_chain`,
   and `blocks` configurations. Include helpful artist, guitar, playing, or
   source notes when relevant. Keep effect models and block parameters aligned
   with the reference and compiler; do not rely on unsupported fields to drive
   device settings.
4. Compile the saved definition and generate the QR image:

   ```bash
   python3 gen_qr.py tones/<tone_name>.json --dump-json
   python3 gen_qr.py tones/<tone_name>.json tones/<tone_name>.png
   ```

   Resolve any errors before finishing. The first command verifies that the
   definition compiles to device data; the second writes the QR PNG.
5. Display the generated QR PNG inline in the final chat response by default,
   using the harness's image-attachment or image-display feature. If the user
   asks not to display it, omit the image while still reporting its path. If
   inline display is unavailable, say so and provide the PNG path.
6. Report the JSON and PNG paths, the key tone choices, and any material
   uncertainty or approximation. The JSON file is the reusable tone
   definition; the PNG is generated output and is ignored by Git.

## Constraints

- The user’s requested tone description is authoritative; ask a concise
  clarification only when an ambiguity would materially change the preset.
- Use valid model names and supported settings from `mightier_amp_settings.md`
  and `gen_qr.py`. The compiler may map unknown model names to defaults rather
  than reporting an error, so inspect each chosen name against the reference.
- Preserve the external workflow: when asked for copy-and-paste instructions,
  direct users to `prompt_template.md` and explain how to save the resulting
  JSON in `tones/` before running `gen_qr.py`.
