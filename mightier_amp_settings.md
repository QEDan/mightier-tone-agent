# Mighty Plug Pro — Complete Effect & Parameter Reference

A machine- and human-readable catalogue of every amplifier, cabinet and effect exposed by
the Mighty Plug Pro (NUX), with default values, device slot mappings, MIDI CC assignments
and the real-world gear each model emulates.

---

## 0. Provenance and licensing

This document merges three kinds of source material, which carry **different licences**:

| Material | Origin | Licence |
|---|---|---|
| Effect/parameter definitions | `mighty_plug_manager` Dart sources (`Amps.dart`, `Cabinet.dart`, `Compressor.dart`, `Delay.dart`, `EFX.dart`, `EmptyEffects.dart`, `EQ.dart`, `Modulation.dart`, `Reverb.dart`, `ValueFormatter.dart`, `NuxConstants.dart`) © 2020–2022 Dian Iliev (Tuntorius) | MIT |
| "Based on" gear attributions | *NUX Mighty Plug Pro Effects Reference*, © 2024 Blrfl Labs | CC BY-NC-SA 4.0 |
| Structure and editorial notes | This compilation | inherits the above |

**Attribution notice for the gear chart:** the "Based on" data is reproduced from the
*NUX Mighty Plug Pro Effects Reference* by Blrfl Labs (labs@blrfl.com), licensed
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International —
<https://creativecommons.org/licenses/by-nc-sa/4.0>.

⚠️ **Practical consequence:** the CC BY-NC-SA terms are *non-commercial* and *share-alike*.
If you redistribute this markdown (or a derivative), the "Based on" columns must retain the
attribution above and any derivative must be released under the same licence. If you need a
permissively licensed version, drop the "Based on" columns and keep only the MIT-licensed
Dart data.

**Firmware coverage.** The gear chart spans two firmware revisions: the GATE / CMP / MOD /
EFX / DLY / RVB / EQ chart is from **20240711**, while the AMP / IR chart is from
**20230320**. Where the two disagree with the Dart sources, see §14.

---

## 1. How to read this file

### 1.1 Processing blocks

The device exposes **eleven** block "heads" (indices 0–10). Nine have definitions in the
supplied Dart files; two do not.

| Idx | Block | Head constant | Definitions supplied? | Editor UI | Enable mask | Enable inverted |
|---|---|---|---|---|---|---|
| 0 | Wah | `Head_iWAH` | yes (stub only) | Sliders | `0x40` | yes |
| 1 | Compressor | `Head_iCMP` | yes | Sliders | `0x40` | yes |
| 2 | Effect / drive | `Head_iEFX` | yes | Sliders | `0x40` | yes |
| 3 | Amplifier | `Head_iAMP` | yes | Sliders | `0x40` | yes |
| 4 | EQ | `Head_iEQ` | yes | **EQ** | `0x40` | yes |
| 5 | Noise gate | `Head_iNG` | **no** | — | — | — |
| 6 | Modulation | `Head_iMOD` | yes | Sliders | `0x40` | yes |
| 7 | Delay | `Head_iDLY` | yes | Sliders | `0x40` | yes |
| 8 | Reverb | `Head_iRVB` | yes | Sliders | `0x40` | yes |
| 9 | Cabinet / IR | `Head_iCAB` | yes | Sliders | `0x40` | yes |
| 10 | Send / Return | `Head_iSR` | **no** | — | — | — |

The app's canonical block order is declared as
`effectTypesIndex = [CMP, EFX, AMP, EQ, NG, MOD, DLY, RVB, CAB]` → `[1, 2, 3, 4, 5, 6, 7, 8, 9]`,
with `defaultEffects = [gate, comp, mod, efx, amp, cab, eq, reverb, delay]`.

Every defined block also exposes MIDI foot-controller handles for
**Off / On / Toggle / Prev / Next**.

### 1.2 Parameter slots — the join key

Each parameter carries a `devicePresetIndex` naming its byte in the preset payload, and a
`midiCC` naming its control-change number. Both resolve to plain integers (§13). Tables in
§4–§12 use the shorthand `P1`…`P12` for `*_Para1`…`*_Para12`.

> **Convention:** the `Slots` column lists slots **in the same order as the parameters** in
> the adjacent column. To resolve a slot to a byte offset or CC number, look it up in §13.

### 1.3 Value formatters

Defaults below are the **raw integers** stored in the preset, exactly as written in the
source. The formatter attached to a parameter converts that integer into a displayed unit.
The formatter classes are registered in `ValueFormatter.dart`; their numeric limits are
defined in separate files **not supplied here**.

Abstract base class contract:

| Member | Value |
|---|---|
| `inputType` | abstract — `InputType.SliderInput` or `InputType.SwitchInput` |
| `min` | `0` (base default) |
| `max` | `100` (base default) |
| `valueToMidi7Bit(double)` | abstract |
| `midi7BitToValue(int)` | abstract |
| `toLabel(double)` | abstract |
| `toHumanInput(double)` | identity by default |
| `fromHumanInput(double)` | identity by default |

> **Inference (labelled):** the presence of `valueToMidi7Bit` / `midi7BitToValue` implies
> values are quantised to 7-bit MIDI (0–127) on the wire regardless of display range. The
> base `min`/`max` of 0/100 are overridden by subclasses; the actual per-formatter limits
> are **unknown** from the supplied files.

Registry of formatter instances, with the source file each is imported from:

