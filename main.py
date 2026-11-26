import time
from openai import OpenAI

client = OpenAI(
    base_url="http://10.11.0.174:1234/v1",
    api_key="lm-studio",
    timeout=120,  # el razonamiento puede alargar la espera
)

MODELO = "qwen/qwen3.5-4b"
SISTEMA = (
    "Eres un diccionario. Respondes siempre en español, con una sola frase "
    "de máximo 30 palabras, sin introducciones ni listas."
)

frase = input("Escribe una frase: ")
listaPalabras = frase.split()
listaDefiniciones = []

for palabra in listaPalabras:
    inicio = time.time()
    try:
        respuesta = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": SISTEMA},
                {"role": "user", "content": "Define la palabra: " + palabra},
            ],
            max_tokens=1500,  # margen para razonar Y responder, pero con tope
            temperature=0.7,
            top_p=0.8,
        )
        eleccion = respuesta.choices[0]
        texto = (eleccion.message.content or "").strip()
        if not texto:
            texto = "(sin respuesta: se agotó el límite de tokens razonando)"
        segundos = time.time() - inicio
        listaDefiniciones.append(f"{palabra}: {texto}  [{segundos:.1f} s]")
    except Exception as e:
        listaDefiniciones.append(f"{palabra}: ERROR - {e}")

for definicion in listaDefiniciones:
    print(definicion)