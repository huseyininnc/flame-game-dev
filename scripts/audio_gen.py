import argparse
import json
import math
import os
import struct
import wave

RATE = 44100


def envelope(index, total, attack, release):
    t = index / RATE
    duration = total / RATE
    attack = min(attack, duration)
    release = min(release, duration)
    if t < attack:
        return t / attack if attack > 0 else 1.0
    if t > duration - release:
        return max(0.0, (duration - t) / release) if release > 0 else 0.0
    return 1.0


def wave_value(shape, phase):
    if shape == "square":
        return 1.0 if math.sin(phase) >= 0 else -1.0
    if shape == "tri":
        return 2 / math.pi * math.asin(math.sin(phase))
    return math.sin(phase)


def tone(op):
    freqs = op.get("freqs") or [op["freq"]]
    duration = op.get("dur", 0.1)
    volume = op.get("vol", 0.4)
    shape = op.get("shape", "sine")
    glide = op.get("glide", 0.0)
    attack = op.get("attack", 0.01)
    release = op.get("release", 0.2)
    total = int(duration * RATE)
    out = []
    for i in range(total):
        t = i / RATE
        amp = envelope(i, total, attack, release) * volume
        sample = 0.0
        for freq in freqs:
            sample += wave_value(shape, 2 * math.pi * (freq + glide * t) * t)
        out.append(sample / len(freqs) * amp)
    return out


def render_sfx(ops):
    out = []
    for op in ops:
        out += tone(op)
    return out


def render_ambient(spec):
    voices = spec.get("voices", [110, 165, 220, 277])
    seconds = spec.get("seconds", 10)
    total = int(seconds * RATE)
    out = []
    for i in range(total):
        t = i / RATE
        sample = 0.0
        for index, base in enumerate(voices):
            drift = math.sin(2 * math.pi * (0.04 + index * 0.015) * t) * 1.4
            sample += math.sin(2 * math.pi * (base + drift) * t)
        sample /= len(voices)
        swell = 0.45 + 0.22 * math.sin(2 * math.pi * 0.06 * t)
        fade = min(1.0, t / 1.5, (seconds - t) / 1.5)
        out.append(sample * swell * 0.5 * max(0.0, fade))
    return out


def write_wav(path, samples):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    frames = bytearray()
    for value in samples:
        clamped = max(-1.0, min(1.0, value))
        frames += struct.pack("<h", int(clamped * 32000))
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(bytes(frames))


def run(manifest, out_dir):
    for entry in manifest.get("sfx", []):
        path = os.path.join(out_dir, f"{entry['name']}.wav")
        write_wav(path, render_sfx(entry["ops"]))
        print(f"saved {path}", flush=True)
    for entry in manifest.get("music", []):
        path = os.path.join(out_dir, f"{entry['name']}.wav")
        write_wav(path, render_ambient(entry["ambient"]))
        print(f"saved {path}", flush=True)
    print("done", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Synthesize royalty-free game SFX/BGM (.wav) from a JSON manifest "
            "using only the Python standard library (no dependencies)."
        ),
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help='JSON: {"sfx":[{"name","ops":[{freq|freqs,dur,vol?,shape?,glide?}]}],'
        ' "music":[{"name","ambient":{"voices","seconds"}}]}.',
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory (name may include subfolders like sfx/shoot).",
    )
    args = parser.parse_args()
    with open(args.manifest, encoding="utf-8") as handle:
        manifest = json.load(handle)
    run(manifest, args.out)


if __name__ == "__main__":
    main()
