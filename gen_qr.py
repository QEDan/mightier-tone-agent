#!/usr/bin/env python3
"""
gen_qr.py - Generate NUX Mighty Amp-compatible preset QR codes from JSON.

This script supports both:
  1. Human-readable preset JSON files (with descriptive names for amps, cabs, pedals,
     and settings, such as settings.json or individual preset files).
  2. Legacy raw byte JSON files (containing raw nux_data, nux_data_b64, or device + payload).

Usage:
  # Generate QR code from a single readable preset JSON file:
  python gen_qr.py tones/nitro.json
  python gen_qr.py tones/nitro.json nitro.png

  # Generate QR code from a multi-preset JSON file by name or index:
  python gen_qr.py tones/settings.json -o nitro.png --preset "Nitro - Dick Dale"
  python gen_qr.py tones/settings.json -o funk49.png --preset 0

  # List all presets available in a JSON file:
  python gen_qr.py tones/settings.json --list

  # Generate QR codes for all presets in a multi-preset JSON file:
  python gen_qr.py tones/settings.json --all

  # Dump the compiled low-level byte representation without generating an image:
  python gen_qr.py tones/nitro.json --dump-json

Dependencies:
  pip install qrcode[pil] pillow
"""

import argparse
import base64
import json
import math
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import qrcode
    from PIL import Image
except ImportError:
    print("Missing dependency: please run 'pip install qrcode[pil] pillow'", file=sys.stderr)
    sys.exit(1)

NUX_PREFIX = "nux://MightyAmp:"

# Target Device IDs (default is Mighty Plug Pro / MP-3)
DEVICE_MAP: Dict[str, Tuple[int, int]] = {
    "mighty_plug_pro": (15, 1),
    "plug_pro": (15, 1),
    "mpp": (15, 1),
    "mp-3": (15, 1),
    "mp3": (15, 1),
    "mighty_space": (15, 1),
    "space": (15, 1),
    "mighty_plug_air": (11, 1),
    "plug_air": (11, 1),
    "air": (11, 1),
    "mp-2": (11, 1),
    "mp2": (11, 1),
    "mighty_lite_mk2": (19, 1),
    "lite_mk2": (19, 1),
    "mighty_8bt_mk2": (20, 1),
    "8bt_mk2": (20, 1),
}
DEFAULT_DEVICE_ID = 15
DEFAULT_DEVICE_VERSION = 1

def clean_key(s: Any) -> str:
    """Normalize string key by stripping whitespace, symbols, and lowercase."""
    return "".join(c.lower() for c in str(s) if c.isalnum())

# ---------------------------------------------------------------------------
# Model definitions and lookup dictionaries for Mighty Plug Pro / Mighty Space
# ---------------------------------------------------------------------------

AMPLIFIERS: Dict[str, int] = {
    "jazzclean": 1, "jazz": 1, "jc120": 1,
    "deluxervb": 2, "deluxereverb": 2, "deluxe": 2, "dr": 2,
    "bassmate": 3, "bassman": 3,
    "tweedy": 4, "tweed": 4,
    "twinrvb": 5, "twinreverb": 5, "twin": 5, "tr": 5,
    "hiwire": 6, "hiwatt": 6,
    "calicrunch": 7, "cali": 7,
    "classa15": 8, "ac15": 8,
    "classa30": 9, "ac30": 9,
    "plexi100": 10, "plexi": 10, "superlead": 10,
    "plexi45": 11, "jtm45": 11,
    "brit800": 12, "jcm800": 12,
    "1987x50": 13, "pl1987x50": 13, "1987x": 13,
    "slo100": 14, "slo": 14, "soldano": 14,
    "firemanhbe": 15, "fireman": 15, "friedman": 15, "hbe": 15,
    "dualrect": 16, "recto": 16, "dualrectifier": 16,
    "dievh4": 17, "vh4": 17, "diezel": 17,
    "vibroking": 18,
    "budda": 19,
    "mrz38": 20, "mrz": 20, "drz": 20,
    "superrvb": 21, "superreverb": 21,
    "britblues": 22,
    "matchd30": 23, "matchless": 23,
    "brit2000": 24, "dsl": 24,
    "uberhigain": 25, "uberschall": 25, "bogner": 25,
    "agl": 26, "aguilar": 26,
    "mld": 27,
    "optimaair": 28, "optima": 28, "acoustic": 28,
    "stageman": 29,
}

