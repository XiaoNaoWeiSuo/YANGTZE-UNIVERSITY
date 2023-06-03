from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFont

class SFont(QFont):
    def __init__(self, font_family, font_size):
        super().__init__()
        self.setFamily(font_family)
        self.setPointSize(font_size)
        self.setHintingPreference(QFont.HintingPreference.PreferNoHinting)