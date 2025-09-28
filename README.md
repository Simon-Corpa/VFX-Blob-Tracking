# Blob Tracking VFX con las librerias Pillow y OpenCV (No TouchDesigner)
VFX Blob Tracking busca encontrar una alternativa al flujo de trabajo en TouchDesigner para crear este tipo de efecto visual. Mediante las librerias Pillow y OpenCV generamos distintas funciones de testeo y procesamiento de vídeo para la detección de cambios en el tiempo de los bordes previamente detectados mediante Canny edges. Obtenida la muestra de regiones con cambios entre fotogramas aprovechamos para filtrar una muestra aleatoria que representamos visualmente mediante cuadrados de distintos tamaños y bloques de texto.

El método cuenta con parametros para ajustar las variables de detección de bordes, frecuencia de puntos y distancia entre puntos; además de inputs para un tratamiento estético más versatil (colores, grosores de linea y aleatoriedad de tamaño de los cuadrados representados). Permite además incorporar tipografias para la representación del texto y agregar vídeos máscara para filtrar las regiones en las que se detectan puntos con el fin expreso de conseguir el efecto que se muestra en el vídeo.

Cabe decir que lo común es usar esta clase de efectos en vídeos estáticos (ejp. con tripode) donde el movimiento es muy puntual:

[Muestra de @sssynthomo del efecto con input de una toma estática de baile contemporaneo](https://youtube.com/shorts/PoDn1tz1Cec?si=2_q3ozgYkUUwM9JN)



https://github.com/user-attachments/assets/bd4d4aa2-eec5-4e25-aa02-2413bacd170d

Vídeo con buena definición: [¡aquí!](https://www.youtube.com/watch?v=BJIZrktP8bw)

## Librerias

| Pillow | OpenCV |
|--------|--------|
| <img width="657" height="750" alt="image" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgJLHUtLfgZY6l0RHOzi7MwbQoOWispKbakObCSuYSpeLACyHRUujwMZPhyphenhyphenC_jdemzhVBxfUo4WdrN4vh5LejeFy2gCFaKkp9LoGHXrg4YYBfcaeaIg23bw0kmhtLT91rLuHe-ANgl5hD8/s1600/pillow.png"/> | <img width="500" height="700" alt="image" src="https://github.com/user-attachments/assets/e8aa3727-dbcc-498b-9001-0128ad41509a" />


## Resumen de funciones

### 1. `compute_canny_difference(frame1, frame2, low_threshold=50, high_threshold=150)`
- Convierte dos frames a escala de grises.
- Calcula los bordes con **Canny** en cada frame.
- Devuelve la **diferencia absoluta** entre ambos bordes.
- 👉 Útil para detectar cambios o movimientos entre dos imágenes consecutivas.

#### Detección de bordes Canny Edges
<img width="566" height="391" alt="image" src="https://github.com/user-attachments/assets/f5dc4dc6-af4b-421e-b917-d7a694c79350" />
---

### 2. `apply_blur_and_threshold(image, blur_ksize=5, thresh_value=127)`
- Aplica un **desenfoque gaussiano** a la imagen.
- Después hace un **umbral binario** (threshold).
- 👉 Sirve para limpiar ruido y resaltar zonas relevantes (blanco/negro).
<img width="945" height="317" alt="image" src="https://github.com/user-attachments/assets/b64d98ca-7f9b-4832-87df-4d0494e23bb4" />

---

### 3. `process_white_pixels(image, d=5, alpha=None)`
- Busca **píxeles blancos** en la imagen binaria.
- Opcionalmente usa una **máscara `alpha`** para excluir ciertos puntos.
- Por cada punto blanco detectado:
  - Lo guarda en una lista.
  - Borra (pinta negro) un círculo de radio `d` alrededor de él.
- 👉 Devuelve la lista de puntos blancos procesados.

---

### 4. `visualize_points_with_text(image, points, csv_path, text_params)`
- Crea una **capa transparente (RGBA)** para dibujar encima.
- Lee datos de un **CSV**.
- Por cada punto:
  - Dibuja un cuadrado en la posición.
  - Elige aleatoriamente texto de una fila del CSV.
  - Renderiza el texto encima del punto.
- Permite configurar:
  - Lista de fuentes, tamaños y colores.
  - Espaciado entre caracteres y líneas.
  - Conexión entre puntos mediante líneas.
  - Factor de eliminación (`deletion_factor`) para reducir el número de puntos.

---

### 5. `process_video(video_path, output_folder, csv_path, interpret_params, text_params, alpha_vid_path=None)`
- Procesa un **video cuadro a cuadro**.
- Para cada frame:
  - Calcula diferencias de bordes entre frames consecutivos.
  - Aplica blur + threshold.
  - Detecta puntos blancos y los filtra con `alpha` (si se da).
  - Dibuja overlay de texto encima de esos puntos.
  - Guarda el resultado como imágenes (`.png`) en `output_folder`.
- 👉 Útil para hacer animaciones o visualizaciones basadas en movimiento en video.

---

### 6. `process_images(img1_path, img2_path, csv_path, ...)`
- Similar a `process_video` pero con **dos imágenes estáticas**.
- Pasos:
  - Calcula diferencia de bordes entre `img1` y `img2`.
  - Aplica blur + threshold.
  - Extrae y procesa puntos blancos.
  - Dibuja overlay con texto.
  - Combina la imagen original con el overlay (blending).
  - Muestra el resultado en una ventana (`cv2.imshow`).
- 👉 Útil para pruebas rápidas sin usar video.



## Extrapolación de metodologías de TouchDesigner
Este método es una adaptación a Python de los distintos tutoriales que restringen su uso exclusivamente a TouchDesigner.

Tras intentar realizar el proyecto en Tooll3 (ahora TiXL, alternativa libre a TouchDesigner) y fracasar, elegí buscar otras alternativas con mis conocimientos de Python.

Si bien TouchDesigner ha sido y es un excelente catalizador para el mixed media y los exploradores audiovisuales resulta frustrante que un efecto bastante escueto quede como medalla de un software privativo que basa su metodología en, para suerte de todos, herramientas que se han mantenido con condiciones de uso sin restricciones para toda la comunidad.

Acepto propuestas, comentarios y críticas al código para consolidarlo progresivamente. Esto es una muestra borrador que ha sido funcional para el trabajo que exigió su creación:

[Sumergidos en Atlántico (Minidocumental)](https://www.youtube.com/embed/JyahuAla-Dk?si=SIVYNeVOu13_ogk6)

Agradecemos a los desarrolladores de TouchDesigner su existencia, ahorramos para una licencia de 300$ (actualizaciones por separado), confiamos en la progresiva convergencia de TiXL con su consecuente donación merecida ¡y seguimos buscando alternativas para mantenerlo creativo!

