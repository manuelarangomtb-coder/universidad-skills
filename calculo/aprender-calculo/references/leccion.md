# Contrato de la lección

Todos los textos son español legible. Los campos de texto son texto plano; utiliza Unicode para fórmulas simples (Δx, x², ∑, ∫, →) y explica su lectura. No escribas LaTeX sin un renderizador local. Los campos `svg` son SVG autocontenidos creados por el autor: `viewBox`, ejes, unidades cuando correspondan, títulos y etiquetas legibles. Evita scripts, eventos, enlaces y recursos externos. El constructor rechaza contenido activo. La plantilla adapta el SVG al ancho disponible y usa `alt` como descripción accesible.

## Estructura JSON

```json
{
  "id": "tema-nivel-v1",
  "title": "Título del tema",
  "subtitle": "Una invitación breve y concreta",
  "objective": "Lo que podrás hacer al terminar",
  "prerequisites": "Recordatorio mínimo",
  "takeaway": "Idea que vale la pena recordar",
  "tutorial": [
    {"title": "Una idea a la vez", "body": "Explicación breve", "formula": "Fórmula explicada", "svg": "<svg viewBox=\"0 0 600 320\">...</svg>", "alt": "Descripción de lo representado"}
  ],
  "simulation": {
    "title": "Explora un cambio",
    "intro": "Qué representa y qué se puede modificar",
    "controlLabel": "Nombre del parámetro",
    "question": "Predicción que comprobarás al mover el control",
    "frames": [
      {"label": "Valor del parámetro", "svg": "<svg viewBox=\"0 0 600 320\">...</svg>", "alt": "Descripción de este estado", "description": "Qué cambió y por qué", "metrics": [{"label": "Magnitud", "value": "Valor y unidad"}]}
    ]
  },
  "applications": [{"title": "Situación cotidiana", "body": "Conexión concreta con el concepto y las unidades"}],
  "training": [
    {"title": "Ejemplo guiado", "prompt": "Enunciado completo", "steps": [
      {"title": "Una decisión", "prompt": "Pregunta", "options": ["A", "B", "C"], "correct": 1, "feedback": ["Pista específica A", "Por qué B funciona", "Pista específica C"], "explanation": "Procedimiento tras el intento", "calculation": "Sustitución → operación → resultado"}
    ]}
  ],
  "exercises": [
    {"id": "e1", "title": "Un reto pequeño", "concept": "Concepto a reforzar", "prompt": "Enunciado sin ambigüedades", "options": ["A", "B", "C", "D"], "correct": 2, "feedback": ["Razón A", "Razón B", "Razón C", "Razón D"], "steps": ["Misma estructura de paso que en training; usar objetos, no cadenas"]}
  ]
}
```

El esquema anterior ilustra tipos y campos; las listas reales deben contener 3–5 tarjetas de tutorial, 1–2 aplicaciones, tres ejemplos guiados con al menos dos pasos cada uno, al menos dos pasos de ayuda por ejercicio y exactamente diez ejercicios. `correct` es un índice entero desde cero. Las opciones de cada pregunta deben ser distintas, con una sola respuesta válida incluso al considerar equivalencias algebraicas y redondeos. Cada `feedback` tiene la misma longitud que `options`. `formula` y `calculation` son opcionales; el resto de campos mostrados son obligatorios. En los pasos finales de ayuda incluye la solución al enunciado original.

## Simulación

Precalcula 12–60 fotogramas para un parámetro pertinente y valores matemáticamente consistentes. El control deslizante selecciona un fotograma, actualiza el dibujo, sus métricas y la explicación. También admite reproducción y pausa, que se detiene al cambiar de sección. Al reconstruir una lección se vuelve al primer fotograma; no se guarda su posición. Respeta la preferencia de reducir movimiento y no arranques la animación automáticamente.

Ejemplos: número de rectángulos y suma aproximada para Riemann; distancia entre dos puntos y pendiente secante para derivadas; cercanía a un punto y valores de f(x) para límites; extremo superior y acumulación para integrales. No presentes una animación decorativa como simulación. Identifica aproximaciones y restricciones (lados de un límite, signo del área, hipótesis de una regla); evita generalizar propiedades de una función concreta. La plantilla sirve para temas nuevos generando otros fotogramas; no está limitada al motor de Riemann del ejemplo.

## Comportamiento incorporado

- Cuatro secciones: Descubre, Explora, Entrena y Practica. Entrena muestra una tarjeta por paso, opciones y botones anterior/siguiente. Tras elegir una opción, la flecha revela su procedimiento antes de avanzar al paso siguiente. «Ver juntos» permite pedir la explicación sin acertar ni adivinar.
- Para abrir la evaluación se completan los tres ejemplos guiados. Se puede volver a consultar las secciones anteriores. No hay bloqueo por respuestas incorrectas en entrenamiento.
- Practica muestra un solo ejercicio, permite seleccionar y confirmar una opción y evalúa inmediatamente con retroalimentación específica. El primer intento queda guardado. Se puede reintentar, abrir ayuda antes o después de contestar, y avanzar tras una respuesta evaluada. El ejercicio se conserva al cerrar la ayuda.
- La ayuda es un diálogo modal con el mismo carrusel de pasos. Pedir ayuda se registra; no bloquea la práctica. Completar la ayuda no cuenta como acertar la pregunta original: el estudiante debe responderla.
- El resumen aparece después de evaluar los diez ejercicios. Muestra aciertos iniciales sin apoyo, resolución posterior, apoyo utilizado y conceptos que conviene retomar. Desde allí se puede volver a cada pregunta.
- El avance se guarda en `localStorage` por identificador y huella del contenido. Cambiar el JSON produce una sesión nueva. Si el navegador no permite persistencia, la sesión funciona en memoria y lo indica. No hay cuentas, telemetría ni datos enviados.
- «Empezar de nuevo» pide confirmación dentro del navegador y solo borra el avance de esta lección. La página admite móvil, foco visible, teclado, etiquetas accesibles, avisos en vivo y movimiento reducido.

## Validación de una lección nueva

El constructor valida estructura, cantidades, referencias correctas, textos y SVG pasivos. No comprueba la verdad matemática. Recalcula por separado todas las respuestas y comprueba que el último paso de ayuda corresponde a la opción correcta. Prueba especialmente el error → explicación → reintento, pedir ayuda antes de responder, volver de una ayuda y continuar, cerrar y reabrir, y los diez ejercicios hasta el resumen. Un cambio en el enunciado requiere revisar también distractores, pistas y ayuda.
