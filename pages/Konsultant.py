from PyQt5.QtWidgets import (
    QDialog,
)
from pages.General import General

class Consultant(QDialog):
    def __init__(self, QwidgetConsultant, widget):
        super().__init__()
        self.page = General(QwidgetConsultant, widget)