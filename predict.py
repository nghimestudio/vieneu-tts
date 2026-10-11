"""Replicate / Cog predictor for VieNeu-TTS v3 Turbo."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf
from cog import BasePredictor, Input, Path as CogPath

# Run from the repo layout used in the Cog image.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

PRESET_VOICES = [
    "Hải Đăng",
    "Adam bựa",
    "Trúc Ly",
    "Thiện Minh",
    "Mai Anh",
    "Thùy Dung",
    "Thiền Tâm Đức",
    "Ngọc Huyền",
    "Quang Sơn",
    "Ngọc Trân",
    "Minh Đức",
    "Phạm Tuyên",
    "Thái Sơn",
    "Xuân Vĩnh",
    "Thanh Bình",
    "Ngọc Linh",
    "Đoan Trang",
    "Thục Đoan",
    "Minh Triết",
    "Mỹ Duyên",
    "Quỳnh Anh",
    "Đức Trí",
    "Kim Thanh",
    "Adam",
    "Quốc Tuấn",
]


class Predictor(BasePredictor):
    def setup(self) -> None:
        from vieneu import Vieneu

        # GPU image → PyTorch; if you switch cog.yaml to cpu/ONNX, use
        # backend="onnx", device="cpu", precision="fp32".
        self.tts = Vieneu(mode="v3turbo", backend="auto", device="auto")
        self.sample_rate = int(getattr(self.tts, "sample_rate", 48_000))

        # Warm the default path so the first user request is faster.
        try:
            _ = self.tts.infer("Xin chào.", voice="Hải Đăng", apply_watermark=False)
        except Exception:
            pass

    def predict(
        self,
        text: str = Input(
            description="Vietnamese (or bilingual) text to synthesize. "
            "Supports optional emotion tags: [cười], [thở dài], [hắng giọng]."
        ),
        voice: str = Input(
            description="Built-in preset voice. Ignored when ref_audio is provided.",
            default="Hải Đăng",
            choices=PRESET_VOICES,
        ),
        ref_audio: Optional[CogPath] = Input(
            description="Optional 3–8s reference clip for instant voice cloning. "
            "When set, overrides the preset voice.",
            default=None,
        ),
        denoise: bool = Input(
            description="Denoise / trim the reference clip before cloning.",
            default=True,
        ),
        temperature: float = Input(
            description="Sampling temperature.",
            default=0.8,
            ge=0.1,
            le=1.5,
        ),
        top_k: int = Input(
            description="Top-k sampling.",
            default=25,
            ge=1,
            le=100,
        ),
        top_p: float = Input(
            description="Top-p (nucleus) sampling.",
            default=0.95,
            ge=0.1,
            le=1.0,
        ),
        repetition_penalty: float = Input(
            description="Repetition penalty.",
            default=1.2,
            ge=1.0,
            le=2.0,
        ),
        max_chars: int = Input(
            description="Max characters per synthesis chunk.",
            default=256,
            ge=32,
            le=512,
        ),
    ) -> CogPath:
        text = (text or "").strip()
        if not text:
            raise ValueError("text must not be empty")

        kwargs = dict(
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            max_chars=max_chars,
            apply_watermark=False,
            denoise=denoise,
        )

        if ref_audio is not None:
            audio = self.tts.infer(text, ref_audio=str(ref_audio), **kwargs)
        else:
            audio = self.tts.infer(text, voice=voice, **kwargs)

        if audio is None or len(np.asarray(audio)) == 0:
            raise RuntimeError("Model returned empty audio")

        out = Path(tempfile.mkdtemp()) / "output.wav"
        sf.write(str(out), np.asarray(audio, dtype=np.float32), self.sample_rate)
        return CogPath(out)
