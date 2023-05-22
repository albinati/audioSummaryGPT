# Audio Summary Generator

This project uses OpenAI's GPT model and the Whisper ASR system to generate a summary from an audio file.

## Setup

1. **Clone the repository**

    ```
    git clone https://github.com/albinati/audioSummaryGPT.git
    cd audioSummaryGPT
    ```

2. **Install the required Python libraries**

    ```
    pip install -r requirements.txt
    ```

3. **Set up your environment variables**

    Create a `.env` file in the root of your project and fill it with your own values:

    ```dotenv
    # .env file
    OPENAI_KEY=your_openai_key
    INPUT_FOLDER=your_input_folder
    AUDIO_FILENAME=your_audio_filename
    OUTPUT_FOLDER=your_output_folder
    OUTPUT_FILENAME=your_output_filename
    TRANSCRIPT_FILENAME=your_transcript_filename
    CHUNK_FILENAME=your_chunk_filename
    USER_PROMPT1=your_user_prompt1
    USER_PROMPT2=your_user_prompt2
    AI_ROLE=your_ai_role
    GPT_MODEL=your_gpt_model (e.g. gpt-3.5-turbo)
    GPT_TEMP=your_gpt_temp (e.g. 0.3)
    ```

## Usage

1. **Transcribe the audio**

    Run the transcriber script to convert your audio into text:

    ```bash
    python transcriber.py
    ```

    This will create a `transcript.txt` file in the output folder.

2. **Generate the summary**

    Run the summarizer script to generate a summary of the transcript:

    ```bash
    python summarizer.py
    ```

    This will create a `summary.txt` and `summary_summarized.txt` files in the output folder with the summary.

## Notes

The transcription and summary quality can be affected by the clarity of the audio and the specific GPT model you're using. The Whisper model is used for transcription, and GPT-3.5-Turbo or GPT-4 can be used for summary generation. The `.env` file should contain all the necessary configuration.
