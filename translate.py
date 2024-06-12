from google.cloud import translate_v2

def translate_text(text, target_language):
    translate_client = translate_v2.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText'] 