| Instance | Class | Defined in (per imports) | Used by effects here? |
|---|---|---|---|
| `percentage` | `PercentageFormatter` | `PercentageFormatter.dart` | no |
| `percentageMPPro` | `PercentageFormatterMPPro` | `PercentageFormatter.dart` | **yes** |
| `decibelMP2` | `DecibelFormatterMP2` | `DecibelFormatter.dart` | no |
| `decibelMPPro` | `DecibelFormatterMPPro` | `DecibelFormatter.dart` | **yes** |
| `decibelEQ` | `DecibelFormatterEQ` | `DecibelFormatter.dart` | **yes** |
| `tempo` | `TempoFormatter` | `TempoFormatter.dart` | no |
| `tempoPro` | `TempoFormatterPro` | `TempoFormatter.dart` | **yes** |
| `tempoProMod` | `TempoFormatterProMod` | `TempoFormatter.dart` | **yes** |
| `tempoProAnalog` | `TempoFormatterProAnalog` | `TempoFormatter.dart` | **yes** |
| `tempoProTapeEcho` | `TempoFormatterProTapeEcho` | `TempoFormatter.dart` | **yes** |
| `brightMode` | `BrightModeFormatter` | `SwitchFormatters.dart` | no |
| `brightModePro` | `BrightModeFormatterMPPro` | `SwitchFormatters.dart` | **yes** |
| `boostMode` | `BoostModeFormatter` | `SwitchFormatters.dart` | no |
| `boostModePro` | `BoostModeFormatterMPPro` | `SwitchFormatters.dart` | **yes** |
| `vibeMode` | `VibeModeFormatter` | `SwitchFormatters.dart` | no |
| `vibeModePro` | `VibeModeFormatterPro` | `SwitchFormatters.dart` | **yes** |
| `contourMode` | `ContourModeFormatter` | `SwitchFormatters.dart` | no |
| `scfMode` | `SCFModeFormatter` | `SwitchFormatters.dart` | **yes** |
| `lowFreqFormatter` | `LowFrequencyFormatter` | `FrequencyFormatter.dart` | **yes** |
| `highFreqFormatter` | `HighFrequencyFormatter` | `FrequencyFormatter.dart` | **yes** |
| `touchWahFormatter` | `TouchWahModeFormatter` | `SwitchFormatters.dart` | no |
| `touchWahFormatterLiteMk2` | `TouchWahModeFormatterLiteMk2` | `SwitchFormatters.dart` | **yes** |
| `touchWahDirectionFormatterPro` | `TouchWahDirectionFormatterPro` | `SwitchFormatters.dart` | **yes** |

> **Inference (labelled):** the discrete-valued formatters (`brightModePro`, `boostModePro`,
> `vibeModePro`, `scfMode`, `touchWahFormatterLiteMk2`, `touchWahDirectionFormatterPro`)
> are the likely `SwitchInput` members; continuous ones are likely `SliderInput`. The
> per-class assignment is not visible in `ValueFormatter.dart`.

### 1.4 Group headings

Entries declaring `isSeparator = true` plus a `category` string appear to act as group
headings in the effect picker. This is an inference from the field names, not stated in
the source.

---

## 2. Amplifiers

29 amplifiers, `nuxIndex` 1–29, family `PlugProAmplifier`. Slots `AMP_Para1`…`AMP_Para6`
are used; `AMP_Para7`/`AMP_Para8` are defined in the protocol but unused by any model here.
Every `Master` parameter is flagged `masterVolume: true`; no other parameter anywhere in
these files carries that flag.

| # | Amp | Category | Based on (Blrfl) | Default cab | Parameters (default) | Slots |
|---|---|---|---|---|---|---|
| 1 | Jazz Clean | Guitar | Roland JC-120 | JZ120 | Gain 65 · Master 70 · Bass 50 · Middle 65 · Treble 55 · Bright 1 | P1 P2 P3 P4 P5 P6 |
| 2 | Deluxe Rvb | Guitar | Fender Deluxe Reverb | DR112 | Gain 65 · Master 80 · Bass 50 · Middle 70 · Treble 60 | P1 P2 P3 P4 P5 |
| 3 | Bass Mate | Bass | Fender Tweed Bassman `[B]` | BS410 | Gain 60 · Master 85 · Bass 60 · Middle 70 · Treble 55 · Presence 100 | P1 P2 P3 P4 P5 P6 |
| 4 | Tweedy | Guitar | Fender Tweed Deluxe | DR112 | Gain 78 · Master 80 · Tone 68 | P1 P2 P6 |
| 5 | Twin Reverb | Guitar | Fender Twin Reverb | TR212 | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Bright 1 | P1 P2 P3 P4 P5 P6 |
| 6 | Hiwire | Guitar | Hiwatt DR103 | HIWIRE412 | Gain 50 · Master 76 · Bass 75 · Middle 62 · Treble 50 · Presence 54 | P1 P2 P3 P4 P5 P6 |
| 7 | Cali Crunch | Guitar | Mesa/Boogie (unspecified) | CALI 112 | Gain 60 · Master 92 · Bass 42 · Middle 59 · Treble 66 · Presence 49 | P1 P2 P3 P4 P5 P6 |
| 8 | Class A15 | Guitar | VOX AC15 | A112 | Gain 50 · Master 50 · Bass 50 · Treble 50 · Cut 50 | P1 P2 P3 P5 P6 |
| 9 | Class A30 | Guitar | VOX AC30 | A212 | Gain 50 · Master 80 · Bass 60 · Treble 60 · Cut 40 | P1 P2 P3 P5 P6 |
| 10 | Plexi 100 | Guitar | Marshall 1959 | GB412 | Gain 71 · Master 66 · Bass 60 · Middle 62 · Treble 53 · Presence 67 | P1 P2 P3 P4 P5 P6 |
| 11 | Plexi 45 | Guitar | Marshall JTM45 | GB412 | Gain 26 · Master 53 · Bass 60 · Middle 62 · Treble 53 · Presence 67 | P1 P2 P3 P4 P5 P6 |
| 12 | Brit 800 | Guitar | Marshall JCM800 | M1960AV | Gain 44 · Master 81 · Bass 35 · Middle 71 · Treble 52 · Presence 58 | P1 P2 P3 P4 P5 P6 |
| 13 | 1987x50 | Guitar | Marshall 1987X | M1960TV | Gain 44 · Master 81 · Bass 35 · Middle 71 · Treble 52 · Presence 58 | P1 P2 P3 P4 P5 P6 |
| 14 | Slo 100 | Guitar | Soldano SLO-100 | SLO412 | Gain 44 · Master 81 · Bass 35 · Middle 71 · Treble 52 · Presence 58 | P1 P2 P3 P4 P5 P6 |
| 15 | Fireman HBE | Guitar | Friedman BE-100 | FIREMAN 412 | Gain 70 · Master 77 · Bass 55 · Middle 65 · Treble 60 · Presence 70 | P1 P2 P3 P4 P5 P6 |
| 16 | Dual Rect | Guitar | Mesa/Boogie Dual Rectifier | RECT 412 | Gain 60 · Master 70 · Bass 55 · Middle 65 · Treble 50 · Presence 65 | P1 P2 P3 P4 P5 P6 |
| 17 | DIE VH4 | Guitar | Diezel VH4 | DIE412 | Gain 68 · Master 72 · Bass 41 · Middle 64 · Treble 55 · Presence 51 | P1 P2 P3 P4 P5 P6 |
| 18 | Vibro King | Guitar | Fender Vibro-King | VIBROKING310 | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Bright 1 | P1 P2 P3 P4 P5 P6 |
| 19 | Budda | Guitar | Peavey Budda | BUDDA112 | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Cut 50 | P1 P2 P3 P4 P5 P6 |
| 20 | Mr. Z38 | Guitar | Dr. Z Maz 38 | Z212 | Gain 44 · Master 81 · Bass 35 · Middle 71 · Treble 52 · Cut 58 | P1 P2 P3 P4 P5 P6 |
| 21 | Super Rvb | Guitar | Fender Super Reverb | SUPERVERB410 | Gain 65 · Master 70 · Bass 50 · Middle 65 · Treble 55 · Bright 1 | P1 P2 P3 P4 P5 P6 |
| 22 | Brit Blues | Guitar | Unknown | GB412 | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Presence 50 | P1 P2 P3 P4 P5 P6 |
| 23 | Match D30 | Guitar | Matchless DC30 | MATCH212 | Gain 50 · Master 50 · Bass 50 · Treble 50 · Cut 50 | P1 P2 P3 P5 P6 |
| 24 | Brit 2000 | Guitar | Marshall JCM2000 | M1960AV | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Presence 50 | P1 P2 P3 P4 P5 P6 |
| 25 | Uber HiGain | Guitar | Bogner Uberschall | UBER412 | Gain 50 · Master 50 · Bass 50 · Middle 50 · Treble 50 · Presence 50 | P1 P2 P3 P4 P5 P6 |
| 26 | AGL | Bass | Aguilar Tone Hammer `[B]` | AGL_DB810 | Gain 61 · Master 89 · Bass 72 · Mid Freq 63 · Middle 50 · Treble 63 | P1 P2 P3 P6 P4 P5 |
| 27 | MLD | Bass | NUX NBP-5 `[B]` | MKB410 | Gain 70 · Master 91 · Bass 59 · Mid Freq 63 · Middle 50 · Treble 61 | P1 P2 P3 P6 P4 P5 |
| 28 | Optima Air | Acoustic | Neve 1073 | G-J15 | Gain 72 · Master 100 · Bass 50 · Middle 50 · Treble 50 | P1 P2 P3 P4 P5 |
| 29 | Stageman | Acoustic | NUX Stageman | M-D45 | Gain 60 · Master 90 · Bass 50 · Middle 50 · Treble 50 | P1 P2 P3 P4 P5 |