CABINETS: Dict[str, int] = {
    "jz120": 1, "dr112": 2, "tr212": 3, "hiwire412": 4, "cali112": 5, "a112": 6,
    "gb412": 7, "m1960ax": 8, "1960ax": 8, "1960a": 8, "m1960av": 9, "1960av": 9,
    "m1960tv": 10, "slo412": 11, "fireman412": 12, "rect412": 13, "die412": 14,
    "match212": 15, "uber412": 16, "bs410": 17, "a212": 18, "m1960ahw": 19,
    "m1936": 20, "budda112": 21, "z212": 22, "superverb410": 23, "vibroking310": 24,
    "agldb810": 25, "agl810": 25, "ampsv212": 26, "ampsv410": 27, "ampsv810": 28,
    "bassguy410": 29, "eden410": 30, "mkb410": 31, "ghbird": 32, "gj15": 33, "md45": 34
}

EFX_MODELS: Dict[str, int] = {
    "distortionplus": 1, "distortion": 1, "distplus": 1,
    "rcboost": 2, "rc": 2,
    "acboost": 3, "ac": 3,
    "distone": 4, "ds1": 4,
    "tscreamer": 5, "tsdrive": 5, "tubescreamer": 5, "ts9": 5, "ts808": 5,
    "bluesdrive": 6, "bd2": 6, "bluesdriver": 6,
    "morningdrive": 7, "morningglory": 7,
    "eatdist": 8, "rat": 8,
    "reddirt": 9,
    "crunch": 10,
    "mufffuzz": 11, "bigmuff": 11, "fuzz": 11,
    "katana": 12,
    "stsinger": 13, "steelsinger": 13,
    "touchwah": 14, "autowah": 14
}

COMPRESSORS: Dict[str, int] = {
    "rosecomp": 1, "rose": 1, "dynacomp": 1,
    "kcomp": 2, "keeley": 2,
    "studiocomp": 3, "studio": 3
}

REVERBS: Dict[str, int] = {
    "room": 1, "roomreverb": 1,
    "hall": 2, "hallreverb": 2,
    "plate": 3, "platereverb": 3,
    "spring": 4, "springreverb": 4,
    "shimmer": 5, "shimmerreverb": 5,
    "damp": 6, "dampreverb": 6
}

DELAYS: Dict[str, int] = {
    "analog": 1, "analogdelay": 1, "dm2": 1,
    "digital": 2, "digitaldelay": 2, "dd2": 2,
    "moddelay": 3, "modulation": 3,
    "tapeecho": 4, "tape": 4,
    "pandelay": 5, "pan": 5,
    "phidelay": 6, "phi": 6
}

MODULATIONS: Dict[str, int] = {
    "ce1": 1, "ce2": 2, "stchorus": 3, "vibrato": 4, "detune": 5, "flanger": 6,
    "phase90": 7, "phase100": 8, "scf": 9, "uvibe": 10, "vibe": 10, "tremolo": 11,
    "rotary": 12, "sch1": 13, "monooctave": 14, "octave": 14
}

FX_ROUTING_MAP: Dict[str, int] = {
    "wah": 0, "comp": 1, "cmp": 1, "compressor": 1, "efx": 2, "drive": 2,
    "distortion": 2, "boost": 2, "amp": 3, "amplifier": 3, "eq": 4,
    "ng": 5, "gate": 5, "noisegate": 5, "noise_gate": 5, "mod": 6,
    "modulation": 6, "dly": 7, "delay": 7, "rvb": 8, "reverb": 8,
    "cab": 9, "cabinet": 9, "ir": 9, "sr": 10, "sendreturn": 10, "send_return": 10
}

# ---------------------------------------------------------------------------
# Value parsing and scaling helpers
# ---------------------------------------------------------------------------

