from openai import OpenAI

client = OpenAI(
    base_url="http://10.11.0.174:1234/v1",
    api_key="lm-studio",
    timeout=60,  # segundos máximos de espera por petición
)

MODELO = "qwen/qwen3.5-9b"
SISTEMA = (
    "Eres un diccionario. Respondes siempre en español, con una sola frase "
    "de máximo 30 palabras, sin introducciones ni listas."
)

frase = input("Escribe una frase: ")
listaPalabras = frase.split()  # split() ignora los espacios dobles
listaDefiniciones = []

for palabra in listaPalabras:
    try:
        respuesta = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": SISTEMA},
                {"role": "user", "content": "Define la palabra: " + palabra},
            ],
            max_tokens=300,
            temperature=0.7,
            top_p=0.8,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        )
        texto = respuesta.choices[0].message.content or "(sin respuesta)"
        if respuesta.choices[0].finish_reason == "length":
            texto += " [cortada por el límite de tokens]"
        listaDefiniciones.append(palabra + ": " + texto)
    except Exception as e:
        listaDefiniciones.append(palabra + ": ERROR - " + str(e))

for definicion in listaDefiniciones:
    print(definicion)