**Slot deviations from list order** (already reflected above, restated for clarity):
AGL and MLD route `Mid Freq` to `P6` while `Middle` takes `P4` and `Treble` takes `P5`.
Class A15, Class A30 and Match D30 have no `Middle` parameter; `P4` is unused.

**Amp groups** (`isSeparator = true`): Jazz Clean (Guitar), Bass Mate (Bass),
Tweedy (Guitar), AGL (Bass), Optima Air (Acoustic).

**Category tags** used by the Blrfl chart: `[A]` acoustic guitar, `[B]` bass guitar,
`[C]` ChopTones bonus IR, `[F247]` added in the 2024-07-11 firmware.

---

## 3. Cabinets / IRs

34 factory cabinets in the Dart source, `cabIndex` 1–34, family `CabinetPro`. All share
the same three editable parameters:

| Parameter | Handle | Default | Formatter | Slot |
|---|---|---|---|---|
| Level | `level` | 0 | `decibelMPPro` | `CAB_Para4` |
| Low Cut | `lowcut` | 20 | `lowFreqFormatter` | `CAB_Para5` |
| High Cut | `hicut` | 100 | `highFreqFormatter` | `CAB_Para6` |

| Idx | Cab | Group | Based on (Blrfl) |
|---|---|---|---|
| 1 | JZ120 | Electric IR | Roland JC-120 |
| 2 | DR112 | Electric IR | Fender Deluxe Reverb |
| 3 | TR212 | Electric IR | Fender Twin Reverb |
| 4 | HIWIRE412 | Electric IR | Hiwatt 4x12 |
| 5 | CALI 112 | Electric IR | Mesa/Boogie California |
| 6 | A112 | Electric IR | VOX AC15 1x12 |
| 7 | GB412 | Electric IR | Greenback 4x12 |
| 8 | M1960AX | Electric IR | Marshall 1960AX |
| 9 | M1960AV | Electric IR | Marshall 1960AV |
| 10 | M1960TV | Electric IR | Marshall 1960TV |
| 11 | SLO412 | Electric IR | Soldano 4x12 |
| 12 | FIREMAN 412 | Electric IR | Friedman 4x12 |
| 13 | RECT 412 | Electric IR | Mesa/Boogie Dual Rectifier |
| 14 | DIE412 | Electric IR | Diezel 4x12 |
| 15 | MATCH212 | Electric IR | Matchless DC30 |
| 16 | UBER412 | Electric IR | Bogner Uberschall |
| 17 | BS410 | Electric IR | Fender Tweed Bassman |
| 18 | A212 | Electric IR | VOX AC30 2x12 |
| 19 | M1960AHW | Electric IR | Marshall 1960AHW |
| 20 | M1936 | Electric IR | Marshall 1936 |
| 21 | BUDDA112 | Electric IR | Peavey Budda 1x12 |
| 22 | Z212 | Electric IR | Dr. Z Maz 38 2x12 |
| 23 | SUPERVERB410 | Electric IR | Fender Super Reverb |
| 24 | VIBROKING310 | Electric IR | Fender Vibro King |
| 25 | AGL_DB810 | Bass IR | Aguilar DB810 `[B]` |
| 26 | AMP_SV212 | Bass IR | Ampeg SV-212AV |
| 27 | AMP_SV410 | Bass IR | Ampeg SVT-410 |
| 28 | AMP_SV810 | Bass IR | Ampeg SVT-810 |
| 29 | BASSGUY410 | Bass IR | Fender BF Bassman |
| 30 | EDEN410 | Bass IR | Eden D410 Series |
| 31 | MKB410 | Bass IR | Eden D410 XLT? |
| 32 | G-HBIRD | Acoustic IR | Gibson Hummingbird `[A]` |
| 33 | G-J15 | Acoustic IR | Gibson J15 `[A]` |
| 34 | M-D45 | Acoustic IR | Martin D-45 `[A]` |

Plus `UserCab`, a dynamic cabinet whose name and index are assigned at runtime
(`setName` / `setNuxIndex`) for user-loaded IRs.

