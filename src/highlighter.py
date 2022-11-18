from re import compile

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QColorConstants


class Highlighter(QSyntaxHighlighter):
    _KEYWORDS = [
        "EQ", "NE", "LT", "GT", "LE", "GE", "AND", "OR", "XOR", "WHILE", "WH",
        "END", "IF", "THEN", "ELSE", "ENDIF"
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
        self._initialize_rules()

    def _initialize_formats(self):
        all_formats = (
            # name, color, bold, italic
            ("normal", None, False, False),
            ("keyword", QColorConstants.Blue, True, False),
            ("operator", QColorConstants.DarkMagenta, False, False),
            ("comment", QColorConstants.LightGray, False, False),
            ("gcode", QColorConstants.DarkBlue, True, False),
            ("mcode", QColorConstants.DarkBlue, True, False),
            ("coordinate", QColorConstants.Blue, True, False),
            ("string", QColorConstants.Green, False, False)
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

        def _a(a, b):
            r.append((compile(a), b))

        _a(
            "|".join([r"\b%s\b" % keyword for keyword in self._KEYWORDS]),
            "keyword"
        )

        _a(
            "|".join([r"\b%s\b" % operator for operator in self._OPERATORS]),
            "operator"
        )
        _a(r"(\\+|\\*|\\/|\\*\\*)", "operator")

        _a(r"(\\(.+\\))", "comment")
        _a(r";.*\n", "comment")

        _a(r"[G](1)?5[4-9](.1)?\\s?(P[0-9]{1,3})?", "gcode")
        _a(r"[G]1[1-2][0-9]", "gcode")
        _a(r"[G]15\\s?(H[0-9]{1,2})?", "gcode")
        _a(r"[G][0-9]{1,3}(\\.[0-9])?", "gcode")

        _a(r"[M][0-9]{1,3}", "mcode")

        _a(r"([X])\\s?(\\-?\\d*\\.?\\d+\\.?|\\-?\\.?(?=[#\\[]))", "coordinate")
        _a(r"([Y])\\s?(\\-?\\d*\\.?\\d+\\.?|\\-?\\.?(?=[#\\[]))", "coordinate")
        _a(r"([Z])\\s?(\\-?\\d*\\.?\\d+\\.?|\\-?\\.?(?=[#\\[]))", "coordinate")

        _a(r"([\\%])", "string")

        self._rules = tuple(r)

    def highlightBlock(self, text: str) -> None:
        text_length = len(text)
        self.setFormat(0, text_length, self._formats["normal"])

        for regex, format_ in self._rules:
            for m in regex.finditer(text):
                i, length = m.start(), m.end() - m.start()
                self.setFormat(i, length, self._formats[format_])
