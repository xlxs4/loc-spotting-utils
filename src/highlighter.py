from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColorConstants


class Highlighter(QSyntaxHighlighter):
    def highlightBlock(self, text: str) -> None:
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
