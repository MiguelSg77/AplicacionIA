from openai import OpenAI

client = OpenAI(base_url="http://10.11.0.174:1234/v1", api_key="lm-studio")

frase = input("Escribe una frase: ")
listaPalabras = frase.split(" ")
listaDefiniciones = []

try:

   for palabra in listaPalabras:
          respuesta = client.chat.completions.create(
       model = "qwen/qwen3.5-9b", messages = [{"role": "user", "content": "Define en 30 palabras la palabra: " + palabra}]
        )
          listaDefiniciones.append(palabra + ": " + respuesta.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")

    for definicion in listaDefiniciones:
        print(definicion)