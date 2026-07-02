# Español — AI tells y variantes regionales

Companion to `writing-rules.md` for books written in Spanish. The five tell families,
structure rules, and compression discipline in writing-rules.md apply unchanged; this
file replaces the English-specific vocabulary lists and adds what Spanish uniquely
needs: regional-variant discipline. The style profile's whitelist outranks this file,
same as always (≥3 occurrences in the author's corpus = allowed for this author).

---

## 1. Vocabulario vetado (relleno IA)

sumergirse / sumergámonos / adentrarse (metafórico) — desentrañar — tapiz — crisol —
abanico ("un abanico de") — "una amplia gama de" — pivotal / fundamental (como relleno) —
"jugar/desempeñar un papel crucial" — piedra angular — pieza clave (como muletilla) —
fomentar (relleno) — potenciar — empoderar — robusto — sinergia — paradigma —
transformador — revolucionar (relleno) — innovador (relleno) — integral (por "holístico") —
apalancar / aprovechar (calco de "leverage") — navegar (metafórico) — "embarcarse en" —
"un viaje" (metafórico) — vertiginoso — "sin fisuras" — optimizar (fuera de contexto
técnico) — vibrante — clave ("es clave que…" como relleno)

## 2. Muletillas y frases vetadas

- "Cabe destacar / mencionar / señalar que…"
- "Es importante destacar / mencionar / tener en cuenta que…"
- "Vale la pena mencionar…"
- "En el mundo / universo / ámbito de…" · "En la era digital…" · "En el vertiginoso
  mundo actual…" · "Hoy en día…" (como apertura de relleno)
- "Sin lugar a dudas" / "Sin duda alguna" / "No es ningún secreto que…"
- "Como bien sabemos…" / "Como hemos visto…" / "Como mencionamos anteriormente…"
- "A lo largo y ancho de…"
- "Desde X hasta Y" (decorativo, no literal)
- "No solo X, sino también Y" (paralelismo negativo — la firma más delatora del español IA)
- "Tanto X como Y" encadenado
- "Pero eso no es todo…" / "Aquí es donde entra en juego…"
- "¿El resultado?" / "¿La clave?" (falsa cercanía en pregunta-respuesta)
- Preguntas retóricas en cadena
- Cierres: "En resumen…", "En conclusión…", "En definitiva…", "En última instancia…",
  "A modo de cierre…", "Para finalizar…" — y cualquier párrafo que recapitule lo recién dicho

## 3. Hedges (cortarlos, la frase mejora)

básicamente — esencialmente — generalmente — típicamente — usualmente — posiblemente —
potencialmente — podría decirse — en cierto modo — en cierta medida — hasta cierto
punto — de alguna manera — relativamente (relleno)

## 4. Calcos del inglés — el tell más grave

AI Spanish is often translated English. These read instantly as machine output:

| Calco (vetado) | Español real |
|---|---|
| hacer sentido | tener sentido |
| tomar acción | actuar |
| en orden de / en orden a | para |
| asumir (por "suponer") | suponer, dar por hecho |
| aplicar (a un puesto) | postularse |
| soportar (por "apoyar/admitir") | respaldar, admitir |
| eventualmente (por "finalmente") | tarde o temprano, con el tiempo |
| actualmente (por "en realidad") | en realidad |
| librería (software) | biblioteca |
| al final del día (metafórico) | a fin de cuentas |
| es acerca de ("it's about") | se trata de |
| remover (por "quitar") | quitar, eliminar |

The Editor scans for these explicitly — they survive vocabulary filters because each
word is legitimate Spanish; only the usage is foreign.

## 5. Variantes regionales — regla central

`book.md` fija idioma **y variante** (ej.: `es-AR · vos (voseo rioplatense)`). La
variante es ley al mismo nivel que el fingerprint: **jamás mezclar sistemas de
tratamiento en un mismo libro.** "Vos tienes" y "tú tenés" son errores, no estilo.
El Editor verifica cada verbo en segunda persona contra la variante declarada.

Variantes soportadas: `es-AR` voseo rioplatense (guía completa abajo) · `es-419` tuteo
neutro latinoamericano (tú + ustedes, sin localismos marcados) · `es-ES` peninsular
(tú + vosotros) · trato de `usted` sostenido si el registro del libro lo pide.

## 6. Guía es-AR — voseo rioplatense

El default argentino para no ficción que tutea al lector es **vos**. El error típico de
un modelo es derivar al tuteo neutro o al peninsular; esta sección existe para impedirlo.

**Pronombres.** Sujeto `vos`; objeto `te`; posesivos `tu/tuyo`; con preposición **"con
vos", "para vos"** — nunca "contigo". Plural **siempre `ustedes` + tercera persona
plural**; `vosotros`, `os` y `vuestro` no existen en este libro.

**Presente del indicativo** — la sílaba tónica cae en la terminación:
-ar → **-ás** (hablás, pensás, arrancás) · -er → **-és** (tenés, querés, sabés, podés,
hacés) · -ir → **-ís** (vivís, decís, salís, venís). Irregulares que dejan de serlo:
*tenés, querés, podés* (no "tienes/quieres/puedes"). `ser` → **sos**. `estar` → estás.
`ir` → vas. `haber` → has.

**Imperativo** — infinitivo menos la -r, con tilde: hablá, tené, vení, decí, hacé,
poné, salí, mirá, acordate (con clítico: fijate, ponete). `ir` → **andá**. `ser` → sé.
Negativo en registro escrito: "no hables", "no vengas" (subjuntivo estándar); "no
hablés/vengás" es más coloquial y enfático — usarlo solo si el corpus lo usa.

**Subjuntivo.** En prosa publicada argentina el subjuntivo estándar es la norma: "que
tengas", "cuando quieras". Las formas voseantes ("tengás", "querás") son orales; solo
entran si el fingerprint las trae.

**Léxico.** Preferir `acá/allá` sobre `aquí/allí`; `computadora`, `celular`, `auto`,
`jugo`, `manejar`, `departamento`, `plata` (registro informal). Vetados los
peninsularismos: ordenador, móvil, coche, zumo, vale, guay, "coger" (en AR es vulgar —
usar agarrar/tomar). Lunfardo y marcadores conversacionales (che, laburo, quilombo,
al toque, dale) **solo si el corpus del autor los usa** — el fingerprint decide el
grado de argentinidad léxica; la gramática voseante, en cambio, no se negocia.

**Checklist es-AR del Editor** (además del pre-flight general):
- [ ] Cero formas de tuteo verbal (tienes, puedes, sabes, haz, ven) y cero vosotros
- [ ] Imperativos con tilde correcta (mirá, fijate, acordate)
- [ ] "con vos / para vos" — ningún "contigo"
- [ ] Léxico peninsular ausente; nivel de lunfardo igual al del corpus, no más
- [ ] Calcos del §4 ausentes
- [ ] Los números y ejemplos usan convenciones argentinas si el libro las estableció
      (pesos, coma decimal, "mil millones" — jamás "billones" por *billions*)
