from datetime import datetime

import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14 Luglio 2026 - Traccia A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

        self._ddYearFrom = None
        self._ddYearTo = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None

        self._ddDirector = None
        self._txtInN = None
        self._btnTrovaGruppo = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14 Luglio 2026 - Traccia A", color="blue", size=24)
        self._page.controls.append(self._title)

        # riga 1
        self._dpFrom = ft.DatePicker(
            first_date=datetime(2017, 1, 1),
            last_date=datetime(2019, 12, 31),
            current_date=datetime(2017, 1, 1),
            help_text="Data iniz.",
            on_change=self._dpFrom_change
        )
        self._dpTo = ft.DatePicker(
            first_date=datetime(2017, 1, 1),
            last_date=datetime(2019, 12, 31),
            current_date=datetime(2019, 12, 31),
            help_text="Data fin. ",
            on_change=self._dpTo_change
        )
        self._page.overlay.extend([self._dpFrom, self._dpTo])

        self._btnPickFrom = ft.ElevatedButton("Data da", on_click=lambda _: self._dpFrom.pick_date())
        self._btnPickTo = ft.ElevatedButton("Data a", on_click=lambda _: self._dpTo.pick_date())

        self._txtDateFrom = ft.Text("Nessuna data selezionata")
        self._txtDateTo = ft.Text("Nessuna data selezionata")

        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                                on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                 on_click=self._controller.handleStampaInfo, disabled = True)

        row1 = ft.Row([ft.Container(self._btnPickFrom, width=125),
                       ft.Container(self._btnPickTo, width=125),
                       ft.Container(self._btnCreaGrafo, width=180),
                       ft.Container(self._btnStampaInfo, width=180)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # new row with two text fields for the selected dates
        self._txtDateFrom = ft.Text("Nessuna data selezionata")
        self._txtDateTo = ft.Text("Nessuna data selezionata")

        row2 = ft.Row([ft.Container(self._txtDateFrom, width=180),
                       ft.Container(self._txtDateTo, width=180)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)


        # riga 3
        self._ddDirector = ft.Dropdown(label="Regista")
        self._txtInN = ft.TextField(label="Numero di registi")
        self._btnTrovaGruppo = ft.ElevatedButton(text="Gruppo registi",
                                                  on_click=self._controller.handleTrovaGruppo)

        row3 = ft.Row([ft.Container(self._ddDirector, width=300),
                       ft.Container(self._txtInN, width=150),
                       ft.Container(self._btnTrovaGruppo, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View for output print
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()


    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

    def _dpFrom_change(self, e):
        self._txtDateFrom.value = "Selezione dal: " + str(e.control.value).split()[0]
        self.update_page()

    def _dpTo_change(self, e):
        self._txtDateTo.value = "al: " + str(e.control.value).split()[0]
        self.update_page()
