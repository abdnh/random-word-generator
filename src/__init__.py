import os
from typing import List

import anki
import aqt
from aqt import gui_hooks
from aqt.qt import QAction
from aqt.editor import Editor


from .randomlist import randomlist, get_wordlist
from .rwg_dialog import RWGDialog

addon_dir = os.path.dirname(os.path.realpath(__file__))


def randomlist_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: anki.template.TemplateRenderContext,
) -> str:

    if not filter_name.startswith("randlist"):
        return field_text

    try:
        config = {}
        for key, value in map(lambda c: c.split("="), filter_name.split()[1:]):
            config[key] = value

        config["words"] = get_wordlist(config.get("words", "en"))
        chosen = randomlist(**config)

        return " ".join(chosen)
    except Exception as e:
        return str(e)


def open_dialog(parent):
    dialog = RWGDialog(parent)
    dialog.exec_()


def on_editor_did_init_buttons(buttons: List[str], editor: Editor):
    btn = editor.addButton(
        icon=os.path.join(addon_dir, "icon.svg"),
        cmd="random_word_generator",
        func=lambda e: open_dialog(e.widget),
        tip="Random Word Generator",
    )

    buttons.append(btn)


if aqt.mw:
    anki.hooks.field_filter.append(randomlist_filter)
    action = QAction(aqt.mw)
    action.setText("Random Word Generator")
    aqt.mw.form.menuTools.addAction(action)
    action.triggered.connect(lambda: open_dialog(aqt.mw))
    gui_hooks.editor_did_init_buttons.append(on_editor_did_init_buttons)
