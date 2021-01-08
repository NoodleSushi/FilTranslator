import pyperclip


class ClipboardWatcher:
    def __init__(self) -> None:
        self.new_text: str = pyperclip.paste()
        self.old_text: str = self.new_text

    def is_changed(self) -> bool:
        pasted: str = pyperclip.paste()
        if pasted != self.new_text:
            self.old_text = self.new_text
            self.new_text = pasted
            return True
        return False
    
    def get_new_text(self) -> str:
        return self.new_text
    
    def copy(self, text: str) -> None:
        pyperclip.copy(text)
        self.old_text = self.new_text
        self.new_text = text