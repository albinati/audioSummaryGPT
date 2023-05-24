from dotenv import load_dotenv
import os
import pathlib
import whisper

def transcribe():

    # Initialize transcribe text variable
    transcribeText = None

    # Load the .env file
    load_dotenv(pathlib.Path(__file__).parent.parent / '.env')

    # Get the GPT model from the .env file
    gpt_model = os.getenv('GPT_MODEL')

    # Define the maximum token limit for different models
    model_token_limit = {
        'gpt-3.5-turbo': 4096,
        'gpt-4': 8192
    }

    # Set maximum tokens depending on the model selected
    max_tokens = model_token_limit.get(gpt_model, 4096) # Default to 4096 if model isn't in the dictionary

    # Get paths from the .env file
    input_folder = os.getenv('INPUT_FOLDER')
    audio_filename = os.getenv('AUDIO_FILENAME')
    output_folder = os.getenv('OUTPUT_FOLDER')
    transcript_filename = os.getenv('TRANSCRIPT_FILENAME')

    # Create output and content directory if it does not exist
    try:
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except Exception as e:
        print(f"Error creating directories: {e}")
        exit(1)

    # Load the whisper model
    try:
        model = whisper.load_model("base")
        print("Model Loaded")
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)

    # If the transcript file does not exist, transcribe the audio file
    try:
        if not os.path.exists(f'{output_folder}/{transcript_filename}'):   
            print("Transcribing audio file. It might take a while.")
            result = model.transcribe(f'{input_folder}/{audio_filename}', verbose = True)
            transcribeText = result["text"]
            with open(f'{output_folder}/{transcript_filename}.txt', 'w') as f:
                f.write(transcribeText)
        # If the transcript file exists, read its content
        else:
            print("Transcription found. No action")            
    except FileNotFoundError:
        print("Input file or folder does not exist. Please fix this and rerun the script.")
        exit(1)
    pass