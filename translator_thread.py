import threading
import re
from typing import Tuple

from googletrans import Translator
from googletrans.models import Translated

from dictionary import Dictionary


class TranslatorThread(threading.Thread):
    def __init__(self) -> None:
        super(TranslatorThread, self).__init__()
        self.translator: Translator = Translator()
        self.text: str = ""
        self.translated_text: str = ""
        self.has_translated_text: bool = False
    
    def start_translating(self, text: str) -> None:
        self.text = text
        self.translated_text = ""
        super(TranslatorThread, self).start()

    def run(self) -> None:
        if re.match("^[A-Za-z0-9-]*$", self.text.strip()):
            definitions: list = Dictionary.translate(self.text)
            if len(definitions) > 0:
                definition = definitions[0]
                self.translated_text = f"{definition['content']}: \n\n{definition['english']}"
        if self.translated_text == "":
            try:
                lang = self.translator.detect(self.text).lang
                translation: Translated
                if lang == 'en':
                    translation = self.translator.translate(self.text, dest='tl')
                else:
                    translation = self.translator.translate(self.text)
                self.translated_text = translation.text
            except Exception as e:
                print(e.__doc__)
                self.translated_text = "GOOGLE TRANSLATE SERVICE ERROR"
        if self.translated_text == "":
            self.translated_text = "NO RESULTS"
        self.has_translated_text = True
    
    def get_results(self) -> Tuple[bool, str]:
        if self.has_translated_text:
            self.has_translated_text = False
            return True, self.translated_text
        return False, ""
