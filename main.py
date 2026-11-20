import requests

URL = "http://10.11.0.174:1234/api/v1/chat"
MODELO = "qwen/qwen3.5-9b"
SISTEMA = (
    "Eres un diccionario. Respondes siempre en español, con una sola frase "
    "de máximo 30 palabras, sin introducciones ni listas."
)


def definir(palabra):
    cuerpo = {
        "model": MODELO,
        "input": SISTEMA + "\n\nDefine la palabra: " + palabra,
        "reasoning": "off",
        "max_output_tokens": 150,
        "temperature": 0.7,
    }
    r = requests.post(URL, json=cuerpo, timeout=60)
    r.raise_for_status()
    datos = r.json()
    partes = [
        str(item.get("content", ""))
        for item in datos.get("output", [])
        if item.get("type") == "message"
    ]
    texto = " ".join(partes).strip()
    if not texto:
        return "(sin respuesta) " + str(datos)[:300]
    return texto


frase = input("Escribe una frase: ")
listaDefiniciones = []

for palabra in frase.split():
    try:
        listaDefiniciones.append(palabra + ": " + definir(palabra))
    except Exception as e:
        listaDefiniciones.append(palabra + ": ERROR - " + str(e))

for definicion in listaDefiniciones:
    print(definicion)