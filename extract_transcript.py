import os
import time 
import azure.cognitiveservices.speech as speechsdk

class ExtractTranscript:
    
    def continuous_recognition_handler(self, evt, transcriptions):
        """Handles the recognized speech."""
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"RECOGNIZED: {evt.result.text}")
            transcriptions.append(evt.result.text)

    def stop_cb(self, evt, speech_recognizer):
        """Stops recognition when the stop event is received."""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        global done
        done = True

    def extract_transcript(self, audio_file):
        """Sets up continuous speech recognition from a file."""
        global done
        done = False

        # Initialize a list to store transcriptions
        transcriptions = []

        # Set up the speech config with your key and region
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = "eastus"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["en-US", "es-AR"])
        
        # Set up the audio config using your audio file
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

        # Initialize the speech recognizer with auto language detection
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            auto_detect_source_language_config=auto_detect_source_language_config,
            audio_config=audio_config
        )
        
        # Connect callbacks to events
        speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: self.continuous_recognition_handler(evt, transcriptions))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: self.stop_cb(evt, speech_recognizer))
        speech_recognizer.canceled.connect(lambda evt: self.stop_cb(evt, speech_recognizer))

        # Start continuous recognition
        speech_recognizer.start_continuous_recognition()

        # Keep the script running until the recognition is complete
        while not done:
            time.sleep(0.5)
        
        return transcriptions

    def save_transcriptions_to_file(self, transcriptions, file_name="transcriptions.txt"):
        """Save the transcriptions to a text file."""
        with open(file_name, 'w', encoding='utf-8') as f:
            for line in transcriptions:
                f.write(line + '\n')
        print(f"Transcriptions saved to {file_name}")