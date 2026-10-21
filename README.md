# Mightier Amp QR Code Generator & Tone Prompt Toolkit

Generate NUX Mighty Amp-compatible preset QR codes from human-readable JSON
tone definitions. Create tones either with an external LLM and the
copy-and-paste prompt, or by asking a repository-aware coding agent to complete
the tone-to-QR workflow. Both workflows produce a reusable JSON definition in
`tones/`.

`gen_qr.py` compiles presets into high error-correction QR code PNGs
(`nux://MightyAmp:...`). The reference catalogue in
[`mightier_amp_settings.md`](mightier_amp_settings.md) describes the Mighty Plug
Pro models, parameters, and signal chain.

## Prerequisites

Install Python 3 and the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## External LLM: copy and paste

1. Open `prompt_template.md` in your preferred LLM and provide the relevant
   context from `mightier_amp_settings.md`.
2. Replace the tone-description placeholder with your desired song, artist, or
   sound and submit the prompt.
3. Save the generated preset JSON as a new file under `tones/`, using a
   lowercase `snake_case` name (for example, `tones/my_tone.json`).
4. Generate its QR code:

   ```bash
   python3 gen_qr.py tones/my_tone.json tones/my_tone.png
   ```

## Coding agent: end-to-end

In a coding harness that supports repository instructions and skills, describe
the tone you want and ask the agent to create it. The repository's `AGENTS.md`
and harness-agnostic skill in `skills/generate-tone-qr/SKILL.md` direct the
agent to research and map the tone, save a new JSON definition under `tones/`,
compile it, and generate the corresponding PNG. The agent should report both
output paths and any notable approximations.

## Generator examples

List presets in a collection:

```bash
python3 gen_qr.py tones/settings.json --list
```

Choose a preset by name:

```bash
python3 gen_qr.py tones/settings.json -o nitro.png --preset "Nitro - Dick Dale"
```

Compile a definition without writing an image (useful for validating JSON):

```bash
python3 gen_qr.py tones/my_tone.json --dump-json
```

Open the generated PNG in the NUX Mighty Amp mobile app's QR scanner to sync
the preset to your device.
