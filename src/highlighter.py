import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui


class Highlighter(QtGui.QSyntaxHighlighter):
    def highlightBlock(self, text: str) -> None:
        builtin_format = QtGui.QTextCharFormat()
        builtin_format.setFontWeight(QtGui.QFont.Bold)
        builtin_format.setForeground(QtGui.QColorConstants.DarkMagenta)

        builtin_expression = QtCore.QRegularExpression(r"^[gmGM]\d{1,5}\s")
        i = builtin_expression.globalMatch(text)
        while i.hasNext():
            match = i.next()
            self.setFormat(
                match.capturedStart(), match.capturedLength(), builtin_format
            )

        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColorConstants.LightGray)

        comment_expression = QtCore.QRegularExpression(r";.*")
        i = comment_expression.globalMatch(text)
        while i.hasNext():
            match = i.next()
            self.setFormat(
                match.capturedStart(), match.capturedLength(), comment_format
            )
