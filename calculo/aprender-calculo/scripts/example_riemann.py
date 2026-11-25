#!/usr/bin/env python3
"""Create a complete Riemann lesson with mathematically computed SVG frames."""
import argparse
import json
from pathlib import Path


def num(value):
    return f"{value:.4f}".rstrip("0").rstrip(".").replace(".", ",")


def plot(n, power=2, sample="right"):
    width = 2 / n
    x = lambda value: 65 + value * 230
    y = lambda value: 285 - value * 56
    rects = []
    total = 0
    for i in range(n):
        point = (i + (1 if sample == "right" else 0.5)) * width
        height = point ** power
        total += height * width
        rects.append(f'<rect x="{x(i*width):.3f}" y="{y(height):.3f}" width="{width*230:.3f}" height="{height*56:.3f}" fill="#d5ed83" fill-opacity="0.8" stroke="#658d35" stroke-width="1"/>')
    points = " ".join(f"{x(i/100):.2f},{y((i/100)**power):.2f}" for i in range(201))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350">
<title>Rectángulos que aproximan el área bajo la curva</title>
<g font-family="system-ui,sans-serif" font-size="17" fill="#163a36">
<text x="65" y="28" font-size="21">f(x) = {'x²' if power==2 else 'x'} · extremos {'derechos' if sample=='right' else 'medios'}</text>
<line x1="65" y1="61" x2="525" y2="61" stroke="#d7e0d6" stroke-dasharray="4 6"/>
{''.join(rects)}
<polyline points="{points}" fill="none" stroke="#175b49" stroke-width="4" stroke-linejoin="round"/>
<path d="M 65 45 V 285 H 550" fill="none" stroke="#163a36" stroke-width="2"/>
<text x="47" y="311">0</text><text x="289" y="311">1</text><text x="519" y="311">2</text><text x="555" y="291">x</text><text x="30" y="67">4</text><text x="28" y="179">2</text>
<text x="65" y="337" font-size="16">n = {n} · Δx = {num(width)} · suma ≈ {num(total)}</text>
</g></svg>'''
    return svg, total


def area_diagram():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350"><title>Área de un rectángulo: base por altura</title><g font-family="system-ui,sans-serif" fill="#163a36"><rect x="135" y="65" width="330" height="190" rx="6" fill="#d5ed83" stroke="#175b49" stroke-width="3"/><text x="300" y="155" text-anchor="middle" font-size="30">área = base × altura</text><text x="300" y="294" text-anchor="middle" font-size="24">base: Δx</text><text x="23" y="160" font-size="22">altura</text><path d="M 135 318 H 465 M 135 310 V 326 M 465 310 V 326" fill="none" stroke="#175b49" stroke-width="2"/></g></svg>'''


def step(title, prompt, options, correct, feedback, explanation, calculation):
    return dict(title=title, prompt=prompt, options=options, correct=correct,
                feedback=feedback, explanation=explanation, calculation=calculation)


def width_step(a, b, n):
    w = (b-a)/n
    return step("Primero, el ancho", f"Dividimos [{a}, {b}] en {n} partes iguales. ¿Cuánto mide Δx?",
                [num(w), num(2*w), num(3*w)], 0,
                ["Sí: repartes la longitud total entre el número de partes.", "Ese ancho es el doble del necesario. Divide la longitud total entre n.", "Ese ancho es demasiado grande. Comprueba que n anchos cubran exactamente el intervalo."],
                "El símbolo Δx se lee ‘delta equis’ y representa el ancho de cada rectángulo.",
                f"Δx = (b − a) / n = ({b} − {a}) / {n} = {num(w)}")


