from extract_transcript import ExtractTranscript


#### EXECUTION 
audio_file = "video.wav"

# Create an instance of ExtractTranscript
transcript_extractor = ExtractTranscript()

# Use the instance to call the methods
transcriptions = transcript_extractor.extract_transcript(audio_file=audio_file)
print("Transcriptions:", transcriptions)
transcript_extractor.save_transcriptions_to_file(transcriptions, "lecture_transcription.txt")