**Cabinet groups** (`isSeparator = true`): JZ120 (Electric IR), AGL_DB810 (Bass IR),
G-HBIRD (Acoustic IR).

**Present in the Blrfl chart but absent from the Dart source:**

| Cab | Based on (Blrfl) | Note |
|---|---|---|
| CT-Bogna-T75 | Bogner 4x12 G12T75 `[C]` | ChopTones bonus IR |
| CT-BritJH-G12M | Marshall 1960 G12M `[C]` | ChopTones bonus IR |

The chart also notes **+18 User Slots** for IRs. See §14 for the discrepancy analysis.

---

## 4. Compressor

| # | Model | Based on (Blrfl) | Parameters (default) | Slots |
|---|---|---|---|---|
| 1 | Rose Comp | Ross Compressor | Level 50 · Sustain 50 | P2 P1 |
| 2 | K Comp | Keeley 3-Knob | Level 50 · Sustain 50 · Clipping 50 | P2 P1 P3 |
| 3 | Studio Comp | Unknown | Gain 50 · Threshold 50 · Ratio 50 · Release 50 | P3 P1 P2 P4 |

All parameters use `percentageMPPro`.

---

## 5. EFX (drives, boosts, wah)

| # | Model | Based on (Blrfl) | Parameters (default) | Slots |
|---|---|---|---|---|
| 1 | Distortion+ | MXR M-104 Dist.+ | Output 75 · Sensitivity 80 | P1 P2 |
| 2 | RC Boost | Xotic RC Booster | Volume 40 · Gain 35 · Bass 35 · Treble 70 | P2 P1 P3 P4 |
| 3 | AC Boost | Xotic AC Booster | Volume 40 · Gain 60 · Bass 35 · Treble 50 | P2 P1 P3 P4 |
| 4 | Dist One | Boss DS-1 | Level 50 · Drive 40 · Tone 55 | P1 P3 P2 |
| 5 | T Screamer | Ibanez TS-9 | Level 55 · Drive 60 · Tone 60 | P3 P1 P2 |
| 6 | Blues Drive | Boss BD-2 | Level 40 · Gain 65 · Tone 50 | P1 P3 P2 |
| 7 | Morning Drive | JHS Morning Glory | Volume 50 · Drive 70 · Tone 65 | P1 P2 P3 |
| 8 | Eat Dist | ProCo Rat | Volume 60 · Distortion 65 · Filter 70 | P3 P1 P2 |
| 9 | Red Dirt | MXR M-115 Dist. III | Level 50 · Drive 65 · Tone 50 | P3 P1 P2 |
| 10 | Crunch | MI Audio Crunch Box? | Volume 25 · Gain 45 · Tone 50 | P1 P3 P2 |
| 11 | Muff Fuzz | EH Big Muff Pi | Volume 40 · Sustain 40 · Tone 50 | P1 P3 P2 |
| 12 | Katana | Keeley Katana | Volume 45 · Boost 0 (`boostModePro`) | P2 P1 |
| 13 | ST Singer | Vertex Steel String | Volume 50 · Gain 50 · Filter 40 | P1 P2 P3 |
| 14 | Touch Wah `[F247]` | Unknown | Type 1 (`touchWahFormatterLiteMk2`) · Wow 35 · Sense 90 · Level 100 · Up/Down Switch 0 (`touchWahDirectionFormatterPro`) | P1 P2 P3 P5 P4 |

Non-discrete parameters use `percentageMPPro`.

---

## 6. Wah (placeholder block)

| # | Model | Based on (Blrfl) | Parameters (default) | Slots |
|---|---|---|---|---|
| 1 | Wah (`WahDummyPro`) | *(not listed)* | Param1 50 · Param2 50 | `WAH_Para1` `WAH_Para2` |

Both parameters are wired to `MidiCCValuesPro.CC_Unknown` (= 0) and all five MIDI
foot-controller handles return `null`. This is a stub definition, not a usable wah model.
Consistently, `MidiCCValuesPro` defines **no** `WAH_Para*` constants.

---

## 7. Noise gate

Defined in the protocol (`Head_iNG` = 5, `NG_Para1`…`NG_Para4` = bytes 49–52, CC 43–46)
but **no model definitions were supplied**. The Blrfl chart lists one entry:

| Model | Based on (Blrfl) |
|---|---|
| Noise Gate | Boss NF-1 |

---

## 8. EQ

| # | Model | Based on (Blrfl) | Bands | Defaults | Slots |
|---|---|---|---|---|---|
| 1 | 6-Band | Boss GE-6 | 100, 220, 500, 1.2K, 2.6K, 6.4K | all 0 | P1–P6 |
| 3 | 10-Band | Unknown | Vol, 31, 62, 125, 250, 500, 1K, 2K, 4K, 8K, 16K | all 0 | P1–P11 |
| 0 | Bluetooth EQ | *(auxiliary)* | Vol, 31, 62, 125, 250, 500, 1K, 2K, 4K, 8K, 16K | all 0 | P1–P11 |
| 0 | Speaker EQ | *(auxiliary)* | Vol, 31, 62, 125, 250, 500, 1K, 2K, 4K, 8K, 16K | all 0 | P1–P11 |

All bands use `decibelEQ`. The two `nuxIndex => 0` variants are auxiliary EQs addressed
through separate MIDI CC banks (`AUX_BAND_1…11` and `SPK_EQ_VOL` / `SPK_EQ_1…10`) rather
than the main `EQ_Para*` slots. Both carry `//TODO: this might not be needed` on their
`getNuxCommand()` method. There is no EQ with `nuxIndex => 2`.

---

## 9. Modulation

