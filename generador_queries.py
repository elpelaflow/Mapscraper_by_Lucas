from itertools import product

estructura_geografica = {
    "caba": [
        "retiro", "san nicolas", "monserrat", "constitucion", "san telmo", "puerto madero",
        "recoleta", "balvanera", "san cristobal", "nueva pompeya", "parque patricios", "barracas",
        "la boca", "almagro", "boedo", "caballito", "flores", "parque chacabuco", "villa lugano",
        "villa soldati", "villa riachuelo", "liniers", "mataderos", "parque avellaneda", "villa real",
        "versalles", "villa luco", "velez sarfield", "floresta", "monte castro", "villa devoto",
        "villa del parque", "villa santa rita", "villa general mitre", "saavedra", "coghlan",
        "villa urquiza", "villa pueyrredon", "nuñez", "belgrano", "colegiales", "palermo",
        "villa ortuzar", "parque chas", "agronomia", "la paternal", "villa crespo"
    ],
    "buenos aires": [
        "san fernando", "san isidro", "vicente lopez", "san martin", "tres de febrero", "hurlingham",
        "ituzaingo", "moron", "matanza norte", "lomas de zamora", "lanus", "avellaneda", "tigre",
        "malvinas argentinas", "jose c paz", "san miguel", "moreno", "merlo", "matanza sur",
        "ezeiza", "esteban echeverria", "almirante brown", "florencio varela", "berazategui", "quilmes",
        "zarate", "campana", "exaltacion de la cruz", "lujan", "general rodriguez", "marcos paz",
        "general las heras", "cañuelas", "san vicente", "coronel brandsen", "la plata", "berisso",
        "ensenada", "bahia blanca", "mar del plata", "tandil", "san nicolas"
    ],
    "tucuman": ["san miguel de tucuman", "yerba buena", "tafi viejo", "cruz alta", "chicligasta"],
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
    "santiago del estero": ["santiago del estero"]
}

def generar_queries():
    print("🧠 Generador avanzado de Example Queries para scraping")

    tipos_negocio = input("👉 Tipos de negocio (ej: Fábrica, Proveedor). Separá por coma: ").strip().lower().split(",")
    rubros = input("👉 Rubros o productos (ej: calzado, lencería). Separá por coma: ").strip().lower().split(",")
    localidades_input = input("👉 Localidades o barrios (opcional). Separá por coma o dejá vacío: ").strip().lower()
    ciudad_input = input("👉 Ciudad o departamento (ej: caba, rosario, etc.): ").strip().lower()
    provincia_input = input("👉 Provincia (ej: buenos aires, tucuman): ").strip().lower()
    pais = input("👉 País: ").strip()

    tipos_negocio = [t.strip() for t in tipos_negocio if t.strip()]
    rubros = [r.strip() for r in rubros if r.strip()]
    localidades = []

    if not tipos_negocio or not rubros or not provincia_input or not pais:
        print("❌ Faltan datos obligatorios. Abortando.")
        return

    # CASO ESPECIAL CABA
    if ciudad_input == "caba":
        ciudad = "ciudad autonoma de buenos aires"
        provincia = "buenos aires"
        if not localidades_input:
            localidades = estructura_geografica.get("caba", [])
        else:
            localidades = [l.strip() for l in localidades_input.split(",") if l.strip()]
    else:
        ciudad = ciudad_input if ciudad_input else provincia_input
        provincia = provincia_input

        if localidades_input:
            localidades = [l.strip() for l in localidades_input.split(",") if l.strip()]
        elif ciudad_input in estructura_geografica:
            localidades = estructura_geografica[ciudad_input]
        else:
            localidades = estructura_geografica.get(provincia_input, [])

    if not localidades:
        print("⚠️ No se encontraron localidades para combinar. Abortando.")
        return

    combinaciones = product(tipos_negocio, rubros, localidades)
    queries = [f"{tipo} de {rubro} en {localidad}, {ciudad}, {provincia}, {pais}" for tipo, rubro, localidad in combinaciones]

    with open("example-queries.txt", "w", encoding="utf-8") as f:
        for query in queries:
            f.write(query + "\n")

    print(f"\n✅ Se generaron {len(queries)} queries en 'example-queries.txt'")

if __name__ == "__main__":
    generar_queries()
