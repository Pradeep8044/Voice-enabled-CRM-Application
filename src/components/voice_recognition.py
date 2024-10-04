import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"
