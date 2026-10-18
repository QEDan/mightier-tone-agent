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

Here are the two files ready to be added to the base of your repository: **`prompt_template.md`** and **`README.md`**.

---

## 1. `prompt_template.md`

```markdown
# NUX Mighty Amp Preset Generator Prompt Template

Copy and paste the template below into your LLM session (along with attaching `mightier_amp_settings.md` as a context file[cite: 2]) to generate a compatible JSON tone definition for `gen_qr.py`[cite: 1].

---

```text
You are an expert guitar tone engineer and digital modeler specialist familiar with the NUX Mighty Plug Pro ecosystem, the gen_qr.py script[cite: 1], and the detailed parameter reference in mightier_amp_settings.md[cite: 2].

I want you to help me design a custom guitar preset JSON definition for the following requested tone, artist, or song:

[INSERT YOUR TONE / SONG / ARTIST DESCRIPTION HERE]

Please follow this rigorous step-by-step workflow:

1. **Research Phase**:
   - Research the requested tone online.
   - If it is from a specific song or artist, identify the actual gear (guitars, amplifiers, pedalboards, cabinets, and studio effects) used to produce the tone on the original recording.
   - Review guitar forums, Reddit, and online discussions for tips, EQ settings, and insights shared by guitarists on how to achieve this specific tone.

2. **Mapping & Adaptation Phase**:
   - Review the attached `mightier_amp_settings.md` context file[cite: 2] to find the closest matching hardware models available in the NUX Mighty Plug Pro ecosystem (referencing valid amplifier names, cabinets/IRs, EFX/drives, modulations, delays, and reverbs listed in sections 2 through 11).
   - Select the most appropriate block order (`signal_chain`), block enable states, model choices, and parameter values (such as gain, bass, middle, treble, presence, decay, time, level, etc.) based on the available parameters documented in the reference guide.

3. **JSON Generation Phase**:
   - Output a valid JSON definition file that can be parsed directly by `gen_qr.py`[cite: 1].
   - The JSON should follow the human-readable preset format supported by `gen_qr.py`[cite: 1] (either as a single preset dictionary or a multi-preset collection containing a `"presets"` array).
   - Ensure the structure includes:
     - `"name"`: Descriptive name of the preset.
     - `"artist"`: Artist or style inspiration (optional).
     - `"device"`: `"mighty_plug_pro"`.
     - `"signal_chain"`: Array of block names in proper routing order (e.g., `["noise_gate", "compressor", "modulation", "efx", "amplifier", "cabinet", "eq", "reverb", "delay"]`).
     - `"blocks"`: Nested dictionary containing block configurations (e.g., `amplifier`, `cabinet`, `efx`, `delay`, `reverb`, `modulation`, `compressor`, `eq`, `noise_gate`), with `"enabled"` flags and parameter values matching the valid models listed in `mightier_amp_settings.md`[cite: 2].

Provide the final JSON code block along with a brief explanation of the gear choices, research insights, and settings you selected.

```

```

---

## 2. `README.md`

```markdown
# NUX Mighty Amp QR Code Generator & Tone Prompt Toolkit

A repository containing tools for generating NUX Mighty Amp-compatible preset QR codes from human-readable JSON definition files[cite: 1], alongside an LLM prompt workflow to research and generate custom guitar tones based on real-world gear[cite: 2].

---

## Included Files

* **`gen_qr.py`**[cite: 1]: Python script to compile human-readable or raw preset JSON files into high error-correction QR code PNG images (`nux://MightyAmp:...`)[cite: 1] compatible with NUX Mighty Amp devices (such as the Mighty Plug Pro / MP-3)[cite: 1].
* **`mightier_amp_settings.md`**[cite: 2]: Complete machine- and human-readable catalogue of amplifiers, cabinets, effects, parameters, slots, and MIDI CC mappings for the Mighty Plug Pro[cite: 2].
* **`prompt_template.md`**: LLM prompt template designed to guide an AI agent through researching a tone, finding real-world gear equivalents, mapping them against `mightier_amp_settings.md`[cite: 2], and outputting a valid preset JSON file[cite: 1].

---

## Prerequisites & Dependencies

To run the QR code generator script, ensure you have Python 3 installed along with the required PIL and qrcode libraries[cite: 1]:

```bash
pip install qrcode[pil] pillow

```

---

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

```

```