def lesson():
    basic, _ = plot(2, power=1)
    detailed, _ = plot(12)
    frames = []
    for n in range(1, 41):
        svg, total = plot(n)
        frames.append(dict(label=f"{n} rectángulo{'s' if n!=1 else ''}", svg=svg,
            alt=f"Curva x al cuadrado entre cero y dos, con {n} rectángulos de extremos derechos. Suma {num(total)} y área exacta ocho tercios.",
            description=f"Con {n} partes, cada ancho es {num(2/n)}. En esta función creciente, los extremos derechos sobreestiman el área. La diferencia con 8/3 es {num(total-8/3)}.",
            metrics=[dict(label="Suma aproximada (u²)", value=num(total)), dict(label="Área exacta (u²)", value="8/3 ≈ 2,6667")]))
    constant = dict(title="Un área que ya conoces", prompt="f(x) = 3 en [0, 4]. Usamos 2 rectángulos iguales. ¿Cuál es la suma?", steps=[
        width_step(0, 4, 2),
        step("La altura no cambia", "Si f(x) = 3, ¿cuánto mide la altura de cada rectángulo?", ["2", "3", "4"], 1,
             ["2 es el ancho, que ya calculamos.", "Exacto: una función constante vale 3 en todos los puntos.", "4 es el extremo del intervalo; la altura la da f(x)."],
             "Para obtener una altura evaluamos la función. Como siempre devuelve 3, ambos rectángulos tienen altura 3.", "f(0) = f(2) = f(4) = 3"),
        step("Sumamos áreas pequeñas", "Cada rectángulo tiene base 2 y altura 3. Hay dos. ¿Área total?", ["6", "8", "12"], 2,
             ["6 corresponde a un solo rectángulo; faltan los dos.", "Multiplica base por altura antes de sumar los rectángulos.", "Sí: 6 + 6 = 12."],
             "Cada área es 2 × 3 = 6. Al sumar dos áreas de 6 obtenemos 12 unidades cuadradas. Aquí la suma es exacta porque la función es constante.", "S = 3 × 2 + 3 × 2 = 12 u²")])
    linear = dict(title="Una altura que va cambiando", prompt="f(x) = x en [0, 2]. Tomamos 2 rectángulos y sus extremos derechos.", steps=[
        width_step(0, 2, 2),
        step("Elegimos dónde medir", "Los intervalos son [0, 1] y [1, 2]. ¿Qué extremos derechos usamos?", ["0 y 1", "1 y 2", "0,5 y 1,5"], 1,
             ["Son los extremos izquierdos. Busca el final de cada intervalo.", "Sí: tomamos el final de cada intervalo.", "Esos son los puntos medios; aquí pedimos los derechos."],
             "El extremo derecho de [0, 1] es 1 y el de [1, 2] es 2. Como f(x) = x, esas también son las alturas.", "x₁ = 1; x₂ = 2 → f(1) = 1; f(2) = 2"),
        step("Altura por ancho, y sumamos", "Las alturas son 1 y 2, y el ancho es 1. ¿Cuál es la suma?", ["3", "2", "4"], 0,
             ["Correcto: (1 + 2) × 1 = 3.", "2 es el área exacta bajo esta recta; la suma pedida usa rectángulos derechos.", "No todas las alturas valen 2; usa una altura por intervalo."],
             "Sumamos las áreas, no solo contamos rectángulos. La suma derecha da 3 u²; el área exacta del triángulo bajo la recta es 2 u². Aquí aproximación y área exacta son distintas.", "S = 1 × 1 + 2 × 1 = 3 u²; área exacta = (2 × 2)/2 = 2 u²")])
    speed = dict(title="Del movimiento a la distancia", prompt="Una persona camina con velocidad v(t) = t + 1 m/s entre 0 y 4 s. Usamos 2 intervalos y puntos medios.", steps=[
        width_step(0, 4, 2),
        step("Miramos en mitad de cada tramo", "Los intervalos son [0, 2] y [2, 4]. ¿Qué velocidades hay en sus puntos medios?", ["1 y 3 m/s", "3 y 5 m/s", "2 y 4 m/s"], 2,
             ["1 y 3 son los tiempos medios; falta sumar 1 para obtener la velocidad.", "Son velocidades en los extremos derechos, t = 2 y t = 4.", "Sí: en t = 1, v = 2; en t = 3, v = 4."],
             "Cada tiempo medio está en mitad de su intervalo. Evaluamos v(1) = 2 y v(3) = 4. El ancho aquí representa 2 segundos.", "t* = 1 s y 3 s → v(1) = 2 m/s; v(3) = 4 m/s"),
        step("Velocidad × tiempo", "Cada intervalo dura 2 s. Con velocidades 2 y 4 m/s, ¿qué distancia obtenemos?", ["6 m", "12 m", "8 m"], 1,
             ["6 es la suma de velocidades; falta multiplicar por los 2 segundos.", "Bien: 2 × 2 + 4 × 2 = 12 metros.", "Has usado solo una de las dos velocidades para ambos intervalos."],
             "Multiplicamos cada velocidad por su duración y sumamos. Las unidades (m/s) × s dan metros. La regla del punto medio es exacta en este ejemplo porque v(t) es lineal.", "Distancia = 2 × 2 + 4 × 2 = 4 + 8 = 12 m")])
    exercises = []

    def add(title, concept, prompt, options, correct, feedback, steps):
        exercises.append(dict(id=f"e{len(exercises)+1}", title=title, concept=concept, prompt=prompt,
                               options=options, correct=correct, feedback=feedback, steps=steps))

    add("El tamaño de cada parte", "Ancho de partición", "Divides [0, 6] en 3 intervalos de igual ancho. ¿Cuánto vale Δx?",
        ["3", "2", "6", "1"], 1,
        ["3 es la cantidad de partes, no su ancho.", "Sí: la longitud 6 se reparte en 3 partes de ancho 2.", "6 es el ancho total; falta dividir entre 3.", "Tres intervalos de ancho 1 solo cubrirían una longitud de 3."],
        [width_step(0, 6, 3), step("Comprobamos la partición", "Si cada parte mide 2, ¿dónde quedan los cortes?", ["0, 1, 2, 3", "0, 2, 4, 6", "0, 3, 6"], 1,
         ["Esos cortes solo llegan hasta 3.", "Sí: tres intervalos cubren [0, 6].", "Esos cortes producen dos intervalos, no tres."],
         "Los tres intervalos son [0, 2], [2, 4] y [4, 6]. Cada uno mide 2; juntos miden 6. La respuesta al ejercicio es Δx = 2.", "Δx = 6 / 3 = 2; comprobación: 3 × 2 = 6")])

    add("Una función constante", "Suma de áreas", "f(x) = 5 en [0, 4]. Usas 4 rectángulos y extremos izquierdos. ¿Cuánto vale la suma?",
        ["5", "16", "20", "25"], 2,
        ["5 es una sola altura. Necesitas sumar las cuatro áreas.", "La altura vale 5, no 4. Distingue altura e intervalo.", "Correcto: cuatro áreas de 5 × 1 suman 20 u².", "La base total mide 4, no 5."],
        [width_step(0, 4, 4), step("Una altura repetida", "Cuatro rectángulos tienen base 1 y altura 5. ¿Qué operación corresponde?", ["4 × 5 × 1", "5 + 1", "4 × 4"], 0,
         ["Exacto: número de rectángulos por área de cada uno.", "El área usa multiplicación; después sumas todas las áreas.", "4 no es la altura de la función."],
         "Al ser constante, f vale 5 en todos los extremos izquierdos. La suma es 5 + 5 + 5 + 5 = 20, igual al área exacta.", "S = 4 × (5 × 1) = 20 u²")])

    add("Tomar el extremo derecho", "Extremos derechos", "Para f(x) = x en [0, 3], con n = 3 y extremos derechos, ¿cuál es la suma?",
        ["3", "9", "4,5", "6"], 3,
        ["3 sería la suma con extremos izquierdos 0, 1 y 2.", "Has dado altura 3 a todos los rectángulos; sus alturas cambian.", "4,5 es el área exacta del triángulo, no esta aproximación derecha.", "Sí: (1 + 2 + 3) × 1 = 6."],
        [width_step(0, 3, 3), step("Las alturas derechas", "¿Qué alturas corresponden a los extremos derechos?", ["0, 1, 2", "1, 2, 3", "0,5; 1,5; 2,5"], 1,
         ["Esos son los extremos izquierdos.", "Sí: evalúas f en 1, 2 y 3.", "Son los puntos medios."],
         "Los tres anchos valen 1. En f(x) = x, las alturas derechas son 1, 2 y 3. Multiplicamos cada una por su ancho y sumamos.", "S = 1 × 1 + 2 × 1 + 3 × 1 = 6 u²")])

    add("Ahora, el extremo izquierdo", "Extremos izquierdos", "Para f(x) = x en [0, 3], con n = 3 y extremos izquierdos, ¿cuál es la suma?",
        ["3", "6", "9", "0"], 0,
        ["Sí: (0 + 1 + 2) × 1 = 3.", "6 corresponde a extremos derechos; aquí se usan los izquierdos.", "No todos los rectángulos tienen altura 3.", "Solo el primer rectángulo tiene altura cero."],
        [width_step(0, 3, 3), step("El comienzo de cada tramo", "Para [0, 1], [1, 2] y [2, 3], ¿qué extremos izquierdos usamos?", ["1, 2, 3", "0, 1, 3", "0, 1, 2"], 2,
         ["Son los extremos derechos.", "El último intervalo empieza en 2, no en 3.", "Sí: cada altura se mide al principio de su intervalo."],
         "Las alturas son f(0) = 0, f(1) = 1 y f(2) = 2. El primer rectángulo aporta cero, pero los otros aportan 1 y 2.", "S = 0 × 1 + 1 × 1 + 2 × 1 = 3 u²")])

    add("Una curva al cuadrado", "Evaluar la función", "f(x) = x² en [0, 2], con n = 2 y extremos derechos. ¿Cuál es la suma?",
        ["2,5", "5", "4", "8"], 1,
        ["2,5 corresponde a puntos medios en este ejemplo.", "Sí: f(1) = 1 y f(2) = 4, y cada ancho vale 1.", "4 es solo la altura del último rectángulo.", "Has usado la altura máxima en todo el intervalo."],
        [width_step(0, 2, 2), step("Evaluar significa sustituir", "Los extremos derechos son 1 y 2. ¿Cuánto valen f(1) y f(2)?", ["1 y 2", "2 y 4", "1 y 4"], 2,
         ["La función es x²: eleva al cuadrado cada punto.", "1² es 1; no se multiplica siempre por 2.", "Correcto: 1² = 1 y 2² = 4."],
         "Sustituimos cada extremo en la función. Las alturas son 1 y 4, y el ancho es 1. La suma derecha es 5 u², una aproximación del área.", "S = f(1) × 1 + f(2) × 1 = 1 + 4 = 5 u²")])

    add("Probar puntos medios", "Puntos medios", "Para f(x) = x² en [0, 2], con n = 2, usa los puntos medios. ¿Cuánto vale la suma?",
        ["5", "2", "2,5", "1"], 2,
        ["5 corresponde a extremos derechos, no a puntos medios.", "Suma de puntos medios no es lo mismo que suma de sus cuadrados.", "Sí: 0,5² + 1,5² = 0,25 + 2,25 = 2,5.", "Falta evaluar y sumar la altura de cada rectángulo."],
        [step("Encontramos el centro", "¿Cuáles son los puntos medios de [0, 1] y [1, 2]?", ["0 y 1", "0,5 y 1,5", "1 y 2"], 1,
         ["Son los extremos izquierdos.", "Sí: promedias los extremos de cada intervalo.", "Son los extremos derechos."],
         "El centro de [0, 1] es (0 + 1)/2 = 0,5. El de [1, 2] es (1 + 2)/2 = 1,5. Cada ancho es 1.", "x*₁ = 0,5; x*₂ = 1,5; Δx = 1"),
         step("Cuadrados y áreas", "¿Cuánto vale 0,5² + 1,5²?", ["2,5", "2", "4"], 0,
         ["Bien: 0,25 + 2,25 = 2,5.", "Has sumado los puntos sin elevarlos al cuadrado.", "El cuadrado de una suma no es la suma de cuadrados."],
         "Primero elevamos cada punto al cuadrado, después multiplicamos por el ancho 1 y sumamos. La aproximación por puntos medios es 2,5 u².", "S = 0,25 × 1 + 2,25 × 1 = 2,5 u²")])

    add("¿Por encima o por debajo?", "Interpretar la aproximación", "f(x) = x² es creciente en [0, 2]. Con un número finito de rectángulos de ancho positivo y extremos derechos, la suma…",
        ["Queda por debajo del área exacta", "Siempre es exacta", "No se puede saber para esta función", "Queda por encima del área exacta"], 3,
        ["En una función creciente, la altura derecha es la mayor de cada intervalo.", "Una curva no coincide con estos rectángulos de ancho positivo.", "Sí podemos usar que x² es estrictamente creciente en este intervalo.", "Exacto: cada rectángulo derecho cubre más que el área bajo la curva en su intervalo."],
        [step("Comparamos alturas", "En una función creciente, ¿la altura del extremo derecho es la menor o la mayor del intervalo?", ["La mayor", "La menor", "Siempre es cero"], 0,
         ["Sí: al avanzar a la derecha, la función aumenta.", "Eso corresponde al extremo izquierdo de una función creciente.", "Crecer no implica valer cero."],
         "Para cualquier x dentro del intervalo, f(x) no supera a la altura derecha. Por eso el rectángulo queda por encima de la curva.", "Si x está entre aᵢ y bᵢ: f(x) ≤ f(bᵢ)"),
         step("De cada parte al total", "Si cada rectángulo aporta un exceso de área, ¿qué ocurre al sumar?", ["Los excesos se vuelven negativos", "Se obtiene siempre el área exacta", "La suma total sobreestima"], 2,
         ["Todos los excesos tienen el mismo signo positivo.", "Los excesos positivos no se cancelan.", "Sí: sumar excesos conserva el exceso total."],
         "La suma derecha queda por encima del área exacta de x² en [0, 2]. Esta conclusión usa que la función crece en ese intervalo; no es una regla para cualquier función.", "S_derecha > ∫₀² x² dx = 8/3, para n finito positivo")])

    add("Una caminata por tramos", "Unidades y aplicación", "v(t) = t + 2 m/s para 0 ≤ t ≤ 4 s. Aproxima la distancia con n = 2 y extremos derechos. ¿Qué obtienes?",
        ["20 m", "10 m", "16 m", "8 m"], 0,
        ["Sí: las velocidades derechas son 4 y 6 m/s, y cada tramo dura 2 s.", "10 suma las velocidades; falta multiplicar por 2 s.", "16 m es la distancia exacta para esta velocidad lineal; se pide suma derecha.", "Has usado solo una parte de la información."],
        [step("Tiempo y velocidad", "Los extremos derechos son t = 2 s y t = 4 s. ¿Qué velocidades usamos?", ["2 y 4 m/s", "4 y 6 m/s", "3 y 5 m/s"], 1,
         ["Esos son los tiempos; falta sumar 2 al evaluar v(t).", "Sí: v(2) = 4 y v(4) = 6.", "Son las velocidades en los puntos medios."],
         "La duración de cada intervalo es (4 − 0)/2 = 2 s. Evaluamos la velocidad al final de cada tramo.", "Δt = 2 s; v(2) = 4 m/s; v(4) = 6 m/s"),
         step("Recuperamos metros", "¿Qué operación suma las dos distancias aproximadas?", ["4 + 6", "(4 + 6) / 2", "4 × 2 + 6 × 2"], 2,
         ["Eso suma velocidades, no distancias.", "Eso promedia velocidades; aún falta la duración total.", "Sí: velocidad por duración en cada intervalo."],
         "Cada área representa metros: (m/s) × s. Sumamos 8 + 12 = 20 metros. Como la velocidad aumenta y usamos extremos derechos, esta aproximación supera la distancia exacta.", "Distancia aproximada = 4 × 2 + 6 × 2 = 20 m")])

    add("Cada vez más rectángulos", "Convergencia", "Para la función continua f(x) = x² en [0, 2], aumentas n sin límite en una partición uniforme. ¿A qué se acerca la suma de Riemann?",
        ["A 0", "A la integral, 8/3", "Siempre a 5", "A 8"], 1,
        ["El ancho baja, pero el número de áreas aumenta; el área total no desaparece.", "Correcto: la suma converge a la integral de x² en [0, 2].", "5 es la aproximación derecha con dos rectángulos; cambia al refinar.", "8 es la aproximación con un solo rectángulo derecho."],
        [step("Qué se hace pequeño", "Cuando n aumenta en [0, 2], ¿qué ocurre con Δx = 2/n?", ["Aumenta sin límite", "Siempre vale 2", "Se acerca a 0"], 2,
         ["n está en el denominador: dividir entre más produce partes menores.", "Solo vale 2 cuando n = 1.", "Sí: los rectángulos se hacen más estrechos."],
         "La función es continua en el intervalo cerrado. Al hacerse pequeña la mayor anchura de los intervalos, las sumas convergen a su integral definida.", "n → ∞ implica Δx = 2/n → 0"),
         step("El valor al que llegamos", "La integral exacta es [x³/3] de 0 a 2. ¿Cuál es su valor?", ["8/3", "4/3", "8"], 0,
         ["Sí: 2³/3 − 0³/3 = 8/3.", "2³ vale 8, no 4.", "Falta dividir entre 3."],
         "La integral da 8/3 u². Las sumas derechas del laboratorio se aproximan a ese valor. La continuidad garantiza aquí que las sumas de particiones cada vez más finas convergen.", "∫₀² x² dx = [x³/3]₀² = 8/3 ≈ 2,6667 u²")])

    add("Cuando la función es negativa", "Área con signo", "f(x) = −2 en [0, 3], con n = 3. ¿Cuánto vale la suma de Riemann con signo?",
        ["6", "0", "−6", "−2"], 2,
        ["6 es el área geométrica. La suma pedida conserva el signo negativo de f.", "No hay partes positivas que cancelen las negativas.", "Sí: tres aportes de −2 × 1 suman −6.", "−2 es una altura; falta sumar los tres aportes."],
        [width_step(0, 3, 3), step("El signo tiene significado", "Con altura −2 y ancho 1, ¿cuál es el aporte de cada rectángulo?", ["2", "−2", "0"], 1,
         ["Eso sería su área geométrica, pero la suma conserva el signo de la función.", "Correcto: −2 × 1 = −2.", "Una altura negativa no significa que el aporte desaparezca."],
         "La suma de Riemann es una acumulación con signo. Aquí la función está bajo el eje: cada aporte es −2. La suma es −6 u²; el área geométrica entre la gráfica y el eje es 6 u².", "S = (−2) × 1 + (−2) × 1 + (−2) × 1 = −6 u²")])

    return dict(id="sumas-riemann-principiante-v1", title="Sumas de Riemann", subtitle="Cómo pequeñas áreas nos ayudan a entender una curva. Descubre la idea, juega con ella y construye confianza a tu ritmo.",
        objective="Al terminar podrás armar una suma de Riemann sencilla y explicar qué aproxima.",
        prerequisites="Solo necesitas multiplicar y sumar. El intervalo [a, b] va desde a hasta b; f(x) nos dice la altura de la gráfica en x.",
        takeaway="Divide el intervalo, elige una altura en cada parte, multiplica altura por ancho y suma los aportes.",
        tutorial=[
            dict(title="Una curva, pequeñas piezas", body="Imagina cubrir la región bajo una curva con rectángulos. Son fáciles de medir. Sus áreas sumadas nos dan una aproximación del área que buscamos.", svg=basic, alt="Recta f(x) = x entre cero y dos y dos rectángulos de extremos derechos: alturas uno y dos, ambos de ancho uno."),
            dict(title="Cada pieza tiene su área", body="Dividimos [a, b] en n partes iguales. Cada ancho se llama Δx. Elegimos un punto x* dentro de cada parte; f(x*) será la altura. Multiplicamos cada altura por el ancho y sumamos. El símbolo ∑ significa ‘sumar todos esos aportes’.", formula="Δx = (b − a) / n\nS = ∑ f(x*ᵢ) × Δx", svg=area_diagram(), alt="Rectángulo cuya área es base por altura. La base está etiquetada delta x."),
            dict(title="Más detalle, mejor aproximación", body="Para una función continua, al hacer cada vez más estrechas todas las partes, la suma se acerca a la integral definida. En estos dibujos f es positiva: la integral coincide con el área. Si f es negativa, los aportes conservan ese signo.", svg=detailed, alt="Curva f(x) = x² entre cero y dos aproximada con doce rectángulos derechos, más estrechos que en el primer ejemplo.")],
        simulation=dict(title="¿Y si usamos más rectángulos?", intro="Explora f(x) = x² en [0, 2]. La línea verde es la curva y las piezas claras son rectángulos con extremos derechos. La unidad horizontal y la vertical son unidades de longitud (u); el área se expresa en u².", controlLabel="Número de rectángulos", question="Al aumentar n, ¿se acercan las áreas aproximadas a 8/3? Observa también cómo se reduce el exceso de los rectángulos.", frames=frames),
        applications=[dict(title="¿Cuánto caminaste?", body="Si tu velocidad cambia, divide el tiempo en tramos. Velocidad (m/s) × duración (s) aproxima la distancia de cada tramo. Si caminas siempre hacia adelante, sumar esos metros aproxima la distancia total."),
                      dict(title="¿Cuánta agua entró?", body="Un caudal variable en litros por minuto puede medirse cada cierto tiempo. Caudal × minutos aproxima los litros de cada tramo; al sumarlos obtienes el volumen que entró.")],
        training=[constant, linear, speed], exercises=exercises)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    target = Path(args.output_dir)
    target.mkdir(parents=True, exist_ok=True)
    path = target / "sumas-de-riemann.json"
    path.write_text(json.dumps(lesson(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(path.resolve())


if __name__ == "__main__":
    main()
