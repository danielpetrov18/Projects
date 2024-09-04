class TranscriptionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class TranslationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class AudioGenerationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
