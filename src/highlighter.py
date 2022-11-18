import re

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QColorConstants


class Highlighter(QSyntaxHighlighter):
    _KEYWORDS = [
        "EQ", "NE", "LT", "GT", "LE", "GE", "AND", "OR", "XOR",
        "WHILE", "WH", "END", "IF", "THEN", "ELSE", "ENDIF"
    ]

    _OPERATORS = [
        "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN", "FIX", "FUP", "LN",
        "ROUND", "SQRT", "FIX", "ABS", "MOD"
    ]

    # Hack to be able to define a custom initializer.
    # By default you can only implement the highlightBlock virtual function
    # without messing up the way it connects to the text parent behind the scenes.
    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)
        self._initialize_formats()

    def _initialize_formats(self):
        all_formats = (
            # name, color, bold, italic
            ("normal", None, False, False),
            ("keyword", QColorConstants.DarkMagenta, True, False),
            ("builtin", QColorConstants.DarkMagenta, False, False),
            ("comment", QColorConstants.LightGray, False, False),
            ("coor-num", QColorConstants.DarkMagenta, False, False),
            ("coor-val", QColorConstants.DarkMagenta, True, True)
        )

        self._formats = {}

        for name, color, bold, italic in all_formats:
            format_ = QTextCharFormat()
            if color:
                format_.setForeground(QColor(color))
            if bold:
                format_.setFontWeight(QFont.Weight.Bold)
            if italic:
                format_.setFontItalic(True)

            self._formats[name] = format_

    def _initialize_rules(self):
        r = []

        def a(a, b):
            r.append((re.compile(a), b))

        a("|".join([r"\b%s\b" % keyword for keyword in self._KEYWORDS]), "keyword")
        a("|".join([r"\b%s\b" % operator for operator in self._OPERATORS]), "operator")

    def highlightBlock(self, text: str) -> None:
        text_length = len(text)
        self.setFormat(0, text_length, self._formats["normal"])

        builtin_format = QTextCharFormat()
        builtin_format.setFontWeight(QFont.Bold)
        builtin_format.setForeground(QColorConstants.DarkMagenta)

        builtin_expression = QRegularExpression(r"^[gmGM]\d{1,5}\s")
        i = builtin_expression.globalMatch(text)
        while i.hasNext():
            match = i.next()
            self.setFormat(
                match.capturedStart(), match.capturedLength(), builtin_format
            )

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColorConstants.LightGray)

        comment_expression = QRegularExpression(r";.*")
        i = comment_expression.globalMatch(text)
        while i.hasNext():
            match = i.next()
            self.setFormat(
                match.capturedStart(), match.capturedLength(), comment_format
            )