| # | Model | Based on (Blrfl) | Parameters (default) | Slots |
|---|---|---|---|---|
| 1 | CE-1 | Boss CE-1 | Rate 39 · Depth 60 · Intensity 32 | P3 P2 P1 |
| 2 | CE-2 | Boss CE-2 | Rate 50 · Depth 50 | P1 P2 |
| 3 | ST Chorus | MXR MX-134 | Rate 60 · Width 36 · Intensity 74 | P3 P2 P1 |
| 4 | Vibrato | Boss VB-2 | Rate 56 · Depth 68 | P1 P2 |
| 5 | Detune | Unknown | Shift-L 54 · Shift-R 0 · Mix 80 | P1 P3 P2 |
| 6 | Flanger | Boss BF-2 | Rate 59 · Width 63 · Level 59 · Feedback 63 | P2 P3 P1 P4 |
| 7 | Phase 90 | MXR Phase 90 Script | Speed 60 | P1 |
| 8 | Phase 100 | MXR Phase 100 | Speed 39 · Intensity 60 | P2 P1 |
| 9 | S.C.F. | TC Stereo Chorus+ | Speed 60 · Width 70 · Intensity 60 · Mode 1 (`scfMode`) | P1 P2 P4 P3 |
| 10 | U-Vibe | Dunlop Univibe UV-1 | Speed 50 · Volume 80 · Intensity 80 · Mode 0 (`vibeModePro`) | P1 P2 P3 P4 |
| 11 | Tremolo | Boss TR-2 (subset) | Rate 70 · Depth 15 | P1 P2 |
| 12 | Rotary | Unknown | Speed 50 · Balance 50 | P2 P1 |
| 13 | SCH-1 | Arion SCH-1 | Rate 30 · Depth 70 · Tone 60 | P1 P2 P3 |
| 14 | Mono Octave `[F247]` | Unknown | Sub 50 · Dry 50 · Up 50 | P1 P2 P3 |

Non-discrete parameters use `percentageMPPro`. A source comment records the modulation
type selector mapping: 0 phaser, 1 chorus, 2 stereo chorus, 3 flanger, 4 vibe, 5 tremolo.

---

## 10. Delay

| # | Model | Based on (Blrfl) | Parameters (default) | Slots | Time formatter |
|---|---|---|---|---|---|
| 1 | Analog (`AnalogDelay`) | Boss DM-2 | Intensity 52 · Time 45 · Rate 34 | P3 P2 P1 | `tempoProAnalog` |
| 1 | Analog (`AnalogDelayV2`) | Boss DM-2 | Intensity 52 · Rate 34 · Echo 45 | P3 P1 P2 | `tempoProAnalog` |
| 2 | Digital Delay | Boss DD-2 (subset) | E.Level 49 · Time 48 · Feedback 68 | P1 P3 P2 | `tempoPro` |
| 3 | Modulation | Ibanez DML10 | Level 68 · Time 49 · Repeat 48 · Mod 68 | P2 P1 P4 P3 | `tempoProMod` |
| 4 | Tape Echo | Unknown | Level 43 · Time 61 · Repeat 56 | P2 P1 P3 | `tempoProTapeEcho` |
| 5 | Pan Delay | Ibanez DPL10 | Level 45 · Time 50 · Repeat 50 | P3 P1 P2 | `tempoPro` |
| 6 | Phi Delay | Unknown | Time 50 · Repeat 50 · Mix 45 | P1 P2 P3 | `tempoPro` |

Two classes named `Analog` both declare `nuxIndex => 1` (legacy and revised variants).
Non-Time parameters use `percentageMPPro`.

---

## 11. Reverb

| # | Model | Based on (Blrfl) | Parameters (default) | Slots |
|---|---|---|---|---|
| 1 | Room | Unknown | Level 50 · Decay 50 · Tone 50 | P3 P1 P2 |
| 2 | Hall | Unknown | Level 50 · Decay 50 · Pre Delay 50 · Liveliness 50 | P4 P1 P2 P3 |
| 3 | Plate | Unknown | Level 50 · Decay 50 | P2 P1 |
| 4 | Spring | Fender Tweed Spring | Level 50 · Decay 32 | P2 P1 |
| 5 | Shimmer | Unknown | Mix 50 · Decay 50 · Shimmer 50 | P1 P2 P3 |
| 6 | Damp | EMT140? | Mix 50 · Depth 50 | P1 P2 |

All parameters use `percentageMPPro`.

---

## 12. Totals

| Block | Count |
|---|---|
| Amplifiers | 29 |
| Cabinets (factory) | 34 (+1 user IR slot; Blrfl chart additionally lists 2 ChopTones bonus IRs) |
| Compressors | 3 |
| Delays | 7 definitions (6 unique indices) |
| EFX | 14 |
| Wah stubs | 1 |
| Noise gates | 0 defined (protocol slot exists) |
| EQs | 4 definitions (2 selectable + 2 auxiliary) |
| Modulations | 14 |
| Reverbs | 6 |

---

## 13. Constant resolution tables

### 13.1 Parameter slots — preset byte ↔ MIDI CC

Sorted by preset byte offset, which groups naturally by block.

