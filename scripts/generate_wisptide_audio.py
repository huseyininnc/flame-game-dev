import math
import os
import random
import struct
import wave

SFX_DIR = r"C:\workspace\zeynsoft_projects\projects\games\wisptide\assets\audio\sfx"
MUSIC_DIR = r"C:\workspace\zeynsoft_projects\projects\games\wisptide\assets\audio\music"
RATE = 44100


def write_wav(path, samples):
    frames = bytearray()
    for value in samples:
        clamped = max(-1.0, min(1.0, value))
        frames += struct.pack("<h", int(clamped * 32000))
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(bytes(frames))


def env(i, total, attack=0.01, release=0.2):
    t = i / RATE
    dur = total / RATE
    at = min(attack, dur)
    rt = min(release, dur)
    if t < at:
        return t / at
    if t > dur - rt:
        return max(0.0, (dur - t) / rt)
    return 1.0


def tone(freq, dur, vol=0.5, shape="sine", glide=0.0):
    total = int(dur * RATE)
    out = []
    for i in range(total):
        t = i / RATE
        f = freq + glide * t
        phase = 2 * math.pi * f * t
        if shape == "sine":
            v = math.sin(phase)
        elif shape == "square":
            v = 1.0 if math.sin(phase) >= 0 else -1.0
        elif shape == "tri":
            v = 2 / math.pi * math.asin(math.sin(phase))
        elif shape == "noise":
            v = random.uniform(-1, 1)
        else:
            v = math.sin(phase)
        out.append(v * vol * env(i, total))
    return out


def chord(freqs, dur, vol=0.4, shape="sine"):
    layers = [tone(f, dur, vol, shape) for f in freqs]
    n = len(layers[0])
    return [sum(l[i] for l in layers) / len(layers) for i in range(n)]


def seq(parts):
    out = []
    for p in parts:
        out += p
    return out


def mix(a, b):
    n = min(len(a), len(b))
    return [(a[i] + b[i]) * 0.7 for i in range(n)]


def ambient(seconds=10):
    total = int(seconds * RATE)
    out = []
    voices = [98, 147, 196, 262]
    for i in range(total):
        t = i / RATE
        v = 0.0
        for idx, base in enumerate(voices):
            drift = math.sin(2 * math.pi * (0.04 + idx * 0.015) * t) * 1.4
            v += math.sin(2 * math.pi * (base + drift) * t)
        v /= len(voices)
        swell = 0.45 + 0.22 * math.sin(2 * math.pi * 0.06 * t)
        fade = min(1.0, t / 1.5, (seconds - t) / 1.5)
        out.append(v * swell * 0.5 * max(0.0, fade))
    return out


def main():
    os.makedirs(SFX_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)
    random.seed(11)
    sfx = {
        "shoot": tone(720, 0.07, 0.3, "square", glide=-260),
        "hit": tone(300, 0.05, 0.32, "tri", glide=-120),
        "enemy_death": tone(420, 0.18, 0.4, "tri", glide=-300),
        "pickup": tone(560, 0.1, 0.32, "sine", glide=320),
        "levelup": seq([
            tone(523, 0.09, 0.4, "tri"),
            tone(659, 0.09, 0.4, "tri"),
            tone(784, 0.14, 0.5, "tri"),
        ]),
        "evolve": seq([
            tone(659, 0.08, 0.4, "sine"),
            tone(988, 0.08, 0.4, "sine"),
            chord([880, 1175, 1397], 0.35, 0.5, "sine"),
        ]),
        "boss": mix(tone(70, 0.7, 0.6, "square"), tone(73, 0.7, 0.5, "tri")),
        "hurt": mix(tone(160, 0.16, 0.5, "tri", glide=-90),
                    tone(0, 0.16, 0.3, "noise")),
        "revive": seq([
            tone(440, 0.1, 0.4, "sine"),
            tone(660, 0.1, 0.4, "sine"),
            chord([660, 880], 0.3, 0.5, "sine"),
        ]),
        "click": tone(880, 0.04, 0.3, "square"),
    }
    for name, samples in sfx.items():
        path = os.path.join(SFX_DIR, f"{name}.wav")
        write_wav(path, samples)
        print(f"OK {path}")
    run_path = os.path.join(MUSIC_DIR, "run.wav")
    write_wav(run_path, ambient())
    print(f"OK {run_path}")


if __name__ == "__main__":
    main()
