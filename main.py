import flet as ft
from flet.core import icon_button
from flet.core.elevated_button import ElevatedButton
from flet.core.theme import IconButtonTheme

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    txt_tipo=ft.TextField(label="Tipo")
    txt_marca = ft.TextField(label="Marca")
    txt_anno = ft.TextField(label="Anno")
    txt_valore= ft.Text(value="0.0")

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungiNuovoStrumento(e):
        try:
            tipo = txt_tipo.value
            marca = txt_marca.value
            anno = int(txt_anno.value)
            valore = float(txt_valore.value)

            deposito.aggiungi_strumento(tipo, marca, anno, valore)
            txt_tipo.value = ""
            txt_marca.value = ""
            txt_anno.value = ""
            txt_valore.value = "0.0"
            aggiorna_lista_strumenti()

        except ValueError:
            alert.show_alert("❌ Errore: il valore attuale non è un numero valido.")

    def aumentaValore(e):
            valore_attuale = float(txt_valore.value)
            txt_valore.value = str(valore_attuale + 50.0)
            page.update()

    def diminuisciValore(e):
            valore_attuale = float(txt_valore.value)
            if valore_attuale >= 50.0:
                txt_valore.value = str(valore_attuale - 50.0)
            else:
                txt_valore.value = "0.0"
            page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    bottoneAggiungiStrumento=ft.ElevatedButton(text="Aggiungi strumento",on_click=aggiungiNuovoStrumento)
    bottoneAumentaValore=ft.ElevatedButton(text="+" , on_click=aumentaValore)
    bottoneDiminuisciValore=ft.ElevatedButton(text="-" , on_click=diminuisciValore)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(controls=[txt_tipo, txt_marca, txt_anno , bottoneDiminuisciValore, txt_valore, bottoneAumentaValore, bottoneAggiungiStrumento]
               , alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
