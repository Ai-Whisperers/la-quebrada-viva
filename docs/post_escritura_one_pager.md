# La Quebrada Viva — Post-Escritura One-Pager

> Cliente: Wesley van de Camp (75%) + Thijs van de Camp (25%) · Escritura traslativa firmada **2026-06-27** · Hoja resumen al T+1 (**2026-06-28**), preparada por AI Whisperers a partir de la KML compartida por Wesley y los datos abiertos ya en el repo. Cifras técnicas trazables a `docs/post_escritura_site_knowledge.md`.

---

## El predio en cuatro números

| Indicador | Valor | Qué significa |
|---|---|---|
| **Núcleo edificable** | **30.9 ha** | Polígono dibujado por Wesley en Google Earth — el "cluster norte de Mbopicua", contiguo, subconjunto de las 62.57 ha legales. |
| **Suelo plano (<8 % de pendiente)** | **4.28 ha · 13.8 %** | Suficiente para 4 cabañas Fase 1 sin terraceo, con margen para mover. La banda media (8–15 %, 12.76 ha) absorbe escalamiento a ~12 cabañas con muros bajos de piedra. |
| **Orientación dominante** | **71.6 % S/SW** | Caras frescas, vista hacia el valle — favorece habitaciones con amanecer, miradores, terrazas. Coincide con la regla LQV de aleros 90 cm + enfriamiento pasivo ≤35 °C. |
| **Cobertura forestal** | **NDVI 0.917 · dosel GEDI 27.7 m** | Atlántica madura pared a pared. Sentinel-2 no detecta claros, no detecta agua estancada. Activo central del proyecto. |

**Contexto envolvente**: 62.57 ha totales en 6 fincas (Mbopicua + Ybyraty). El polígono cubre **3 de las 6** (hipótesis padrón A o B, ambas 30.35 ha, ver §2 del knowledge doc). Las ~32 ha restantes (finca 697 Mbopicua + finca 298 Ybyraty) quedan como reserva forestal / activo paisajístico sin programa edificable inmediato.

---

## Lo que sabemos sin pisar el terreno

- **Relieve**: 73.5 m de desnivel (157.9 → 231.5 m). Quebrada clásica — terreno de trabajo, no precipicio.
- **Pin de Wesley** ("escobar wes", 166.3 m AMSL): sentado cerca del extremo bajo del polígono → muy probable referencia de **arroyo / quebrada de acceso**, no sitio de construcción ni cresta.
- **Clima ERA5 (1990–2025)**: 22 °C media anual, **1,736 mm/año**, Cfa húmedo subtropical. Lluvia abundante, sin estación seca pronunciada.
- **Hidrología visible**: NDWI < 0 en todo el polígono → cero espejos de agua superficial dentro de la línea de Wesley. La presencia de la quebrada se infiere por topografía, no se confirma en imagen.

---

## Lo que NO sabemos hasta que lleguen las fotos

Pendiente de Wesley: **"the client will share some images soon of the place in person"**. La carpeta `docs/site_data/client_photos/2026-06_post_escritura/` ya tiene la lista de 14 tomas pedidas (intake checklist activo). Las preguntas que solo las fotos pueden cerrar:

1. **¿Dónde corre la quebrada exactamente?** El DEM 30 m la oculta; un par de fotos del cauce la fijan al metro.
2. **Estado real del camino interno** desde la ruta hasta el pin de Wesley.
3. **Construcciones existentes** (si las hay) — el satélite no las muestra, pero un caserío chico podría no aparecer.
4. **Especies dominantes del dosel** — la NDVI confirma cobertura, no composición. Lapacho, peterebí, yvyrá-pytá tienen tratamientos de diseño distintos.
5. **Acceso a la piscina natural / salto** mencionado por Wesley en conversaciones previas — posición + caída + estado.

---

## Próximos 30 días (sin Fase 1 todavía)

| # | Acción | Quién | Cuándo |
|---|---|---|---|
| 1 | Wesley sube fotos según la lista de 14 tomas | W | Apenas pueda |
| 2 | AI Whisperers cruza fotos contra el knowledge doc y actualiza R01 + §6 si algo invalida una afirmación | I | T+2 a partir de fotos |
| 3 | Anexo I del boleto (linderos de cada finca) → cierra hipótesis padrón A/B | Escribana Peña Ros | Esperado en mano |
| 4 | Municipalidad de Escobar — uso de suelo para hospedaje + restaurante + eventos | Abogado local | 1–2 semanas |
| 5 | Re-evaluación dron LiDAR ($1,500, 1 m DEM) — vuela el polígono + 60 m buffer, no las 62 ha completas | W | T+30, con fotos en mano |

Lo que **no** estamos haciendo todavía y por qué: ningún proveedor contactado, ninguna propuesta a Awasi ni a hoteles de San Bernardino, ningún arquitecto convocado, ningún dron volado. Los borradores existen localmente en el repo (no enviados) — la firma está fresca; primero confirmamos terreno con fotos, después salimos al mercado.

---

## Para los socios — lectura rápida

**Wesley**: Tu polígono cuadra. 30.9 ha de cluster norte de Mbopicua, todo edificable en gradiente, dosel intacto. Tu pin de elevación 166 m lee como referencia de quebrada, no de casa — confirmá si era eso. Tus fotos cierran lo que falta.

**Thijs**: Land is closed, polygon checks out, forest cover is wall-to-wall mature Atlantic, ~4 ha of flat ground anchors Phase 1 (4 cabins with headroom). Spend in the next 30 days is research, not construction. Bigger numbers will follow once client photos and Anexo I are in hand.

---

*Anclajes técnicos: `docs/post_escritura_site_knowledge.md` (paquete completo, 8 secciones), `docs/site_data/extended_aoi/polygon_quicklook.png` (vista del polígono sobre COP30 + hillshade), `docs/site_data/extended_aoi/polygon_ndvi_quicklook.png` (NDVI clipped), `docs/site_data/escobar_property_polygon.geojson` (la línea de Wesley en GeoJSON), `docs/RESEARCH_GAPS.md` R01.*