def parse_num(v: Any, default: float = 0.0) -> float:
    """Parse numeric values from numbers, strings, or descriptive presets."""
    if v is None:
        return default
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().lower()
        m = re.match(r"^([+-]?[0-9]+(?:\.[0-9]+)?)", s)
        if m:
            try:
                num = float(m.group(1))
                if "khz" in s:
                    num *= 1000.0
                return num
            except ValueError:
                pass
        # Context-dependent descriptive words:
        if s in ("short", "fast", "min", "minimum", "low"):
            return 30.0
        if s in ("medium", "mid", "default", "normal"):
            return 50.0
        if s in ("long", "slow", "max", "maximum", "high"):
            return 70.0
        if "ear" in s or "hum" in s:
            return 30.0
    return default

def clamp_byte(v: Any) -> int:
    return max(0, min(255, int(round(float(v)))))

def low_cut_to_byte(val: Any) -> int:
    """Map Low Cut parameter (Hz or 0..100) to preset byte value."""
    if val is None:
        return 0
    num = parse_num(val, 20.0)
    if num <= 100.0:
        return clamp_byte(num)
    # Range is 20 Hz to 300 Hz
    return max(0, min(100, int((num - 20.0) / 280.0 * 100.0)))

def high_cut_to_byte(val: Any) -> int:
    """Map High Cut parameter (Hz or 0..100) to preset byte value."""
    if val is None:
        return 100
    num = parse_num(val, 20000.0)
    if num <= 100.0:
        return clamp_byte(num)
    try:
        f = max(5000.0, min(20000.0, float(num)))
        a = math.log10(f)
        res = (a - math.log10(5000.0)) / (math.log10(20000.0) - math.log10(5000.0)) * 100.0
        return max(0, min(100, int(round(res))))
    except Exception:
        return 100

def eq_band_to_byte(val: Any) -> int:
    """Handle EQ band values in dB (-15..+15) or 0..100."""
    num = parse_num(val, 0.0)
    if -15.0 <= num <= 15.0:
        return clamp_byte(50.0 + num)
    return clamp_byte(num)

# ---------------------------------------------------------------------------
# High-level preset compiler for Mighty Plug Pro
# ---------------------------------------------------------------------------

