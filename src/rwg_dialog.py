import sys

if __name__ == "__main__":
    from PyQt6.QtWidgets import QDialog, QApplication
    import form_qt6 as rwg_form
    from randomlist import randomlist, get_wordlist_labels, get_wordlist
else:
    from aqt import qtmajor
    from aqt.qt import *

    if qtmajor > 5:
        from . import form_qt6 as rwg_form
    else:
        from . import form_qt5 as rwg_form
    from .randomlist import randomlist, get_wordlist_labels, get_wordlist


class RWGDialog(QDialog):
    def __init__(
        self,
        parent,
    ):
        QDialog.__init__(self, parent)
        self.form = rwg_form.Ui_Dialog()
        self.form.setupUi(self)

        self.form.generateButton.clicked.connect(self.accept)
        self.form.copyButton.clicked.connect(self.on_copy_selected)
        self.form.wordlistComboBox.currentIndexChanged.connect(self.on_list_changed)
        self.form.lengthSpinBox.setValue(7)
        self.populate_wordlists()

    def populate_wordlists(self):
        self.form.wordlistComboBox.addItems(get_wordlist_labels())

    def on_list_changed(self, index):
        self.words = get_wordlist(self.form.wordlistComboBox.currentText())
        max_value = len(self.words)
        self.form.startSpinBox.setMaximum(max_value)
        self.form.endSpinBox.setMaximum(max_value)
        self.form.endSpinBox.setValue(max_value)
        self.form.wordCountLabel.setText(f"Word Count: {max_value}")

    def accept(self):
        start = self.form.startSpinBox.value()
        end = self.form.endSpinBox.value()
        length = self.form.lengthSpinBox.value()
        chosen = randomlist(self.words, start, end, length)
        self.form.generatedList.clear()
        self.form.generatedList.addItems(chosen)
        QApplication.clipboard().setText(" ".join(chosen))

    def on_copy_selected(self):
        selected_items = self.form.generatedList.selectedItems()
        selected_text = []
        for item in selected_items:
            selected_text.append(item.text())
        QApplication.clipboard().setText(" ".join(selected_text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = RWGDialog(None)
    d.exec()
