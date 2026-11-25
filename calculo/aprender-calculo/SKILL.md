---
name: aprender-calculo
description: Enseña un tema de cálculo mediante una lección HTML interactiva con tutorial visual, simulación, entrenamiento guiado y diez ejercicios evaluados con ayuda paso a paso. Úsala cuando el estudiante quiera aprender o practicar cálculo de esta manera.
---

# Aprender cálculo

## Conversación inicial

Si el usuario invoca la skill sin indicar tema, pregunta: «¿Qué tema de cálculo quieres aprender? Por ejemplo: límites, derivadas, integrales o sumas de Riemann». Espera su respuesta antes de crear la lección. Usa una pregunta conversacional o una herramienta de entrada disponible; no dependas de herramientas exclusivas del modo Plan. Si ya indicó el tema, empieza directamente. No presupongas sumas de Riemann: es solo un ejemplo.

Asume nivel principiante y español, salvo que el estudiante indique otra cosa. No exijas un cuestionario previo. Actúa como docente experto en el tema elegido: precisión matemática, lenguaje cotidiano y progresión desde la intuición. Explica símbolos antes de usarlos. Presenta los prerrequisitos con un recordatorio breve. Ante un tema demasiado amplio, elige y anuncia un primer objetivo concreto abordable en una sesión.

## Construir la experiencia

Lee [references/leccion.md](references/leccion.md) para el contrato de contenido y el comportamiento de la plantilla. Crea contenido original para el tema elegido; no cambies únicamente el título del ejemplo.

1. Escribe un JSON de lección con un objetivo, un tutorial breve de 3–5 tarjetas, ilustraciones matemáticas SVG con descripción textual, una simulación manipulable, una o dos aplicaciones cotidianas y tres ejemplos de entrenamiento de dificultad gradual.
2. Cada ejemplo guiado presenta preguntas sencillas de selección múltiple y un carrusel. El estudiante elige una opción; recibe retroalimentación específica; con la flecha avanza al procedimiento y al resultado. Se puede volver a pasos anteriores. No muestres la solución antes de su intento salvo que solicite verla.
3. Escribe exactamente diez ejercicios de selección múltiple, de menor a mayor dificultad, con una única respuesta correcta, distractores plausibles, explicación para cada opción y solución completa en pasos. Mezcla interpretación, cálculo y aplicaciones; distribuye la posición de las respuestas correctas. Comprueba las operaciones independientemente antes de entregar.
4. Utiliza el constructor y la plantilla reutilizables de esta skill:

   ```sh
   python3 <ruta-skill>/scripts/build_lesson.py <leccion.json> --output <tema>.html
   ```

   El HTML es autónomo: CSS, JavaScript, contenido e ilustraciones incluidos, sin servidor, CDN ni conexión. La plantilla incorpora navegación, evaluación, ayuda guiada, progreso y reinicio. Adapta sus recursos si el tema exige otro tipo de interacción, preservando esas funciones. Los SVG y fotogramas deben representar las matemáticas del tema, no ser decoración genérica.
5. Abre y prueba el HTML con las herramientas locales disponibles. Comprueba la simulación, un acierto, un error con reintento, la ayuda hasta su resultado, el paso de entrenamiento a evaluación y el resumen de diez ejercicios. Verifica teclado y pantalla estrecha. No afirmes haber hecho pruebas de navegador si solo revisaste código. Entrega un enlace al HTML generado y una invitación breve a comenzar.

El constructor crea carpetas de salida si hacen falta. Guarda las lecciones en el destino indicado o en una carpeta `lecciones/` del directorio de trabajo. No sustituyas una lección anterior del usuario sin necesidad; usa un nombre distinto cuando proceda. No publiques ni envíes resultados a terceros salvo que el usuario lo solicite.

## Trato al estudiante y evaluación

El objetivo es motivar. Evita cronómetros, vidas, penalizaciones por pedir ayuda, comparaciones y mensajes de fracaso. Ante un error, explica la confusión concreta y ofrece reintentar o recibir ayuda. Celebra el razonamiento y el progreso con mesura. Una explicación nunca se limita a «aplica la fórmula»: muestra sustitución, operación, unidades e interpretación cuando corresponda.

Evalúa los ejercicios uno por uno al confirmar la opción. Conserva el primer intento para informar el diagnóstico sin inflar resultados con reintentos. Permite reintentos y avanzar después de recibir retroalimentación. Distingue aciertos al primer intento sin ayuda, ejercicios resueltos después, ejercicios con apoyo y pendientes de resolver. Si pidió ayuda antes de acertar, no lo cuentes como resolución independiente. El resumen identifica conceptos por reforzar y propone una acción pequeña; no etiqueta al estudiante con una nota desmotivadora.

La ayuda de cada ejercicio reproduce el entrenamiento: pequeñas decisiones, flechas, procedimiento y resultado progresivos. No basta un cuadro con la respuesta final. Mantén las opciones del ejercicio original disponibles al cerrar la ayuda.

## Recursos

- [assets/lesson.html](assets/lesson.html): motor de la experiencia; el constructor inserta el JSON.
- [scripts/build_lesson.py](scripts/build_lesson.py): valida el contenido y produce un único HTML.
- [scripts/example_riemann.py](scripts/example_riemann.py): genera una lección completa de referencia y sus ilustraciones calculadas. Ejecuta `python3 <ruta-skill>/scripts/example_riemann.py --output-dir <carpeta>` y luego el constructor. Úsalo como referencia estructural; para otro tema, crea su contenido y simulación específicos.