| Slot | Preset byte | MIDI CC | Typical role in this app |
|---|---|---|---|
| `WAH_Para1` | 12 | — (uses `CC_Unknown` = 0) | Wah stub Param1 |
| `WAH_Para2` | 13 | — (uses `CC_Unknown` = 0) | Wah stub Param2 |
| `CMP_Para1` | 15 | 13 | Sustain / Threshold |
| `CMP_Para2` | 16 | 14 | Level / Ratio |
| `CMP_Para3` | 17 | 15 | Clipping / Gain |
| `CMP_Para4` | 18 | 16 | Release |
| `EFX_Para1` | 20 | 17 | Drive / Sensitivity / Type |
| `EFX_Para2` | 21 | 18 | Tone / Volume |
| `EFX_Para3` | 22 | 19 | Level / Gain / Wow |
| `EFX_Para4` | 23 | 20 | Treble / Mode / Direction |
| `EFX_Para5` | 24 | 21 | Touch Wah Level |
| `EFX_Para6` | 25 | 22 | **unused** |
| `AMP_Para1` | 27 | 23 | Gain |
| `AMP_Para2` | 28 | 24 | Master (always `masterVolume: true`) |
| `AMP_Para3` | 29 | 25 | Bass |
| `AMP_Para4` | 30 | 26 | Middle |
| `AMP_Para5` | 31 | 27 | Treble |
| `AMP_Para6` | 32 | 28 | Presence / Tone / Bright / Cut / Mid Freq |
| `AMP_Para7` | 33 | 29 | **unused** |
| `AMP_Para8` | 34 | 30 | **unused** |
| `EQ_Para1` | 36 | 31 | Band 1 (or Vol on 10-band) |
| `EQ_Para2` | 37 | 32 | Band 2 |
| `EQ_Para3` | 38 | 33 | Band 3 |
| `EQ_Para4` | 39 | 34 | Band 4 |
| `EQ_Para5` | 40 | 35 | Band 5 |
| `EQ_Para6` | 41 | 36 | Band 6 |
| `EQ_Para7` | 42 | 37 | Band 7 |
| `EQ_Para8` | 43 | 38 | Band 8 |
| `EQ_Para9` | 44 | 39 | Band 9 |
| `EQ_Para10` | 45 | 40 | Band 10 |
| `EQ_Para11` | 46 | 41 | Band 11 (16K) |
| `EQ_Para12` | 47 | 42 | **unused** |
| `NG_Para1` | 49 | 43 | **undefined** (no NG models supplied) |
| `NG_Para2` | 50 | 44 | **undefined** |
| `NG_Para3` | 51 | 45 | **undefined** |
| `NG_Para4` | 52 | 46 | **undefined** |
| `MOD_Para1` | 54 | 47 | Rate / Speed / Sub |
| `MOD_Para2` | 55 | 48 | Depth / Width / Dry |
| `MOD_Para3` | 56 | 49 | Intensity / Tone / Up |
| `MOD_Para4` | 57 | 50 | Mode / Feedback |
| `MOD_Para5` | 58 | 51 | **unused** |
| `MOD_Para6` | 59 | 52 | **unused** |
| `DLY_Para1` | 61 | 53 | Time |
| `DLY_Para2` | 62 | 54 | Repeat / Level |
| `DLY_Para3` | 63 | 55 | Level / Feedback |
| `DLY_Para4` | 64 | 56 | Mod (Modulation delay only) |
| `DLY_Para5` | 65 | 57 | **unused** |
| `DLY_Para6` | 66 | 58 | **unused** |
| `DLY_Para7` | 67 | 59 | **unused** |
| `DLY_Para8` | 68 | 60 | **unused** |
| `RVB_Para1` | 70 | 61 | Decay / Mix |
| `RVB_Para2` | 71 | 62 | Tone / Decay / Level |
| `RVB_Para3` | 72 | 63 | Level / Shimmer |
| `RVB_Para4` | 73 | 64 | Level (Hall only) |
| `CAB_Para1` | 75 | 65 | **unused** |
| `CAB_Para2` | 76 | 66 | **unused** |
| `CAB_Para3` | 77 | 67 | **unused** |
| `CAB_Para4` | 78 | 68 | Level |
| `CAB_Para5` | 79 | 69 | Low Cut |
| `CAB_Para6` | 80 | 70 | High Cut |
| `SR_Para1` | 82 | — | **undefined** (send/return) |
| `SR_Para2` | 83 | — | **undefined** |

**Observed relationship.** For every parameter slot, `preset byte = MIDI CC + head index + 1`:

| Block | Head idx | First byte | First CC | Delta |
|---|---|---|---|---|
| CMP | 1 | 15 | 13 | +2 |
| EFX | 2 | 20 | 17 | +3 |
| AMP | 3 | 27 | 23 | +4 |
| EQ | 4 | 36 | 31 | +5 |
| NG | 5 | 49 | 43 | +6 |
| MOD | 6 | 54 | 47 | +7 |
| DLY | 7 | 61 | 53 | +8 |
| RVB | 8 | 70 | 61 | +9 |
| CAB | 9 | 75 | 65 | +10 |

> **Inference (labelled).** Extending that rule to the two undefined blocks predicts
> `WAH_Para1` → CC 11 and `SR_Para1` → CC 71. Those numbers are already occupied by
> `TUNER_State` (11) and `TUNER_Number` (71), so neither block has free CCs under this
> scheme. That is a plausible reason the Wah stub is hard-wired to `CC_Unknown`, but the
> source does not state this — treat it as a hypothesis, not a documented fact.

**Unused-but-reserved slots:** `EFX_Para6`, `AMP_Para7`, `AMP_Para8`, `EQ_Para12`,
`MOD_Para5`, `MOD_Para6`, `DLY_Para5`–`DLY_Para8`, `CAB_Para1`–`CAB_Para3`.
Note that `CAB_Para1`–`CAB_Para3` sit *before* the three the cabinet block actually uses,
so the cab block's first three slots are unaccounted for.

### 13.2 Block head indices

Identical in both numbering spaces:

| Idx | Head constant | Block |
|---|---|---|
| 0 | `Head_iWAH` | Wah |
| 1 | `Head_iCMP` | Compressor |
| 2 | `Head_iEFX` | Effect / drive |
| 3 | `Head_iAMP` | Amplifier |
| 4 | `Head_iEQ` | EQ |
| 5 | `Head_iNG` | Noise gate |
| 6 | `Head_iMOD` | Modulation |
| 7 | `Head_iDLY` | Delay |
| 8 | `Head_iRVB` | Reverb |
| 9 | `Head_iCAB` | Cabinet / IR |
| 10 | `Head_iSR` | Send / return |

Block counts also live in the preset layout: `WAH_Count` 11, `CMP_Count` 14, `EFX_Count` 19,
`AMP_Count` 26, `EQ_Count` 35, `NG_Count` 48, `MOD_Count` 53, `DLY_Count` 60, `RVB_Count` 69,
`CAB_Count` 74, `SR_Count` 81.

### 13.3 Non-parameter preset bytes

| Constant | Byte | Meaning |
|---|---|---|
| `MASTER` | 84 | Patch level |
| `delay_time_flag` | 85 | Whether delay time follows tap/BPM |
| `bpmH` | 86 | Tempo BPM, high byte |
| `bpmL` | 87 | Tempo BPM, low byte |
| `BITCTRL` | 88 | Bit control field |
| `LINK1`–`LINK11` | 89–99 | Module-link flags |
| `UserName1`–`UserName16` | 100–115 | Preset name characters |
| `swsel1`–`swsel3` | 116–118 | Footswitch selection |
| `pdsel1`–`pdsel2` | 119–120 | Pedal selection |
| `version` | 121 | Preset version |
| `scene1`–`scene3` | 122–124 | Scene data |

### 13.4 Non-parameter MIDI CCs

