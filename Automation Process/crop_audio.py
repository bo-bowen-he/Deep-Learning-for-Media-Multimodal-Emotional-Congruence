import os
from pydub import AudioSegment

INPUT_FOLDER = "audio_converted"
OUTPUT_FOLDER = "audio"
CROP_DURATION_MS = 60 * 1000  # 60 seconds in milliseconds

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

wav_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".wav")]

if not wav_files:
    print(f"No WAV files found in '{INPUT_FOLDER}'.")
else:
    for filename in wav_files:
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        print(f"Processing: {filename}")

        audio = AudioSegment.from_wav(input_path)
        cropped = audio[:CROP_DURATION_MS]
        cropped.export(output_path, format="wav")

        print(f"  Saved: {output_path}")

    print(f"\nDone! {len(wav_files)} file(s) cropped and saved to '{OUTPUT_FOLDER}/'.")
