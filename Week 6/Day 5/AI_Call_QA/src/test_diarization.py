from pyannote.audio import Pipeline
import soundfile as sf
import torch

print("Loading model...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token="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"
)

print("Model loaded successfully!")

audio_file = r"data\uploads\Red.m4a"

print("Loading audio using SoundFile...")

audio, sample_rate = sf.read(audio_file)

# Convert to PyTorch tensor
waveform = torch.tensor(audio, dtype=torch.float32)

# If stereo, convert shape from (time, channels) to (channels, time)
if waveform.ndim == 2:
    waveform = waveform.transpose(0, 1)

# If mono, add channel dimension
if waveform.ndim == 1:
    waveform = waveform.unsqueeze(0)

audio_input = {
    "waveform": waveform,
    "sample_rate": sample_rate
}

print("Running diarization...")

diarization = pipeline(audio_input)

print("\nDiarization Result:\n")

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.2f}s --> {turn.end:.2f}s : {speaker}")