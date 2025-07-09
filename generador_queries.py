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
    pais = input("👉 País: ").strip()
    provincia_input = (
        input("👉 Provincia (ej: buenos aires, tucuman): ").strip().lower()
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
        print("❌ Faltan datos obligatorios. Abortando.")
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

        self.lb_tipos = self._create_listbox("Tipo de negocio", TIPOS_NEGOCIO_OPCIONES)        
        self.lb_localidades = self._create_listbox(
            "Localidades o barrios", [], height=8
        )
        self.lb_ciudades = self._create_listbox("Ciudad o departamento", [], height=5)
        self.lb_provincias = self._create_listbox("Provincia", [], height=5)
        self.lb_paises = self._create_listbox("País", PAISES_OPCIONES, height=5)

        self.lb_paises.bind("<<ListboxSelect>>", self.on_pais_select)
        self.lb_provincias.bind("<<ListboxSelect>>", self.on_provincia_select)
        self.lb_ciudades.bind("<<ListboxSelect>>", self.on_ciudad_select)

        tk.Button(
            root,
            text="Generar queries",
            command=self.on_generate,
            bg="#2D2A32",
            fg="white",
        ).pack(pady=10)

    def _create_listbox(self, label, options, height=6):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=label).pack()
        lb = tk.Listbox(
            frame,
            listvariable=tk.StringVar(value=options),
            selectmode=tk.MULTIPLE,
            height=height,
            exportselection=False,
            width=45,
        )
        lb.pack()
        return lb

    def _update_listbox(self, lb, options):
        lb.delete(0, tk.END)
        for opt in options:
            lb.insert(tk.END, opt)

    def on_pais_select(self, _event=None):
        paises = [self.lb_paises.get(i).lower() for i in self.lb_paises.curselection()]
        provincias = []
        for p in paises:
            provincias.extend(PROVINCIAS_POR_PAIS.get(p, []))
        self._update_listbox(self.lb_provincias, sorted(set(provincias)))
        self._update_listbox(self.lb_ciudades, [])
        self._update_listbox(self.lb_localidades, [])

    def on_provincia_select(self, _event=None):
        provs = [
            self.lb_provincias.get(i).lower() for i in self.lb_provincias.curselection()
        ]
        ciudades = []
        for p in provs:
            ciudades.extend(CIUDADES_POR_PROVINCIA.get(p, []))
        self._update_listbox(self.lb_ciudades, sorted(set(ciudades)))
        self._update_listbox(self.lb_localidades, [])

    def on_ciudad_select(self, _event=None):
        ciudades = [
            self.lb_ciudades.get(i).lower() for i in self.lb_ciudades.curselection()
        ]
        locs = []
        for c in ciudades:
            locs.extend(LOCALIDADES_POR_CIUDAD.get(c, []))
        self._update_listbox(self.lb_localidades, sorted(set(locs)))
    
    def on_generate(self):
        tipos = [self.lb_tipos.get(i).lower() for i in self.lb_tipos.curselection()]
        rubros = [
            r.strip().lower() for r in self.entry_rubros.get().split(",") if r.strip()
        ]
        locs = [
            self.lb_localidades.get(i).lower()
            for i in self.lb_localidades.curselection()
        ]
        ciudades = [
            self.lb_ciudades.get(i).lower() for i in self.lb_ciudades.curselection()
        ]
        provincias = [
            self.lb_provincias.get(i).lower() for i in self.lb_provincias.curselection()
        ]
        paises = [self.lb_paises.get(i) for i in self.lb_paises.curselection()]

        generar_queries(tipos, rubros, locs, ciudades, provincias, paises)


def generar_queries(tipos_negocio, rubros, localidades, ciudades, provincias, paises):
    """Genera las queries combinando las selecciones de la UI."""

    if not tipos_negocio or not rubros or not provincias or not paises:
        messagebox.showerror(
            "Datos faltantes",
            "Debes seleccionar al menos un tipo de negocio, rubro, provincia y país.",
        )
        return

    if not localidades:
        localidades = []
        if ciudades:
            for c in ciudades:
                locs = estructura_geografica.get(c, [])
                if locs:
                    localidades.extend(locs)
        if not localidades:
            for p in provincias:
                locs = estructura_geografica.get(p, [])
                if locs:
                    localidades.extend(locs)
        localidades = sorted(set(localidades))

        if not localidades:
            localidades = [""]

    combinaciones = product(
        tipos_negocio, rubros, localidades, ciudades or [""], provincias, paises    
    )

    queries = []
    for tipo, rubro, loc, ciudad, prov, pais in combinaciones:
        ciudad_final = ciudad if ciudad else prov
        if loc:
            queries.append(f"{tipo} de {rubro} en {loc}, {ciudad_final}, {prov}, {pais}")
        else:
            queries.append(f"{tipo} de {rubro} en {ciudad_final}, {prov}, {pais}")

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
