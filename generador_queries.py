from itertools import product
import tkinter as tk
from tkinter import messagebox

estructura_geografica = {
    "caba": [
        "retiro",
        "san nicolas",
        "monserrat",
        "constitucion",
        "san telmo",
        "puerto madero",
        "recoleta",
        "balvanera",
        "san cristobal",
        "nueva pompeya",
        "parque patricios",
        "barracas",
        "la boca",
        "almagro",
        "boedo",
        "caballito",
        "flores",
        "parque chacabuco",
        "villa lugano",
        "villa soldati",
        "villa riachuelo",
        "liniers",
        "mataderos",
        "parque avellaneda",
        "villa real",
        "versalles",
        "villa luco",
        "velez sarfield",
        "floresta",
        "monte castro",
        "villa devoto",
        "villa del parque",
        "villa santa rita",
        "villa general mitre",
        "saavedra",
        "coghlan",
        "villa urquiza",
        "villa pueyrredon",
        "nuñez",
        "belgrano",
        "colegiales",
        "palermo",
        "villa ortuzar",
        "parque chas",
        "agronomia",
        "la paternal",
        "villa crespo",
    ],
    "buenos aires": [
        "san fernando",
        "san isidro",
        "vicente lopez",
        "san martin",
        "tres de febrero",
        "hurlingham",
        "ituzaingo",
        "moron",
        "matanza norte",
        "lomas de zamora",
        "lanus",
        "avellaneda",
        "tigre",
        "malvinas argentinas",
        "jose c paz",
        "san miguel",
        "moreno",
        "merlo",
        "matanza sur",
        "ezeiza",
        "esteban echeverria",
        "almirante brown",
        "florencio varela",
        "berazategui",
        "quilmes",
        "zarate",
        "campana",
        "exaltacion de la cruz",
        "lujan",
        "general rodriguez",
        "marcos paz",
        "general las heras",
        "cañuelas",
        "san vicente",
        "coronel brandsen",
        "la plata",
        "berisso",
        "ensenada",
        "bahia blanca",
        "mar del plata",
        "tandil",
        "san nicolas",
    ],
    "tucuman": [
        "san miguel de tucuman",
        "yerba buena",
        "tafi viejo",
        "cruz alta",
        "chicligasta",
    ],
    "cordoba": ["cordoba", "rio cuarto", "colon", "punilla", "san justo"],
    "santa fe": ["rosario", "santa fe", "san lorenzo", "general lopez", "castellanos"],
    "mendoza": ["mendoza", "godoy cruz", "guaymallen", "maipu", "san rafael"],
    "entre rios": ["parana", "concordia", "gualeguaychú", "uruguay", "colon"],
    "salta": ["salta", "cerrillos", "oran", "cafayate", "general guemes"],
    "catamarca": ["san fernando del valle de catamarca"],
    "chaco": ["san fernando"],
    "chubut": ["rawson"],
    "corrientes": ["corrientes"],
    "formosa": ["formosa"],
    "jujuy": ["san salvador de jujuy"],
    "la pampa": ["santa rosa"],
    "la rioja": ["la rioja"],
    "misiones": ["posadas"],
    "neuquen": ["neuquen"],
    "rio negro": ["viedma"],
    "san juan": ["san juan"],
    "san luis": ["san luis"],
    "santa cruz": ["rio gallegos"],
    "santiago del estero": ["santiago del estero"],
}

# Opciones para la interfaz gráfica
TIPOS_NEGOCIO_OPCIONES = [
    "Fábrica",
    "Proveedor",
    "Distribuidor",
    "Mayorista",
    "Minorista",
]
LOCALIDADES_OPCIONES = sorted(
    {loc for locs in estructura_geografica.values() for loc in locs}
)
CIUDADES_OPCIONES = sorted(estructura_geografica.keys())
PROVINCIAS_OPCIONES = sorted([p for p in estructura_geografica.keys() if p != "caba"])
PAISES_OPCIONES = ["Argentina", "Uruguay", "Chile", "Brasil", "Paraguay"]

# Relaciones jerárquicas para las selecciones
PROVINCIAS_POR_PAIS = {
    "argentina": PROVINCIAS_OPCIONES,
}
CIUDADES_POR_PROVINCIA = {prov: [prov] for prov in PROVINCIAS_OPCIONES}
CIUDADES_POR_PROVINCIA["buenos aires"] = ["caba"] + estructura_geografica["buenos aires"]
LOCALIDADES_POR_CIUDAD = estructura_geografica

