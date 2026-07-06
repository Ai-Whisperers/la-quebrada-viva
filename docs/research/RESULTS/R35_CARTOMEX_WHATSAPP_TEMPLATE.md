# Cartomex WhatsApp Template — LQV LiDAR Survey Quote Request

> **For Wesley van de Camp.** Pre-written message in Spanish for Wes to copy-paste to Cartomex's WhatsApp.
> Cartomex is the main drone LiDAR provider in Paraguay. They quote on WhatsApp — public quote flow.

---

## Cartomex contact

- **WhatsApp**: +55 11 770-9888 (Brazil area code — their Brazil office also covers PY; verify or ask for the PY contact when they reply)
- **Email**: info@cartomex.com
- **Website**: https://www.cartomex.com/lidar-paraguay.html
- **Response time**: "less than 1 business hour" per their site

---

## WhatsApp message to send (Spanish)

```
Hola! Soy Wesley van de Camp, tengo una finca de 62 hectáreas en
Escobar, Paraguarí, Paraguay. Estoy desarrollando un parque de
alojamiento eco-turístico (5 cabañas + restaurante + piscina en Fase 1,
escalando a 30 cabañas).

Necesito cotización para levantamiento LiDAR con dron de:

- 62 ha totales
- Cobertura de la quebrada interior (vegetación densa, necesito
  penetración del dosel)
- 5 sitios específicos de construcción (cabañas, restaurante, piscina)
- Modelo Digital del Terreno (MDT) con curvas de nivel
- Nube de puntos clasificada (.LAS)
- Precisión vertical: 5-15 cm es suficiente

¿Pueden volar la propiedad? ¿Cuál sería el costo total y los plazos
de entrega?

Mi contacto:
- WhatsApp: +XX XXX XXX XXX (Wes's number)
- Email: wes@theriverstonevalley.com (or current email)

Quedo atento a su respuesta.

Gracias,
Wesley van de Camp
```

---

## Follow-up questions to ask once they reply with a quote

1. **¿Cuándo pueden venir?** (saber si podemos agendar para antes de Q4 2026)
2. **¿Necesitan permisos especiales?** (DINAC, INAA, due owner permission)
3. **¿Entregan en formato .LAS + .DWG + ortofoto?** (verificar entregables)
4. **¿Cuántos puntos por m²?** (recomendado: 100+ pts/m² para nuestro uso)
5. **¿Tienen referencias en Paraguay?** (pedir 2-3 clientes previos similares)
6. **¿El precio incluye el procesamiento?** (algunos cobran captura + procesamiento por separado)
7. **¿Tienen equipo LiDAR multirretorno para penetrar vegetación?** (esencial para la quebrada)
8. **¿Cuál es el costo si necesito un segundo vuelo después?** (en caso de errores)
9. **¿Pueden agregar batimetría de la quebrada?** (mapa del fondo del arroyo)
10. **¿Tiempo de entrega desde el vuelo hasta el informe final?** (típico 1-3 semanas)

---

## What to do with the response

- **Save the quote** in `docs/research/RESULTS/CARTOMEX_QUOTE_2026-XX-XX.md` with date + price + scope
- **Compare** to the DJI L3 setup cost ($35K capex, see `DRONE_LIDAR_QUICK_REFERENCE.md`)
- **Decision trigger**: if Cartomex quote > $8K, definitely hire. If < $5K, definitely hire. Between $5-8K, depends on side-business appetite.

---

## Red flags to watch for in the response

- Quote that doesn't include processing (separate line item for $1-2K)
- Quote that excludes "ground control points" (could add $500-1K)
- Quote that needs separate fee for re-flights
- Quote that's verbal only (insist on PDF written quote)

---

*Pre-written by Erebus 2026-07-06 for Wes to use. Send via WhatsApp, save the response in the research results folder, commit to git.*