| CC | Constant | Meaning |
|---|---|---|
| 11 | `TUNER_State` | Tuner active state |
| 12 | `TUNER_Note` | Tuner detected note |
| 71 | `TUNER_Number` | Tuner note number |
| 72 | `TUNER_Cent` | Tuner cents offset |
| 73 | `MASTER` | Patch level |
| 74 | `MSELECT` | Manual / preset select |
| 75 | `PEDAL` | Expression pedal |
| 76 | `SCENE` | Scene select |
| 77 | `DRUMENABLE` | Drum machine on/off |
| 78 | `DRUMTYPE` | Drum style (comment: 0 to ~66) |
| 79 | `DRUMLEVEL` | Drum level |
| 80 | `LOOPLEVEL` | Looper level (comment: confirmed) |
| 81 | `LOOPSTATE` | Looper state |
| 82 | `AUXEQENABLE` | Aux EQ group 0–3 |
| 83 | `PRESETRANGE` | Active-preset bitfield |
| 84 | `MICVOLUME` | Mic volume |
| 85 | `MICMUTE` | Mic mute |
| 86 | `USBROUNT_1` | Recording level |
| 87 | `USBROUNT_2` | Playback level |
| 88 | `USBROUNT_3` | Audio mode 0–2 (0 dry out, 1 normal, 2 reamp) |
| 89 | `USBROUNT_4` | Dry / wet |
| 90 | `AUX_MUTE` | Aux mute |
| 91 | `AUX_PHASE` | Aux phase invert |
| 92–102 | `AUX_BAND_1`–`AUX_BAND_11` | Aux EQ bands |
| 103 | `AUX_BAND_12` | Marked `NOT USED` in source |
| 104–106 | `DRUM_BASS`, `DRUM_MIDDLE`, `DRUM_TREBLE` | Drum tone controls |
| 107 | `LOOP_ARNR` | Loop auto-record / overdub |
| 108–110 | `NR_ENABLE`, `NR_SENS`, `NR_DECAY` | Noise reduction |
| 111 | `SPK_EQ_GROUP` | Speaker EQ group |
| 112 | `SPK_EQ_VOL` | Speaker EQ volume |
| 113–122 | `SPK_EQ_1`–`SPK_EQ_10` | Speaker EQ bands |
| 123 | `SPK_EQ_11` | Defined but unused by `EQTenBandSpeaker` |
| 125 | `AUX_SAVE` | Save aux EQ |
| 0 | `CC_Unknown` | Placeholder / not assigned |

> ⚠️ **Namespace collision.** The `TunerLiteMK2_*` constants reuse CCs already claimed by
> the speaker EQ: `TunerLiteMK2_State` = 112 = `SPK_EQ_VOL`, `TunerLiteMK2_Note` = 113 =
> `SPK_EQ_1`, `TunerLiteMK2_Number` = 114 = `SPK_EQ_2`, `TunerLiteMK2_Cent` = 115 =
> `SPK_EQ_3`. These presumably apply to different device families (Lite Mk2 vs Plug Pro),
> but the overlap is a trap for any tool that resolves CCs without knowing the target device.

> ⚠️ **Second collision.** `Head_iWAH` = 0 and `CC_Unknown` = 0 share the value 0. In
> `WahDummyPro` both meanings are in play simultaneously.

### 13.5 Other device families in `NuxConstants.dart`

The file also defines preset layouts for devices other than the Plug Pro. These are
**out of scope** for this document but present, so tooling should not confuse them:

| Class | Target device |
|---|---|
| `PresetDataIndexPlugAir` | Mighty Plug (Air) |
| `PresetDataIndex8BT` | 8BT — comment says to use `PresetDataIndexLite` |
| `PresetDataIndex2040BT` | 2040BT |
| `PresetDataIndexLite` | Mighty Lite / Mighty BT family |
| `PresetDataIndexPlugPro` | **Mighty Plug Pro — the subject of this document** |

A parallel legacy CC map, `MidiCCValues` (no `Pro` suffix), covers the Lite / 2040BT / Air
families and uses an entirely different numbering (e.g. `bCC_AmpEnable` = 102,
`bCC_AmpBass` = 103). Do not mix it with `MidiCCValuesPro`.

---

## 14. Quirks, discrepancies and unresolved items

### 14.1 Flags carried in the Dart source

- **`//check this`** on the `AMP_Para6` mapping of the sixth parameter for: Tweedy (Tone),
  Hiwire (Presence), Cali Crunch (Presence), Plexi 100 (Presence), Plexi 45 (Presence),
  Brit 800 (Presence), DIE VH4 (Presence), Mr. Z38 (Cut), AGL (Mid Freq), MLD (Mid Freq).
  Ten of the twenty-nine amps have an unverified slot-6 assignment.
- **`//TODO: this might not be needed`** on `getNuxCommand()` in `EQTenBandBT` and
  `EQTenBandSpeaker`.
- **Duplicate index:** `AnalogDelay` and `AnalogDelayV2` both declare `nuxIndex => 1` and
  both render as "Analog"; their parameter orders differ.
- **Missing index:** no EQ declares `nuxIndex => 2`.
- **Placeholder:** `WahDummyPro` uses `CC_Unknown` and returns `null` for all five
  foot-controller handles.

### 14.2 Dart source vs Blrfl chart

Model **counts agree** for every block except cabinets and noise gate:

| Block | Dart | Blrfl chart | Agreement |
|---|---|---|---|
| Amps | 29 | 29 | ✅ |
| EFX | 14 | 14 | ✅ |
| Modulation | 14 | 14 | ✅ |
| Delay | 7 defs / 6 indices | 6 | ✅ (duplicate index aside) |
| Reverb | 6 | 6 | ✅ |
| Compressor | 3 | 3 | ✅ |
| EQ (selectable) | 2 | 2 | ✅ |
| Cabinets | 34 factory + `UserCab` | 36 listed | ⚠️ chart adds 2 ChopTones IRs |
| Noise gate | 0 defined | 1 listed | ⚠️ protocol slot exists, no model |

**Naming differences** (same model, different spelling):

| Blrfl chart | Dart | Note |
|---|---|---|
| 1987 X 50 | `1987x50` / `Pl1987x50` | spacing only |
| Die VH4 | `DIE VH4` / `DIEVH4` | capitalisation only |
| HWIRE412 | `HIWIRE412` | chart appears to be a typo |
| Blues Drv | `Blues Drive` | abbreviation |
| Morning Drv | `Morning Drive` | abbreviation |

**Present in the chart, absent from the Dart source:**

| Item | Chart entry | Interpretation |
|---|---|---|
| `CT-Bogna-T75` | Bogner 4x12 G12T75 `[C]` | ChopTones bonus IR, likely user-loadable |
| `CT-BritJH-G12M` | Marshall 1960 G12M `[C]` | ChopTones bonus IR, likely user-loadable |
| Noise Gate | Boss NF-1 | Model exists on device; definitions not supplied |