# Algunas ciudades se muestran con un nombre distinto al utilizarse en las
# consultas. Por ejemplo, "caba" se debe mostrar como "ciudad autónoma de
# buenos aires".
CIUDAD_DISPLAY = {
    "caba": "ciudad autónoma de buenos aires",
}


class MultiSelectDropdown:
    """Widget simple para seleccionar múltiples opciones en un menú desplegable."""

    def __init__(self, master, label, options, command=None):
        self.frame = tk.Frame(master)
        self.frame.pack(pady=5)
        tk.Label(self.frame, text=label).pack()

        self.button = tk.Menubutton(self.frame, text="Seleccione...", relief=tk.RAISED)
        self.button.pack()
        self.menu = tk.Menu(self.button, tearoff=False)
        self.button.config(menu=self.menu)

        self._label = label
        self.command = command
        self.vars = {}
        self.update_options(options)

    def update_options(self, options):
        self.menu.delete(0, tk.END)
        self.vars = {}
        for opt in options:
            var = tk.BooleanVar()
            self.menu.add_checkbutton(
                label=opt,
                variable=var,
                command=self._on_select,
            )
            self.vars[opt] = var
        self._update_label()

    def _on_select(self):
        self._update_label()
        if self.command:
            self.command()

    def _update_label(self):
        selected = [opt for opt, var in self.vars.items() if var.get()]
        text = ", ".join(selected) if selected else "Seleccione..."
        self.button.config(text=text)

    def get_selected(self):
        return [opt for opt, var in self.vars.items() if var.get()]


def generar_queries_cli():
    print("🧠 Generador avanzado de Example Queries para scraping")

    tipos_negocio = (
        input("👉 Tipos de negocio (ej: Fábrica, Proveedor). Separá por coma: ")
        .strip()
        .lower()
        .split(",")
    )
    rubros = (
        input("👉 Rubros o productos (ej: calzado, lencería). Separá por coma: ")
        .strip()
        .lower()
        .split(",")
    )
    pais = input("👉 País (obligatorio): ").strip()
    provincia_input = (
        input("👉 Provincia (obligatoria, ej: buenos aires, tucuman): ").strip().lower()
    )
    ciudad_input = (
        input("👉 Ciudad o departamento (ej: caba, rosario, etc.): ").strip().lower()
    )
    localidades_input = (
        input("👉 Localidades o barrios (opcional). Separá por coma o dejá vacío: ")
        .strip()
        .lower()
    )

    tipos_negocio = [t.strip() for t in tipos_negocio if t.strip()]
    rubros = [r.strip() for r in rubros if r.strip()]
    localidades = [l.strip() for l in localidades_input.split(",") if l.strip()]

    if not tipos_negocio or not rubros or not provincia_input or not pais:
        print(
            "❌ Faltan datos obligatorios. Debes ingresar país y provincia. "
            "Los campos 'Ciudad o departamento' y 'Localidades o barrios' son opcionales."
        )
        return

    generar_queries(
        tipos_negocio,
        rubros,
        localidades,
        [ciudad_input] if ciudad_input else [],
        [provincia_input],
        [pais],
    )


class QueryGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Generador de Example Queries")
        root.geometry("500x600")

        tk.Label(root, text="Rubros o productos (separados por coma)").pack(pady=5)
        self.entry_rubros = tk.Entry(root, width=50)
        self.entry_rubros.pack(pady=5)

        # Tipo de negocio como checkboxes
        self.tipo_vars = {}
        frame_tipos = tk.LabelFrame(root, text="Tipo de negocio")
        frame_tipos.pack(pady=5)
        for opt in TIPOS_NEGOCIO_OPCIONES:
            var = tk.BooleanVar()
            tk.Checkbutton(frame_tipos, text=opt, variable=var).pack(anchor="w")
            self.tipo_vars[opt] = var

        # Menús desplegables multiselección
        self.dd_localidades = MultiSelectDropdown(root, "Localidades o barrios", [])
        self.dd_ciudades = MultiSelectDropdown(
            root, "Ciudad o departamento", [], command=self.on_ciudad_select
        )
        self.dd_provincias = MultiSelectDropdown(
            root, "Provincia (obligatoria)", [], command=self.on_provincia_select
        )
        self.dd_paises = MultiSelectDropdown(
            root, "País (obligatorio)", PAISES_OPCIONES, command=self.on_pais_select
        )

        tk.Button(
            root,
            text="Generar queries",
            command=self.on_generate,
            bg="#2D2A32",
            fg="white",
        ).pack(pady=10)

    def _update_dropdown(self, dd, options):
        dd.update_options(options)

    def on_pais_select(self, _event=None):
        paises = [p.lower() for p in self.dd_paises.get_selected()]
        provincias = []
        for p in paises:
            provincias.extend(PROVINCIAS_POR_PAIS.get(p, []))
        self._update_dropdown(self.dd_provincias, sorted(set(provincias)))
        self._update_dropdown(self.dd_ciudades, [])
        self._update_dropdown(self.dd_localidades, [])

    def on_provincia_select(self, _event=None):
        provs = [p.lower() for p in self.dd_provincias.get_selected()]
        ciudades = []
        for p in provs:
            ciudades.extend(CIUDADES_POR_PROVINCIA.get(p, []))
        self._update_dropdown(self.dd_ciudades, sorted(set(ciudades)))
        self._update_dropdown(self.dd_localidades, [])

    def on_ciudad_select(self, _event=None):
        ciudades = [c.lower() for c in self.dd_ciudades.get_selected()]
        locs = []
        for c in ciudades:
            locs.extend(LOCALIDADES_POR_CIUDAD.get(c, []))
        self._update_dropdown(self.dd_localidades, sorted(set(locs)))

    def on_generate(self):
        tipos = [opt.lower() for opt, var in self.tipo_vars.items() if var.get()]
        rubros = [
            r.strip().lower() for r in self.entry_rubros.get().split(",") if r.strip()
        ]
        locs = [l.lower() for l in self.dd_localidades.get_selected()]
        ciudades = [c.lower() for c in self.dd_ciudades.get_selected()]
        provincias = [p.lower() for p in self.dd_provincias.get_selected()]
        paises = [p for p in self.dd_paises.get_selected()]

        generar_queries(tipos, rubros, locs, ciudades, provincias, paises)


def generar_queries(tipos_negocio, rubros, localidades, ciudades, provincias, paises):
    """Genera las queries combinando las selecciones de la UI."""

    if not tipos_negocio or not rubros or not provincias or not paises:
        messagebox.showerror(
            "Datos faltantes",
            "Debes seleccionar al menos un tipo de negocio, rubro, provincia y país. "
            "Los campos 'Ciudad o departamento' y 'Localidades o barrios' son opcionales.",
        )
        return

    user_selected_ciudades = bool(ciudades)
    if not ciudades:
        for p in provincias:
            ciudades.extend(CIUDADES_POR_PROVINCIA.get(p, []))
        ciudades = sorted(set(ciudades))

    queries = []
    for pais in paises:
        for prov in provincias:
            ciudades_actuales = (
                [c for c in ciudades if c in CIUDADES_POR_PROVINCIA.get(prov, [])]
                if ciudades
                else CIUDADES_POR_PROVINCIA.get(prov, [])
            )
            for ciudad in ciudades_actuales:
                if localidades:
                    locs = localidades
                elif user_selected_ciudades:
                    locs = estructura_geografica.get(ciudad, []) or [""]
                else:
                    locs = [""]
                for loc in locs:
                    for tipo in tipos_negocio:
                        for rubro in rubros:
                            ciudad_mostrar = CIUDAD_DISPLAY.get(ciudad, ciudad)
                            if loc:
                                queries.append(
                                    f"{tipo} de {rubro} en {loc}, {ciudad_mostrar}, {prov}, {pais}"
                                )
                            else:
                                queries.append(
                                    f"{tipo} de {rubro} en {ciudad_mostrar}, {prov}, {pais}"
                                )

    with open("example-queries.txt", "w", encoding="utf-8") as f:
        for q in queries:
            f.write(q + "\n")

    messagebox.showinfo(
        "Éxito", f"Se generaron {len(queries)} queries en 'example-queries.txt'"
    )


if __name__ == "__main__":
    root = tk.Tk()
    app = QueryGeneratorApp(root)
    root.mainloop()
