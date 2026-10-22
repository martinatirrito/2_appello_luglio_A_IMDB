import flet as ft
import traceback


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        date1 = self._view._dpFrom.value
        date2 = self._view._dpTo.value

        if date1 is None or date2 is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenziona selezionare date inizio e data fine", color="red"))
            self._view.update_page()
            return

        if date1 > date2:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenziona inserire range valido! Data inizio deve essere minore di data fine.", color = "red"))
            self._view.update_page()
            return

        try:
            self._model.buildGraph(date1, date2)
            self._view._btnStampaInfo.disabled = False
            self._view._txt_result.controls.clear()
            Nnodi, Narchi = self._model.getGraphDetails()
            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di nodi: {Nnodi}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {Narchi}")
            )

            self._view.update_page()

        except Exception as ex:
            traceback.print_exc()
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        nNodi, nArchi = self._model.getGraphDetails()
        if nNodi == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            best_degree, max_degree = self._model.getBestDegree()
            if best_degree:
                self._view._txt_result.controls.append(
                    ft.Text(f"Attore con grado maggiore: {best_degree} (grado: {max_degree})"))

            best_weight, max_weight = self._model.getSommaPesiIncidenti()
            if best_weight:
                self._view._txt_result.controls.append(
                    ft.Text(f"Attore con somma pesi incidenti massima: {best_weight} (somma: {max_weight})"))

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(ft.Text(""))

            top5 = self._model.top5Archi()
            if top5:
                self._view._txt_result.controls.append(
                    ft.Text("Top 5 archi con peso maggiore:"))
                for i, (u, v, weight) in enumerate(top5, 1):
                    self._view._txt_result.controls.append(
                        ft.Text(f"{i}. {u} -- {v} (peso: {weight})"))
            else:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun arco trovato."))

            self.fillDDRegisti()

            self._view.update_page()

        except Exception as ex:
            traceback.print_exc()
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")

    def fillDDRegisti(self):
        self._view._ddDirector.options.clear()
        registi = self._model.getAllRegisti()
        for r in registi:
            self._view._ddDirector.options.append(ft.dropdown.Option(str(r.name_id), text=str(r)))
        self._view.update_page()


    def handleTrovaGruppo(self, e):
        pass

