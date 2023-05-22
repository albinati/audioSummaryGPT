# Transcriber

This is a script for transcribing audio files into text using the Whisper ASR system.

## Usage

Before running this script, please make sure your `.env` file is configured correctly with the necessary variables. Specifically, you need to specify:

- `INPUT_FOLDER`: The directory where your audio file is located.
- `AUDIO_FILENAME`: The name of the audio file to be transcribed.
- `OUTPUT_FOLDER`: The directory where the transcript file will be saved.
- `TRANSCRIPT_FILENAME`: The name of the output transcript file (without extension).

To run the transcriber, use the following command:

```bash
python transcriber.py