def compile_readable_preset(preset: Dict[str, Any], default_dev_id: int = DEFAULT_DEVICE_ID) -> bytes:
    """Compile a human-readable preset dictionary into a valid NUX byte array."""
    # Resolve device ID and version
    dev_field = preset.get("device")
    dev_id = default_dev_id
    dev_ver = DEFAULT_DEVICE_VERSION

    if isinstance(dev_field, dict):
        dev_id = dev_field.get("id", dev_id)
        dev_ver = dev_field.get("version", dev_ver)
    elif isinstance(dev_field, str):
        lookup = DEVICE_MAP.get(clean_key(dev_field))
        if lookup:
            dev_id, dev_ver = lookup
    elif isinstance(dev_field, int):
        dev_id = dev_field

    data = [0] * 113
    blocks = preset.get("blocks", {})
    other_blocks = preset.get("other_blocks", {})

    def is_block_enabled(b_dict: Optional[Dict[str, Any]], block_name: str) -> bool:
        if not b_dict:
            c = clean_key(block_name)
            for k, v in other_blocks.items():
                if clean_key(k) == c:
                    return bool(v)
            return False
        return bool(b_dict.get("enabled", True))

    # 1. Noise Gate
    ng = blocks.get("noise_gate", blocks.get("ng", blocks.get("gate", {})))
    ng_on = is_block_enabled(ng, "noise_gate")
    data[5] = 1 | (0 if ng_on else 0x40)
    data[49] = clamp_byte(parse_num(ng.get("threshold"), 30.0))
    data[50] = clamp_byte(parse_num(ng.get("decay"), 30.0))

    # 2. Compressor
    cmp_b = blocks.get("compressor", blocks.get("cmp", blocks.get("comp", {})))
    cmp_on = is_block_enabled(cmp_b, "compressor")
    c_model = clean_key(cmp_b.get("model", "rosecomp"))
    c_idx = COMPRESSORS.get(c_model, 1)
    data[1] = c_idx | (0 if cmp_on else 0x40)
    if c_idx == 1:  # Rose Comp
        data[15] = clamp_byte(parse_num(cmp_b.get("sustain"), 50.0))
        data[16] = clamp_byte(parse_num(cmp_b.get("level"), 50.0))
    elif c_idx == 2:  # K Comp
        data[15] = clamp_byte(parse_num(cmp_b.get("sustain"), 50.0))
        data[16] = clamp_byte(parse_num(cmp_b.get("level"), 50.0))
        data[17] = clamp_byte(parse_num(cmp_b.get("clipping", cmp_b.get("clip")), 50.0))
    elif c_idx == 3:  # Studio Comp
        data[15] = clamp_byte(parse_num(cmp_b.get("threshold"), 50.0))
        data[16] = clamp_byte(parse_num(cmp_b.get("ratio"), 50.0))
        data[17] = clamp_byte(parse_num(cmp_b.get("gain"), 50.0))
        data[18] = clamp_byte(parse_num(cmp_b.get("release"), 50.0))

    # 3. EFX
    efx = blocks.get("efx", blocks.get("drive", blocks.get("distortion", blocks.get("boost", {}))))
    efx_on = is_block_enabled(efx, "efx")
    e_model = clean_key(efx.get("model", "rcboost"))
    e_idx = EFX_MODELS.get(e_model, 2)
    data[2] = e_idx | (0 if efx_on else 0x40)
    if e_idx in (2, 3):  # RC Boost / AC Boost
        data[20] = clamp_byte(parse_num(efx.get("gain", efx.get("drive")), 35.0))
        data[21] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 40.0))
        data[22] = clamp_byte(parse_num(efx.get("bass"), 35.0))
        data[23] = clamp_byte(parse_num(efx.get("treble"), 70.0))
    elif e_idx in (4, 5, 6, 7, 9):  # Dist One, TS Drive, Blues Drive, Morning Drive, Red Dirt
        data[20] = clamp_byte(parse_num(efx.get("drive", efx.get("gain")), 50.0))
        data[21] = clamp_byte(parse_num(efx.get("tone", efx.get("filter")), 50.0))
        data[22] = clamp_byte(parse_num(efx.get("level", efx.get("volume")), 50.0))
    elif e_idx == 8:  # Eat Dist (Rat)
        data[20] = clamp_byte(parse_num(efx.get("distortion", efx.get("drive")), 65.0))
        data[21] = clamp_byte(parse_num(efx.get("filter", efx.get("tone")), 70.0))
        data[22] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 60.0))
    elif e_idx == 10:  # Crunch
        data[20] = clamp_byte(parse_num(efx.get("gain", efx.get("drive")), 50.0))
        data[21] = clamp_byte(parse_num(efx.get("tone"), 50.0))
        data[22] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 50.0))
    elif e_idx == 11:  # Muff Fuzz
        data[20] = clamp_byte(parse_num(efx.get("sustain", efx.get("drive")), 50.0))
        data[21] = clamp_byte(parse_num(efx.get("tone"), 50.0))
        data[22] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 50.0))
    elif e_idx == 12:  # Katana
        data[20] = clamp_byte(parse_num(efx.get("boost", efx.get("gain")), 0.0))
        data[21] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 45.0))
    elif e_idx == 13:  # ST Singer
        data[20] = clamp_byte(parse_num(efx.get("gain", efx.get("drive")), 50.0))
        data[21] = clamp_byte(parse_num(efx.get("volume", efx.get("level")), 50.0))
        data[22] = clamp_byte(parse_num(efx.get("filter", efx.get("tone")), 50.0))
    elif e_idx == 14:  # Touch Wah
        data[20] = clamp_byte(parse_num(efx.get("type"), 1.0))
        data[21] = clamp_byte(parse_num(efx.get("sense"), 90.0))
        data[22] = clamp_byte(parse_num(efx.get("wow"), 35.0))
        data[23] = clamp_byte(parse_num(efx.get("direction", efx.get("updown")), 0.0))
        data[24] = clamp_byte(parse_num(efx.get("level"), 100.0))
    else:  # Distortion+
        data[20] = clamp_byte(parse_num(efx.get("distortion", efx.get("drive")), 50.0))
        data[21] = clamp_byte(parse_num(efx.get("output", efx.get("level", efx.get("volume"))), 50.0))

    # 4. Amplifier
    amp = blocks.get("amplifier", blocks.get("amp", {}))
    amp_on = is_block_enabled(amp, "amplifier")
    a_model = clean_key(amp.get("model", "deluxervb"))
    a_idx = AMPLIFIERS.get(a_model, 2)
    data[3] = a_idx | (0 if amp_on else 0x40)
    data[27] = clamp_byte(parse_num(amp.get("gain"), 50.0))
    data[28] = clamp_byte(parse_num(amp.get("master"), 50.0))
    data[29] = clamp_byte(parse_num(amp.get("bass"), 50.0))
    data[30] = clamp_byte(parse_num(amp.get("middle", amp.get("mid")), 50.0))
    data[31] = clamp_byte(parse_num(amp.get("treble"), 50.0))
    p6_val = amp.get("bright", amp.get("presence", amp.get("tone", amp.get("cut", amp.get("mid_freq", amp.get("midfreq"))))))
    data[32] = clamp_byte(parse_num(p6_val, 0.0))

    # 5. EQ
    eq = blocks.get("eq", {})
    eq_on = is_block_enabled(eq, "eq")
    eq_model = clean_key(eq.get("model", "6band"))
    eq_idx = 3 if "10" in eq_model else 1
    data[4] = eq_idx | (0 if eq_on else 0x40)
    if eq_idx == 1:  # 6-Band
        data[36] = eq_band_to_byte(eq.get("band_100hz", eq.get("100", 0.0)))
        data[37] = eq_band_to_byte(eq.get("band_220hz", eq.get("220", 0.0)))
        data[38] = eq_band_to_byte(eq.get("band_500hz", eq.get("500", 0.0)))
        data[39] = eq_band_to_byte(eq.get("band_1200hz", eq.get("1200", eq.get("1.2k", 0.0))))
        data[40] = eq_band_to_byte(eq.get("band_2600hz", eq.get("2600", eq.get("2.6k", 0.0))))
        data[41] = eq_band_to_byte(eq.get("band_6400hz", eq.get("6400", eq.get("6.4k", 0.0))))
        for b in range(42, 48):
            data[b] = 50
    else:  # 10-Band
        data[36] = eq_band_to_byte(eq.get("vol", 0.0))
        freqs = ["31", "62", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"]
        for i, fr in enumerate(freqs):
            data[37 + i] = eq_band_to_byte(eq.get(f"band_{fr}", eq.get(fr, 0.0)))

    # 6. Cabinet
    cab = blocks.get("cabinet", blocks.get("cab", blocks.get("ir", {})))
    cab_on = is_block_enabled(cab, "cabinet")
    c_model = clean_key(cab.get("model", "dr112"))
    cab_idx = CABINETS.get(c_model, 2)
    data[9] = cab_idx | (0 if cab_on else 0x40)
    data[78] = clamp_byte(parse_num(cab.get("level"), 0.0))
    data[79] = low_cut_to_byte(cab.get("low_cut_hz", cab.get("low_cut", 20.0)))
    data[80] = high_cut_to_byte(cab.get("high_cut_hz", cab.get("high_cut", 20000.0)))

    # 7. Reverb
    rvb = blocks.get("reverb", blocks.get("rvb", {}))
    rvb_on = is_block_enabled(rvb, "reverb")
    r_model = clean_key(rvb.get("model", "room"))
    r_idx = REVERBS.get(r_model, 1)
    data[8] = r_idx | (0 if rvb_on else 0x40)
    if r_idx in (3, 4):  # Plate / Spring
        data[70] = clamp_byte(parse_num(rvb.get("decay"), 50.0))
        data[71] = clamp_byte(parse_num(rvb.get("level", rvb.get("mix")), 50.0))
    elif r_idx == 1:  # Room
        data[70] = clamp_byte(parse_num(rvb.get("decay"), 50.0))
        data[71] = clamp_byte(parse_num(rvb.get("tone"), 50.0))
        data[72] = clamp_byte(parse_num(rvb.get("level", rvb.get("mix")), 50.0))
    elif r_idx == 2:  # Hall
        data[70] = clamp_byte(parse_num(rvb.get("decay"), 50.0))
        data[71] = clamp_byte(parse_num(rvb.get("predelay", rvb.get("pre_delay")), 50.0))
        data[72] = clamp_byte(parse_num(rvb.get("liveliness"), 50.0))
        data[73] = clamp_byte(parse_num(rvb.get("level", rvb.get("mix")), 50.0))
    elif r_idx == 5:  # Shimmer
        data[70] = clamp_byte(parse_num(rvb.get("mix", rvb.get("level")), 50.0))
        data[71] = clamp_byte(parse_num(rvb.get("decay"), 50.0))
        data[72] = clamp_byte(parse_num(rvb.get("shimmer"), 50.0))
    elif r_idx == 6:  # Damp
        data[70] = clamp_byte(parse_num(rvb.get("mix", rvb.get("level")), 50.0))
        data[71] = clamp_byte(parse_num(rvb.get("depth"), 50.0))

    # 8. Delay
    dly = blocks.get("delay", blocks.get("dly", {}))
    dly_on = is_block_enabled(dly, "delay")
    d_model = clean_key(dly.get("model", "analog"))
    d_idx = DELAYS.get(d_model, 1)
    data[7] = d_idx | (0 if dly_on else 0x40)
    data[61] = clamp_byte(parse_num(dly.get("time", dly.get("rate", dly.get("e_level"))), 50.0))
    data[62] = clamp_byte(parse_num(dly.get("repeat", dly.get("feedback", dly.get("time"))), 50.0))
    data[63] = clamp_byte(parse_num(dly.get("level", dly.get("intensity", dly.get("echo", dly.get("mix")))), 50.0))
    if "mod" in dly:
        data[64] = clamp_byte(parse_num(dly["mod"], 50.0))

    # 9. Modulation
    mod = blocks.get("modulation", blocks.get("mod", {}))
    mod_on = is_block_enabled(mod, "modulation")
    m_model = clean_key(mod.get("model", "ce1"))
    m_idx = MODULATIONS.get(m_model, 1)
    data[6] = m_idx | (0 if mod_on else 0x40)
    data[54] = clamp_byte(parse_num(mod.get("rate", mod.get("speed", mod.get("level", mod.get("intensity")))), 50.0))
    data[55] = clamp_byte(parse_num(mod.get("depth", mod.get("width", mod.get("volume"))), 50.0))
    data[56] = clamp_byte(parse_num(mod.get("intensity", mod.get("tone", mod.get("mode"))), 50.0))
    if "feedback" in mod:
        data[57] = clamp_byte(parse_num(mod["feedback"], 50.0))

    # 10. Master volume & BPM
    data[84] = clamp_byte(parse_num(preset.get("master"), 50.0))
    bpm = clamp_byte(parse_num(preset.get("bpm"), 120.0))
    data[86] = 0
    data[87] = bpm

    # 11. Signal chain routing (LINK1..11, bytes 89..99)
    chain = preset.get("signal_chain", [])
    default_order = [5, 1, 6, 2, 3, 9, 4, 8, 7]  # NG, CMP, MOD, EFX, AMP, CAB, EQ, RVB, DLY
    used_ids: List[int] = []
    for item in chain:
        fid = FX_ROUTING_MAP.get(clean_key(item))
        if fid is not None and fid not in used_ids:
            used_ids.append(fid)
    for fid in default_order:
        if fid not in used_ids:
            used_ids.append(fid)
    for i in range(11):
        data[89 + i] = used_ids[i] if i < len(used_ids) else 0

    return bytes([dev_id & 0xFF, dev_ver & 0xFF] + data)

# ---------------------------------------------------------------------------
# Input Dispatcher
# ---------------------------------------------------------------------------

def validate_byte_list(lst: List[int]) -> None:
    if not isinstance(lst, list):
        raise ValueError("byte list must be a JSON array")
    for i, v in enumerate(lst):
        if not isinstance(v, int):
            raise ValueError(f"nux data element at index {i} is not an integer")
        if v < 0 or v > 255:
            raise ValueError(f"nux data element at index {i} is out of byte range (0..255): {v}")

def build_nux_bytes_from_json(obj: Any, preset_selector: Optional[Union[str, int]] = None, override_device: Optional[str] = None) -> Tuple[bytes, str]:
    """
    Parse any JSON format (human-readable preset, multi-preset, or legacy byte array)
    and return (compiled_bytes, preset_name).
    """
    # 1. Check if multi-preset collection
    if isinstance(obj, dict) and "presets" in obj and isinstance(obj["presets"], list):
        presets = obj["presets"]
        if not presets:
            raise ValueError("presets array in JSON is empty")
        selected_preset = None
        if preset_selector is not None:
            # Check integer index
            if isinstance(preset_selector, int) or (isinstance(preset_selector, str) and preset_selector.isdigit()):
                idx = int(preset_selector)
                if 0 <= idx < len(presets):
                    selected_preset = presets[idx]
                else:
                    raise IndexError(f"Preset index {idx} out of range (0..{len(presets) - 1})")
            else:
                target_name = clean_key(preset_selector)
                for p in presets:
                    if clean_key(p.get("name", "")) == target_name:
                        selected_preset = p
                        break
                if not selected_preset:
                    available = [p.get("name", f"Index {i}") for i, p in enumerate(presets)]
                    raise ValueError(f"Preset '{preset_selector}' not found. Available presets: {available}")
        else:
            selected_preset = presets[0]

        name = selected_preset.get("name", "Preset")
        dev_id = DEFAULT_DEVICE_ID
        if override_device:
            dev_id = DEVICE_MAP.get(clean_key(override_device), (DEFAULT_DEVICE_ID, 1))[0]
        return compile_readable_preset(selected_preset, default_dev_id=dev_id), name

    # 2. Check if wrapped single preset
    if isinstance(obj, dict) and "preset" in obj and isinstance(obj["preset"], dict):
        obj = obj["preset"]

    # 3. Check if human-readable preset (contains "blocks" or "signal_chain" or "amplifier")
    if isinstance(obj, dict) and ("blocks" in obj or "signal_chain" in obj or "amplifier" in obj):
        name = obj.get("name", "Preset")
        dev_id = DEFAULT_DEVICE_ID
        if override_device:
            dev_id = DEVICE_MAP.get(clean_key(override_device), (DEFAULT_DEVICE_ID, 1))[0]
        return compile_readable_preset(obj, default_dev_id=dev_id), name

    # 4. Legacy format: raw nux_data
    if isinstance(obj, dict) and "nux_data" in obj:
        lst = obj["nux_data"]
        validate_byte_list(lst)
        return bytes(lst), "Raw nux_data"

    # 5. Legacy format: nux_data_b64
    if isinstance(obj, dict) and "nux_data_b64" in obj:
        if not isinstance(obj["nux_data_b64"], str):
            raise ValueError("nux_data_b64 must be a base64 string")
        data = base64.b64decode(obj["nux_data_b64"], validate=True)
        return data, "Raw base64"

    # 6. Legacy format: device + payload
    if isinstance(obj, dict) and "device" in obj and "payload" in obj:
        dev = obj["device"]
        if not isinstance(dev, dict) or "id" not in dev or "version" not in dev:
            raise ValueError("device object must contain 'id' and 'version'")
        did = dev["id"]
        ver = dev["version"]
        payload = obj["payload"]
        validate_byte_list(payload)
        return bytes([did & 0xFF, ver & 0xFF] + payload), "Device payload"

    raise ValueError(
        "Unrecognized JSON structure. Expected either a human-readable preset "
        "(with 'blocks' or 'presets'), or raw bytes ('nux_data', 'nux_data_b64', 'device'+'payload')."
    )

# ---------------------------------------------------------------------------
# QR Code Generator
# ---------------------------------------------------------------------------

def generate_qr_image(data_bytes: bytes, box_size: int = 10, border: int = 4) -> Image.Image:
    """Generate a high error-correction PIL Image (QR code) for Mighty Amp."""
    b64 = base64.b64encode(data_bytes).decode("ascii")
    content = NUX_PREFIX + b64

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a Mighty Amp preset QR code PNG from readable or raw JSON.")
    parser.add_argument("input", nargs="?", help="Input JSON file (preset, multi-preset, or raw). Use '-' for stdin.")
    parser.add_argument("output", nargs="?", help="Output PNG file path.")
    parser.add_argument("-i", "--input-file", dest="opt_input", help="Optional explicit input file path.")
    parser.add_argument("-o", "--output-file", dest="opt_output", help="Optional explicit output file path.")
    parser.add_argument("-p", "--preset", help="Select preset by name or index from a multi-preset file.")
    parser.add_argument("-l", "--list", action="store_true", help="List all presets in the input file and exit.")
    parser.add_argument("-a", "--all", action="store_true", help="Generate QR codes for all presets in a multi-preset file.")
    parser.add_argument("-d", "--device", help="Target device (default: 'plug_pro' / id 15). Options: plug_pro, plug_air, space, lite_mk2, 8bt_mk2.")
    parser.add_argument("--box-size", type=int, default=10, help="QR pixel size of one box (default 10).")
    parser.add_argument("--border", type=int, default=4, help="QR border boxes (default 4).")
    parser.add_argument("--dump-json", action="store_true", help="Dump compiled raw bytes structure to stdout instead of image.")
    args = parser.parse_args(argv)

    input_path = args.opt_input or args.input
    output_path = args.opt_output or args.output

    if not input_path:
        parser.print_help()
        sys.exit(2)

    # Load JSON
    if input_path == "-":
        obj = json.load(sys.stdin)
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            obj = json.load(f)

    # Handle --list
    if args.list:
        if isinstance(obj, dict) and "presets" in obj and isinstance(obj["presets"], list):
            print(f"Presets found in {input_path} ({len(obj['presets'])} total):")
            for i, p in enumerate(obj["presets"]):
                name = p.get("name", "Unnamed")
                artist = p.get("artist", "")
                details = f" - {artist}" if artist else ""
                print(f"  [{i}] {name}{details}")
        elif isinstance(obj, dict) and ("name" in obj or "blocks" in obj):
            print(f"Single preset in {input_path}: '{obj.get('name', 'Unnamed')}'")
        else:
            print(f"No named presets found in {input_path} (raw byte format).")
        sys.exit(0)

    # Handle --all
    if args.all:
        if not (isinstance(obj, dict) and "presets" in obj and isinstance(obj["presets"], list)):
            print("Error: --all requires an input file with a 'presets' array.", file=sys.stderr)
            sys.exit(1)
        presets = obj["presets"]
        out_dir = os.path.dirname(output_path) if output_path else "."
        for i, p in enumerate(presets):
            nux_bytes, name = build_nux_bytes_from_json(obj, preset_selector=i, override_device=args.device)
            safe_name = re.sub(r"[^\w\-_]", "_", name.lower().strip())
            file_name = f"{safe_name}.png"
            target = os.path.join(out_dir, file_name)
            img = generate_qr_image(nux_bytes, box_size=args.box_size, border=args.border)
            img.save(target)
            print(f"[{i+1}/{len(presets)}] Saved '{name}' -> {target} ({len(nux_bytes)} bytes, device id {nux_bytes[0]})")
        sys.exit(0)

    # Single QR generation
    try:
        nux_bytes, name = build_nux_bytes_from_json(obj, preset_selector=args.preset, override_device=args.device)
    except Exception as e:
        print(f"Error processing preset: {e}", file=sys.stderr)
        sys.exit(1)

    if args.dump_json:
        dump_data = {
            "device": {"id": nux_bytes[0], "version": nux_bytes[1]},
            "payload": list(nux_bytes[2:]),
            "nux_data_b64": base64.b64encode(nux_bytes).decode("ascii")
        }
        print(json.dumps(dump_data, indent=2))
        sys.exit(0)

    if not output_path:
        print("Error: Output PNG file path is required. Use: python gen_qr.py input.json output.png", file=sys.stderr)
        sys.exit(2)

    img = generate_qr_image(nux_bytes, box_size=args.box_size, border=args.border)
    img.save(output_path)
    print(f"Wrote QR for '{name}' to {output_path} (device id {nux_bytes[0]}, payload {len(nux_bytes)} bytes)")

if __name__ == "__main__":
    main()