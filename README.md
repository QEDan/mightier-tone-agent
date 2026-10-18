# Mightier Amp QR Code Generator & Tone Prompt Toolkit

A repository containing tools for generating NUX Mighty Amp-compatible preset QR codes from human-readable JSON definition files, alongside an LLM prompt workflow to research and generate custom guitar tones based on real-world gear.

https://github.com/tuntorius/mightier_amp

---

## Included Files

* **`gen_qr.py`**[cite: 1]: Python script to compile human-readable or raw preset JSON files into high error-correction QR code PNG images (`nux://MightyAmp:...`)[cite: 1] compatible with NUX Mighty Amp devices (such as the Mighty Plug Pro / MP-3)[cite: 1].
* **`mightier_amp_settings.md`**[cite: 2]: Complete machine- and human-readable catalogue of amplifiers, cabinets, effects, parameters, slots, and MIDI CC mappings for the Mighty Plug Pro[cite: 2].
* **`prompt_template.md`**: LLM prompt template designed to guide an AI agent through researching a tone, finding real-world gear equivalents, mapping them against `mightier_amp_settings.md`[cite: 2], and outputting a valid preset JSON file[cite: 1].

---

## Prerequisites & Dependencies

To run the QR code generator script, ensure you have Python 3 installed along with the required PIL and qrcode libraries[cite: 1]:

```bash
pip install qrcode[pil] pillow~
```


## Usage Workflow

### Step 1: Generate Tone JSON via LLM

1. Open your preferred LLM session.
2. Attach **`mightier_amp_settings.md`** as a context file.


3. Copy the text from **`prompt_template.md`**, insert your desired song, artist, or tone description, and submit the prompt.
4. Save the LLM's JSON output into your repo (e.g., `tones/my_tone.json`).

### Step 2: Inspect Available Presets (Optional)

If your JSON file contains a multi-preset collection, you can list all available presets using `--list`:

```bash
python gen_qr.py tones/my_tone.json --list

```

### Step 3: Generate QR Code PNG

Compile the preset JSON into a scannable QR code PNG image:

```bash
python gen_qr.py tones/my_tone.json output_qr.png

```

For multi-preset files, select a specific preset by name or index:

```bash
python gen_qr.py tones/settings.json -o my_preset.png --preset "Nitro - Dick Dale"

```

### Step 4: Scan & Play

Open the official NUX Mighty Amp mobile app, scan the generated PNG QR code with your device camera, and sync the preset directly to your hardware!
