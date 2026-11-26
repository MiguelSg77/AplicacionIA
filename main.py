import os
import time
from openai import OpenAI

ARCHIVO = "definiciones.txt"

client = OpenAI(
    base_url="http://10.11.0.174:1234/v1",
    api_key="lm-studio",
    timeout=120,
)

MODELO = "qwen/qwen3.5-4b"
SISTEMA = (
    "Eres un diccionario. Respondes siempre en español, con una sola frase "
    "de máximo 30 palabras, sin introducciones ni listas."
)
SISTEMA_CONTEXTO = (
    "Eres un comentarista de textos con muy buen oído para el tono y la "
    "intención. Te doy una frase y las definiciones literales de sus palabras. "
    "No analices la frase de forma estricta ni literal: interpreta lo que la "
    "persona quiere decir de verdad y da tu opinión sobre ella.\n"
    "Ten en cuenta lo siguiente:\n"
    "- Si lo que se dice choca con la situación que se describe (por ejemplo, "
    "alabar algo que claramente es negativo), es una ironía o un sarcasmo: dilo "
    "con claridad y explica qué se quiere decir en realidad.\n"
    "- Si hay sentido figurado, humor, exageración, queja o crítica, "
    "identifícalo.\n"
    "- Si la frase es literal y sincera, dilo también: no veas ironía donde no "
    "la hay.\n"
    "Ejemplo: 'Qué bien, otro atasco justo cuando llego tarde.' -> Es una "
    "ironía: quien habla finge alegría para expresar su frustración. Es una "
    "queja cotidiana, y me parece una forma muy humana de desahogarse con "
    "humor.\n"
    "Responde en español, en un solo párrafo de máximo 100 palabras. Empieza "
    "indicando el tono (literal, irónico, humorístico, crítico...), después "
    "explica qué puede significar y termina con tu opinión personal en una "
    "frase. Puedes hablar en primera persona ('me parece', 'creo que'), pero "
    "no inventes hechos que no se puedan deducir de la frase."
)

frase = input("Escribe una frase: ")
listaPalabras = frase.split()
listaDefiniciones = []
definicionesOk = []  # solo las respuestas reales, para dárselas al modelo como contexto

with open(ARCHIVO, "a", encoding="utf-8") as archivo:
    for palabra in listaPalabras:
        inicio = time.time()
        try:
            respuesta = client.chat.completions.create(
                model=MODELO,
                messages=[
                    {"role": "system", "content": SISTEMA},
                    {"role": "user", "content": "Define la palabra: " + palabra},
                ],
                max_tokens=1500,
                temperature=0.7,
                top_p=0.8,
            )
            eleccion = respuesta.choices[0]
            texto = (eleccion.message.content or "").strip()
            segundos = time.time() - inicio

            if texto:
                archivo.write(f"{palabra}: {texto}\n")
                archivo.flush()
                definicionesOk.append(f"- {palabra}: {texto}")
            else:
                texto = "(sin respuesta: se agotó el límite de tokens razonando)"

            listaDefiniciones.append(f"{palabra}: {texto}  [{segundos:.1f} s]")
        except Exception as e:
            listaDefiniciones.append(f"{palabra}: ERROR - {e}")

for definicion in listaDefiniciones:
    print(definicion)

# --- Contexto de la frase ---
print("\nAnalizando el contexto de la frase...")
inicio = time.time()
try:
    respuesta = client.chat.completions.create(
        model=MODELO,
        messages=[
            {"role": "system", "content": SISTEMA_CONTEXTO},
            {
                "role": "user",
                "content": f'Frase: "{frase}"\n\nDefiniciones literales de sus palabras (pueden no reflejar el sentido real en la frase):\n'
+ ("\n".join(definicionesOk) or "(sin definiciones)"),
            },
        ],
        max_tokens=600,
        temperature=0.7,
        top_p=0.8,
    )
    explicacion = (respuesta.choices[0].message.content or "").strip()
    segundos = time.time() - inicio

    if explicacion:
        print(f"\nContexto de la frase [{segundos:.1f} s]:\n{explicacion}")
        with open(ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(f"\nFrase: {frase}\nContexto: {explicacion}\n\n")
    else:
        print("\n(sin respuesta: se agotó el límite de tokens)")
except Exception as e:
    print(f"\nERROR al analizar el contexto: {e}")

print("\nResultados guardados en:", os.path.abspath(ARCHIVO))