The chart also notes **+18 User Slots** for IRs, which corresponds to the dynamic `UserCab`
class in the Dart source.

**Firmware coverage differs between the chart's own pages.** The GATE / CMP / MOD / EFX /
DLY / RVB / EQ page is labelled **20240711**; the AMP / IR page is labelled **20230320**.
Anything introduced between those dates would appear on the first page but not the second.
The chart marks Touch Wah and Mono Octave as `[F247]` (added 2024-07-11), and both are
present in the Dart source.

### 14.3 Default cabinet pairings that don't match the modelled amp

The Dart source fixes a default cabinet per amp; the chart supplies the modelled gear. Most
pairings line up (Class A15 → A112, Plexi 100 → GB412, Dual Rect → RECT 412, and so on).
These do not:

| Amp | Modelled after | Default cab | Default cab modelled after |
|---|---|---|---|
| Tweedy | Fender Tweed Deluxe | DR112 | Fender Deluxe Reverb |
| Cali Crunch | Mesa/Boogie (unspecified) | CALI 112 | Mesa/Boogie California |
| Brit Blues | Unknown | GB412 | Greenback 4x12 |
| MLD | NUX NBP-5 | MKB410 | Eden D410 XLT? |
| Optima Air | Neve 1073 | G-J15 | Gibson J15 |
| Stageman | NUX Stageman | M-D45 | Martin D-45 |

> **Inference (labelled).** This comparison is my analysis, not a claim made by either
> source. The practical implication for recommendation tooling is that the factory default
> cabinet is not reliably the matching IR for the amp's modelled circuit — for example,
> selecting Tweedy does not default to a tweed-era cabinet.

### 14.4 Unresolved: formatter ranges

Still **unknown** from the supplied files. `ValueFormatter.dart` provides only the abstract
contract (`min = 0`, `max = 100`) and the instance registry. The concrete limits and label
strings live in:

- `PercentageFormatter.dart` — `PercentageFormatter`, `PercentageFormatterMPPro`
- `DecibelFormatter.dart` — `DecibelFormatterMP2`, `DecibelFormatterMPPro`, `DecibelFormatterEQ`
- `TempoFormatter.dart` — `TempoFormatter`, `TempoFormatterPro`, `TempoFormatterProMod`, `TempoFormatterProAnalog`, `TempoFormatterProTapeEcho`
- `FrequencyFormatter.dart` — `LowFrequencyFormatter`, `HighFrequencyFormatter`
- `SwitchFormatters.dart` — `BrightModeFormatter(MPPro)`, `BoostModeFormatter(MPPro)`, `VibeModeFormatter(Pro)`, `ContourModeFormatter`, `SCFModeFormatter`, `TouchWahModeFormatter(LiteMk2)`, `TouchWahDirectionFormatterPro`

Until those are supplied, treat every default in §2–§11 as a **raw preset integer**, not a
percentage, dB value, hertz value or milliseconds value.

---

## 15. Usage notes for LLM tooling

Suggested interpretation rules when consuming this document:

1. **Treat defaults as raw integers.** Do not convert to engineering units without the
   formatter files (§14.4).
2. **Join on slot, not on list position.** Several effects list parameters in an order that
   does not match their slot order — AGL and MLD are the clearest cases (§2), and the
   delays vary widely (§10).
3. **Distinguish the two numbering spaces.** Preset byte ≠ MIDI CC. Use §13.1.
4. **Check the device family before resolving a CC.** The `TunerLiteMK2_*` / `SPK_EQ_*`
   overlap (§13.4) and the legacy `MidiCCValues` class (§13.5) are both traps.
5. **Discount `//check this` slot-6 amp mappings** (§14.1) when precision matters.
6. **Do not assume the default cab matches the amp's modelled circuit** (§14.3).
7. **Attribute gear equivalences to Blrfl Labs**, and respect the CC BY-NC-SA terms if
   redistributing (§0).
8. **Prefer explicit model names over "based on" names** when generating presets, since
   several chart entries are marked `Unknown` or carry a question mark (Crunch, Damp,
   MKB410, Studio Comp, Detune, Rotary, Brit Blues, Tape Echo, Phi Delay, Room, Hall,
   Plate, Shimmer, 10-Band).

---

## 16. Known gaps in this compilation

| Gap | Fix |
|---|---|
| Parameter min/max/step and display units | Supply the five formatter files listed in §14.4 |
| Noise gate models and parameters | Supply the NG effect definitions |
| Send/return models and parameters | Supply the SR effect definitions |
| Actual wah models | Supply the wah definitions (`WahDummyPro` is a stub) |
| Resolution of `//check this` amp slot-6 mappings | Verify against device or newer source |
| Whether the 2 ChopTones IRs are factory or user slots | Check device IR list or app release notes |

---

## 17. Human-Readable Preset JSON Schema Specification

To support direct parsing into `gen_qr.py`[cite: 1] and usage within the NUX Mighty Plug Pro ecosystem, single-preset human-readable files must follow the schema demonstrated below (see also `back_in_black.json`[cite: 4]):

```json
{
  "name": "Preset Name",
  "artist": "Artist / Inspiration",
  "device": "mighty_plug_pro",
  "signal_chain": [
    "NG",
    "CMP",
    "MOD",
    "EFX",
    "AMP",
    "CAB",
    "EQ",
    "DLY",
    "RVB"
  ],
  "blocks": {
    "efx": {
      "model": "Muff Fuzz",
      "enabled": true,
      "drive": 65,
      "tone": 55,
      "level": 50
    },
    "amplifier": {
      "model": "Plexi 100",
      "enabled": true,
      "gain": 70,
      "master": 75,
      "bass": 50,
      "middle": 65,
      "treble": 68,
      "presence": 60
    }
  },
  "other_blocks": {
    "noise_gate": true,
    "compressor": false,
    "eq": false,
    "modulation": false,
    "delay": false,
    "reverb": false,
    "wah": false,
    "send_return": false
  },
  "master": 50,
  "bpm": 120
}
```
### 17.1 Supported Signal Chain Routing Codes

The signal_chain array accepts standard uppercase short codes mapped internally by FX_ROUTING_MAP:

* NG / GATE: Noise Gate
* CMP / COMP: Compressor
* EFX / DRIVE: Effects / Drives / Boosts
* AMP: Amplifier
* CAB / IR: Cabinet / Impulse Response
* EQ: Equalizer
* MOD: Modulation
* DLY: Delay
* RVB: Reverb
