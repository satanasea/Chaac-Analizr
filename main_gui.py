#########################################################################################################
#                                                                                                       #
#   _____  _    _                     _____             _   _          _      _____  ______  _____      #
#  / ____|| |  | |    /\        /\   / ____|      /\   | \ | |   /\   | |    |_   _||___  / |  __ \     #
# | |     | |__| |   /  \      /  \ | |          /  \  |  \| |  /  \  | |      | |     / /  | |__) |    #
# | |     |  __  |  / /\ \    / /\ \| |         / /\ \ | . ` | / /\ \ | |      | |    / /   |  _  /     #
# | |____ | |  | | / ____ \  / ____ \ |____    / ____ \| |\  |/ ____ \| |____ _| |_  / /__  | | \ \     #
#  \_____||_|  |_|/_/    \_\/_/    \_\_____|  /_/    \_\_| \_/_/    \_\______|_____|/_____| |_|  \_\    #
#                                                                                                       #
#########################################################################################################
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from registro_climatico import RegistroClimatico
from analizador import Analizador

BG       = "#000000"
FG       = "#ffffff"
OK_C     = "#56d364"
WARN_C   = "#f0883e"
BAD_C    = "#ff7b72"
FONT     = ("Consolas", 10) 
FONT_B   = ("Consolas", 10, "bold")
FONT_BIG = ("Consolas", 20, "bold")

