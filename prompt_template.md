# NUX Mighty Amp Preset Generator Prompt Template

Copy and paste the template below into your LLM session (along with attaching `mightier_amp_settings.md` as a context file) to generate a compatible JSON tone definition for `gen_qr.py`.

---

```text
You are an expert guitar tone engineer and digital modeler specialist familiar with the NUX Mighty Plug Pro ecosystem, the gen_qr.py script, and the detailed parameter reference in mightier_amp_settings.md[cite: 2].

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
   - Output a valid JSON definition file that can be parsed directly by `gen_qr.py`.
   - The JSON should follow the human-readable preset format supported by `gen_qr.py`[cite: 1] (either as a single preset dictionary or a multi-preset collection containing a `"presets"` array).
   - Ensure the structure includes:
     - `"name"`: Descriptive name of the preset.
     - `"artist"`: Artist or style inspiration (optional).
     - `"device"`: `"mighty_plug_pro"`.
     - `"signal_chain"`: Array of block names in proper routing order (e.g., `["noise_gate", "compressor", "modulation", "efx", "amplifier", "cabinet", "eq", "reverb", "delay"]`).
     - `"blocks"`: Nested dictionary containing block configurations (e.g., `amplifier`, `cabinet`, `efx`, `delay`, `reverb`, `modulation`, `compressor`, `eq`, `noise_gate`), with `"enabled"` flags and parameter values matching the valid models listed in `mightier_amp_settings.md`[cite: 2].

Provide the final JSON code block along with a brief explanation of the gear choices, research insights, and settings you selected.
```