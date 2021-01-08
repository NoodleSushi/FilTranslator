from fil_translator import FilTranslator

if __name__ == "__main__":
    fil_translator = FilTranslator()
    while True:
        if not fil_translator.update():
            break