def seccion(parent, titulo, **kwargs):
    frame = tk.LabelFrame(parent, text=f"  {titulo}  ", font=FONT_B,
                          bg=BG, fg=FG, bd=0, relief="solid",
                          labelanchor="nw", **kwargs)
    return frame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chaac AnaliZR")
        self.geometry("1280x760")
        self.minsize(900, 600)
        self.configure(bg=BG)       
        self.registro   = None
        self.analizador = None
        self._ui()

    def _ui(self):
        
        toolbar = tk.Frame(self, bg=BG, pady=6)
        toolbar.pack(fill="x", padx=10)

        tk.Label(toolbar, text="Chaac AnaliZR",
                 font=("Consolas", 13, "bold"), bg=BG, fg=FG).pack(side="left")

        tk.Button(toolbar, text="🔍", font=FONT_B, bg=BG, fg=OK_C,
                  relief="solid", bd=1, activebackground="#444", activeforeground=OK_C,
                  cursor="hand2", command=self._cargar).pack(side="right", padx=4)

        tk.Button(toolbar, text="✖", font=FONT, bg=BG, fg=BAD_C,
                  relief="solid", bd=0, activebackground=BG, activeforeground=BAD_C,
                  cursor="hand2", command=self._limpiar).pack(side="right", padx=4)

        
        fila_cards = tk.Frame(self, bg=BG)
        fila_cards.pack(fill="x", padx=10, pady=(0, 6))

        self.cards = {}
        for i, (key, label) in enumerate([
            ("registros",  "Total registros"),
            ("temp_prom",  "Temp. promedio"),
            ("hum_prom",   "Humedad prom."),
            ("lluvia_max", "Lluvia máx."),
            ("ok",         "Condiciones OK"),
            ("criticas",   "Alertas críticas"),
        ]):
            fila_cards.columnconfigure(i, weight=1)
            f = tk.LabelFrame(fila_cards, text=f"  {label}  ", font=("Consolas", 10),
                               bg=BG, fg=FG, bd=1, relief="solid")
            f.grid(row=0, column=i, padx=4, pady=4, sticky="ew")

            # Color segun el tipo de card
            color = BAD_C if key == "criticas" else OK_C if key == "ok" else FG
            lbl = tk.Label(f, text="—", font=FONT_BIG, bg=BG, fg=color)
            lbl.pack(pady=4, padx=8)
            self.cards[key] = lbl

        
        cuerpo = tk.Frame(self, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        sec_tabla = seccion(cuerpo, "Datos de monitoreo")
        sec_tabla.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self._build_tabla(sec_tabla)

        sec_graf = seccion(cuerpo, "Gráficas")
        sec_graf.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        self._build_graficas(sec_graf)

    def _build_tabla(self, parent):
        cols  = ("fecha_hora", "temp_C", "hum_pct", "lluvia_mm", "ubicacion", "estado")
        heads = ("Fecha/Hora", "Temp °C", "Hum %", "Lluvia mm", "Ubicación", "Estado")
        anchos = (140, 70, 60, 80, 90, 190)

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("S.Treeview", background=BG, foreground=FG,
                         fieldbackground=BG, rowheight=21, font=FONT)
        style.configure("S.Treeview.Heading", background=BG,
                         foreground=FG, font=FONT_B, relief="flat")
        style.map("S.Treeview.Heading", background=[("active", BG)])
        style.map("S.Treeview", background=[("selected", "#444")],
                  foreground=[("selected", FG)])

        f = tk.Frame(parent, bg=BG)
        f.pack(fill="both", expand=True, padx=4, pady=4)

        self.tree = ttk.Treeview(f, columns=cols, show="headings", style="S.Treeview")
        for col, head, ancho in zip(cols, heads, anchos):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=ancho, minwidth=ancho, anchor="center")

        
        self.tree.tag_configure("ok",   foreground=OK_C)
        self.tree.tag_configure("warn", foreground=WARN_C)
        self.tree.tag_configure("bad",  foreground=BAD_C)

        tk.Frame(f, bg=FG, height=1).pack(fill="x")
        self.tree.pack(fill="both", expand=True)

    def _build_graficas(self, parent):
        
        self.fig = Figure(figsize=(5, 4), facecolor=BG)
        self.fig.subplots_adjust(hspace=0.7, left=0.1, right=0.95, top=0.93, bottom=0.12)

        self.ax1 = self.fig.add_subplot(311)  # Temperatura
        self.ax2 = self.fig.add_subplot(312)  # Humedad
        self.ax3 = self.fig.add_subplot(313)  # Lluvia

        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_facecolor(BG)
            ax.tick_params(colors=FG, labelsize=7)
            for sp in ax.spines.values():
                sp.set_edgecolor("#555")
            ax.grid(True, color="#3c3c3c", linewidth=0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

    def _cargar(self):
        
        ruta = filedialog.askopenfilename(
            title="Seleccionar CSV",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
        )
        if not ruta:
            return
        try:
            self.registro = RegistroClimatico(ruta)
            self.registro.cargar_datos()
            self._analizar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _analizar(self):
        lecturas = self.registro.obtener_lecturas()
        self.analizador = Analizador(lecturas)
        resultados = self.analizador.analizar_todas()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        alertas = []
        for lectura, alerta in resultados:
            alertas.append(alerta)

            if "NO RECOMENDABLE" in alerta:
                tag, estado = "bad", "✖ NO COLAR CONCRETO  "
            elif "DEFICIENTES" in alerta:
                tag, estado = "warn", "⚠ SECADO DEFICIENTE"
            else:
                tag, estado = "ok", "✔ CONDICIONES OPTIMAS"

            self.tree.insert("", "end", values=(
                lectura.fecha_hora.strftime("%Y-%m-%d %H:%M"),
                f"{lectura.temperatura_C:.1f}",
                f"{lectura.humedad_pct:.0f}",
                f"{lectura.lluvia_mm:.1f}",
                lectura.ubicacion,
                estado
            ), tags=(tag,))
        
        temps   = [l.temperatura_C for l in lecturas]
        hums    = [l.humedad_pct   for l in lecturas]
        lluvias = [l.lluvia_mm     for l in lecturas]
        fechas  = [l.fecha_hora    for l in lecturas]

        self.cards["registros"].config(text=str(len(lecturas)))
        self.cards["temp_prom"].config(text=f"{sum(temps)/len(temps):.1f}°C")
        self.cards["hum_prom"].config(text=f"{sum(hums)/len(hums):.1f}%")
        self.cards["lluvia_max"].config(text=f"{max(lluvias):.1f}mm")
        self.cards["ok"].config(text=str(alertas.count("CONDICIONES OPTIMAS")))
        self.cards["criticas"].config(text=str(alertas.count("NO RECOMENDABLE COLAR CONCRETO")))
        
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.cla()
            ax.set_facecolor(BG)
            ax.tick_params(colors=FG, labelsize=7)
            for sp in ax.spines.values():
                sp.set_edgecolor("#555")
            ax.grid(True, color="#3c3c3c", linewidth=0.5)

        self.ax1.plot(fechas, temps, color="#e94560", linewidth=1.5, marker="o", markersize=2)
        self.ax1.set_title("Temperatura (°C)", color=FG, fontsize=8, pad=2)

        self.ax2.plot(fechas, hums, color="#79c0ff", linewidth=1.5, marker="s", markersize=2)
        self.ax2.set_title("Humedad (%)", color=FG, fontsize=8, pad=2)

        self.ax3.bar(fechas, lluvias, color="#56d364", width=0.04, alpha=0.85)
        self.ax3.set_title("Lluvia (mm)", color=FG, fontsize=8, pad=2)

        fmt = mdates.DateFormatter("%d/%m")
        loc = mdates.DayLocator()
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.xaxis.set_major_formatter(fmt)
            ax.xaxis.set_major_locator(loc)
            ax.tick_params(axis="x", colors=FG, labelsize=7, rotation=30)

        self.canvas.draw()

    def _limpiar(self):
        self.registro = None

        for item in self.tree.get_children():
            self.tree.delete(item)

        for key in self.cards:
            self.cards[key].config(text="—")

        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.cla()
            ax.set_facecolor(BG)
            for sp in ax.spines.values():
                sp.set_edgecolor("#555")
            ax.grid(True, color="#3c3c3c", linewidth=0.5)

        self.canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()