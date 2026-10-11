# VieNeu-TTS v3 Turbo

Vietnamese (and bilingual) text-to-speech with instant voice cloning, powered by [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS).

48 kHz high-fidelity speech, 25 built-in preset voices, optional zero-shot cloning from a short reference clip, and experimental emotion tags like `[cười]`, `[thở dài]`, `[hắng giọng]`.

## Examples

### Preset voice

**Input**
- `text`: `Xin chào! Đây là giọng đọc VieNeu-TTS v3 Turbo trên Replicate.`
- `voice`: `Hải Đăng`

**Output:** 48 kHz WAV in the Hải Đăng preset voice.

### With emotion cue

**Input**
- `text`: `[cười] Trời ơi, cái giọng nó tự nhiên quá. Giờ thì tha hồ mà quẩy content nhé!`
- `voice`: `Mai Anh`

**Output:** Natural Vietnamese speech with a chuckle cue.

### Instant voice cloning

**Input**
- `text`: `Đây là giọng được nhân bản tức thì từ một đoạn thu âm ngắn.`
- `ref_audio`: a clean 3–8s reference WAV of the target speaker
- `denoise`: `true`

**Output:** Cloned-speaker WAV at 48 kHz.

## Inputs

| Name | Type | Default | Description |
|---|---|---|---|
| `text` | string | required | Vietnamese / bilingual text (supports `[cười]`, `[thở dài]`, `[hắng giọng]`) |
| `voice` | choice | `Hải Đăng` | One of 25 built-in preset voices |
| `ref_audio` | file | optional | 3–8s reference clip for cloning (overrides `voice`) |
| `denoise` | bool | `true` | Denoise / trim the reference before cloning |
| `temperature` | float | `0.8` | Sampling temperature |
| `top_k` | int | `25` | Top-k sampling |
| `top_p` | float | `0.95` | Nucleus sampling |
| `repetition_penalty` | float | `1.2` | Repetition penalty |
| `max_chars` | int | `256` | Max characters per synthesis chunk |

## Tips

- Start with editors' picks: Hải Đăng, Mai Anh, Trúc Ly, Adam bựa, Ngọc Lý / Ngọc Huyền.
- Keep clone references short (3–8s), clean, and mostly continuous speech.
- Long text is chunked automatically via `max_chars`.

## Links

- Weights: https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo
- Source: https://github.com/nghimestudio/vieneu-tts
- Upstream: https://github.com/pnnbao97/VieNeu-TTS
- Site: https://www.vieneu.io
