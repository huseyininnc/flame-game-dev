import math
import os
import random
import struct
import wave

SFX_DIR = r"C:\workspace\zeynsoft_projects\projects\games\mitomerge\assets\audio\sfx"
MUSIC_DIR = r"C:\workspace\zeynsoft_projects\projects\games\mitomerge\assets\audio\music"
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


def envelope(index, total, attack=0.01, release=0.2):
    t = index / RATE
    duration = total / RATE
    attack_t = min(attack, duration)
    release_t = min(release, duration)
    if t < attack_t:
        return t / attack_t
    if t > duration - release_t:
        return max(0.0, (duration - t) / release_t)
    return 1.0


def tone(freq, duration, volume=0.5, shape="sine", glide=0.0):
    total = int(duration * RATE)
    samples = []
    for i in range(total):
        t = i / RATE
        f = freq + glide * t
        phase = 2 * math.pi * f * t
        if shape == "sine":
            value = math.sin(phase)
        elif shape == "square":
            value = 1.0 if math.sin(phase) >= 0 else -1.0
        elif shape == "triangle":
            value = 2 / math.pi * math.asin(math.sin(phase))
        elif shape == "noise":
            value = random.uniform(-1, 1)
        else:
            value = math.sin(phase)
        samples.append(value * volume * envelope(i, total))
    return samples


def chord(freqs, duration, volume=0.4, shape="sine"):
    layers = [tone(f, duration, volume, shape) for f in freqs]
    length = len(layers[0])
    return [sum(layer[i] for layer in layers) / len(layers) for i in range(length)]


def sequence(parts):
    result = []
    for part in parts:
        result += part
    return result


def make_spawn():
    return tone(420, 0.18, 0.5, "triangle", glide=380)


def make_merge():
    return sequence([
        chord([523, 659], 0.12, 0.45, "triangle"),
        chord([784, 988], 0.16, 0.5, "triangle"),
    ])


def make_shot():
    return tone(880, 0.06, 0.35, "square", glide=-300)


def make_hit():
    mixed = []
    base = tone(240, 0.08, 0.4, "triangle", glide=-120)
    noise = tone(0, 0.08, 0.25, "noise")
    for i in range(len(base)):
        mixed.append((base[i] + noise[i]) * 0.6)
    return mixed


def make_death():
    return tone(520, 0.22, 0.45, "triangle", glide=-360)


def make_wave():
    return sequence([
        tone(523, 0.1, 0.4, "triangle"),
        tone(659, 0.1, 0.4, "triangle"),
        tone(784, 0.16, 0.5, "triangle"),
    ])


def make_nucleus():
    return tone(140, 0.26, 0.6, "sine", glide=-40)


def make_boss():
    growl = tone(90, 0.6, 0.6, "square", glide=20)
    return growl


def make_prestige():
    return sequence([
        tone(659, 0.1, 0.4, "sine"),
        tone(880, 0.1, 0.4, "sine"),
        tone(1175, 0.12, 0.45, "sine"),
        chord([880, 1175, 1397], 0.4, 0.5, "sine"),
    ])


def make_ambient(seconds=8):
    total = int(seconds * RATE)
    samples = []
    voices = [110, 165, 220, 277]
    for i in range(total):
        t = i / RATE
        value = 0.0
        for index, base in enumerate(voices):
            drift = math.sin(2 * math.pi * (0.05 + index * 0.02) * t) * 1.5
            value += math.sin(2 * math.pi * (base + drift) * t)
        value /= len(voices)
        swell = 0.4 + 0.25 * math.sin(2 * math.pi * 0.08 * t)
        fade = min(1.0, t / 1.5, (seconds - t) / 1.5)
        samples.append(value * swell * 0.5 * max(0.0, fade))
    return samples


def main():
    os.makedirs(SFX_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)
    random.seed(7)

    sfx = {
        "spawn": make_spawn(),
        "merge": make_merge(),
        "shot": make_shot(),
        "hit": make_hit(),
        "death": make_death(),
        "wave": make_wave(),
        "nucleus": make_nucleus(),
        "boss": make_boss(),
        "prestige": make_prestige(),
    }
    for name, samples in sfx.items():
        path = os.path.join(SFX_DIR, f"{name}.wav")
        write_wav(path, samples)
        print(f"OK {path}")

    ambient_path = os.path.join(MUSIC_DIR, "ambient.wav")
    write_wav(ambient_path, make_ambient())
    print(f"OK {ambient_path}")


if __name__ == "__main__":
    main()
