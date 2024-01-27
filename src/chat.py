import json

def calcular_similitud(cadena1, cadena2):
    """
    Función para calcular la similitud entre dos cadenas.
    Devuelve un valor entre 0 y 1, donde 1 indica cadenas idénticas.
    """
    longitud_cadena1 = len(cadena1)
    longitud_cadena2 = len(cadena2)

    matriz = [[0] * (longitud_cadena2 + 1) for _ in range(longitud_cadena1 + 1)]

    for i in range(longitud_cadena1 + 1):
        for j in range(longitud_cadena2 + 1):
            if i == 0:
                matriz[i][j] = j
            elif j == 0:
                matriz[i][j] = i
            elif cadena1[i - 1] == cadena2[j - 1]:
                matriz[i][j] = matriz[i - 1][j - 1]
            else:
                matriz[i][j] = 1 + min(matriz[i - 1][j],        # Eliminación
                                       matriz[i][j - 1],        # Inserción
                                       matriz[i - 1][j - 1])    # Sustitución

    max_longitud = max(longitud_cadena1, longitud_cadena2)
    similitud = 1 - (matriz[longitud_cadena1][longitud_cadena2] / max_longitud)

    return similitud

def cargar_preguntas():
    try:
        with open('preguntas.json', 'r') as file:
            preguntas_guardadas = json.load(file)
    except FileNotFoundError:
        preguntas_guardadas = {}

    return preguntas_guardadas

def guardar_pregunta(pregunta):
    preguntas_guardadas = cargar_preguntas()

    # Si la pregunta ya existe en el archivo, incrementar el contador
    if pregunta in preguntas_guardadas:
        preguntas_guardadas[pregunta] += 1
    else:
        preguntas_guardadas[pregunta] = 1

    # Cambiar 'surtir' a 'change' en el JSON
    if 'surtir' in preguntas_guardadas:
        preguntas_guardadas['change'] = preguntas_guardadas.pop('surtir')

    with open('preguntas.json', 'w') as file:
        json.dump(preguntas_guardadas, file, indent=2)

def traducir_texto(texto, idioma_destino='en'):
    # Implementación simple de traducción para algunos idiomas
    diccionario_traducciones = {
        'es': {'what is your name?': '¿cuál es tu nombre?', 'how are you?': '¿cómo estás?'},
        'en': {'¿cuál es tu nombre?': 'what is your name?', '¿cómo estás?': 'how are you?'},
        'fr': {'what is your name?': 'quel est votre nom?', 'how are you?': 'comment ça va?', 'surtir': 'change'}
    }

    return diccionario_traducciones.get(idioma_destino, {}).get(texto, texto)

def responder_pregunta(pregunta, idioma='es', umbral_similitud=0.7, procesadas=None):
    if procesadas is None:
        procesadas = set()

    preguntas_guardadas = cargar_preguntas()

    # Calcular la similitud entre la pregunta del usuario y las preguntas guardadas
    similitudes = [(pregunta_guardada, calcular_similitud(pregunta.lower(), pregunta_guardada.lower()))
                   for pregunta_guardada in preguntas_guardadas]

    # Ordenar por similitud descendente
    similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)

    # Obtener la pregunta más similar
    pregunta_similar, similitud_maxima = similitudes[0]

    # Responder si la similitud es mayor que el umbral
    if similitud_maxima > umbral_similitud:
        # Evitar procesar la misma pregunta nuevamente para evitar recursión infinita
        if pregunta_similar not in procesadas:
            procesadas.add(pregunta_similar)
            respuesta_similar = responder_pregunta(pregunta_similar, idioma, procesadas=procesadas)
            return f"Probablemente quisiste preguntar: '{pregunta_similar}'. Mi respuesta es: {respuesta_similar}"

    # Resto de la lógica para responder preguntas
    if idioma == 'es':
        if pregunta.lower() == "¿cuál es tu nombre?":
            return "Soy una IA y no tengo un nombre específico."
        elif pregunta.lower() == "¿cómo estás?":
            return "Estoy bien, gracias por preguntar."
        elif pregunta.lower() in preguntas_guardadas:
            return f"La respuesta a esa pregunta es: {preguntas_guardadas[pregunta.lower()]}"
        else:
            guardar_pregunta(pregunta.lower())  # Guardar la pregunta no contestada
            return "Lo siento, no tengo información sobre eso."
    elif idioma == 'en':
        pregunta_en = traducir_texto(pregunta, idioma_destino='en')
        # Aquí puedes implementar lógica de respuesta en inglés
        if pregunta_en.lower() == "what is your name?":
            return "I am an AI and I don't have a specific name."
        elif pregunta_en.lower() == "how are you?":
            return "I am doing well, thank you for asking."
        elif pregunta_en.lower() in preguntas_guardadas:
            return f"The answer to that question is: {preguntas_guardadas[pregunta_en.lower()]}"
        else:
            guardar_pregunta(pregunta.lower())  # Guardar la pregunta no contestada
            return "Sorry, I don't have information about that."
    elif idioma == 'fr':
        pregunta_fr = traducir_texto(pregunta, idioma_destino='fr')
        # Implementar la lógica para salir de la IA si se ingresa 'surtir'
        if pregunta_fr.lower() == "surtir":
            guardar_pregunta(pregunta_fr.lower())  # Guardar la pregunta no contestada
            return "Au revoir! (Goodbye!)"
        # Aquí puedes implementar lógica de respuesta en francés
        elif pregunta_fr.lower() == "quel est votre nom?":
            return "Je suis une IA et je n'ai pas de nom spécifique."
        elif pregunta_fr.lower() == "comment ça va?":
            return "Je vais bien, merci de demander."
        elif pregunta_fr.lower() in preguntas_guardadas:
            return f"La réponse à cette question est : {preguntas_guardadas[pregunta_fr.lower()]}"
        else:
            guardar_pregunta(pregunta.lower())  # Guardar la pregunta no contestada
            return "Désolé, je n'ai pas d'information à ce sujet."


def main():
    print("¡Bienvenido! Puedes preguntarme en español, inglés o francés. Escribe 'salir' para terminar la conversación.")

    while True:
        idioma_usuario = input("Selecciona tu idioma (es/en/fr): ").lower()

        if idioma_usuario not in ['es', 'en', 'fr']:
            print("Idioma no válido. Selecciona 'es', 'en' o 'fr'.")
            continue

        entrada_usuario = input("Usuario: ")

        if entrada_usuario.lower() == 'salir':
            print("¡Hasta luego!")
            break

        respuesta = responder_pregunta(entrada_usuario, idioma=idioma_usuario)
        print(f"IA ({idioma_usuario}):", respuesta)

        # Salir de la IA si la respuesta contiene 'Au revoir!'
        if 'Au revoir!' in respuesta:
            break

if __name__ == "__main__":
    main()
