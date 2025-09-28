# Blob Tracking VFX con las librerias Pillow y OpenCV (No TouchDesigner)
VFX Blob Tracking busca encontrar una alternativa al flujo de trabajo en TouchDesigner para crear este tipo de efecto visual. Mediante las librerias Pillow y OpenCV generamos distintas funciones de testeo y procesamiento de vídeo para la detección de cambios en el tiempo de los bordes previamente detectados mediante Canny edges. Obtenida la muestra de regiones con cambios entre fotogramas aprovechamos para filtrar una muestra aleatoria que representamos visualmente mediante cuadrados de distintos tamaños y bloques de texto.

El método cuenta con parametros para ajustar las variables de detección de bordes, frecuencia de puntos y distancia entre puntos; además de inputs para un tratamiento estético más versatil (colores, grosores de linea y aleatoriedad de tamaño de los cuadrados representados). Permite además incorporar tipografias para la representación del texto y agregar vídeos máscara para filtrar las regiones en las que se detectan puntos con el fin expreso de conseguir el efecto que se muestra en el vídeo.

Cabe decir que lo común es usar esta clase de efectos en vídeos estáticos (ejp. con tripode) donde el movimiento es muy puntual:
[Muestra de @sssynthomo del efecto con input de una toma estática de baile contemporaneo](https://youtube.com/shorts/PoDn1tz1Cec?si=2_q3ozgYkUUwM9JN)

## Detección de bordes Canny Edges
<img width="566" height="391" alt="image" src="https://github.com/user-attachments/assets/f5dc4dc6-af4b-421e-b917-d7a694c79350" />

Punto de partida para el método usado para simplificar los movimientos dentro de la escena.

## Extrapolación de metodologías de TouchDesigner
Este método es una adaptación a Python de los distintos tutoriales que restringen su uso exclusivamente a TouchDesigner.

Tras intentar realizar el proyecto en Tooll3 (ahora TiXL, alternativa libre a TouchDesigner) y fracasar, elegí buscar otras alternativas con mis conocimientos de Python.

Si bien TouchDesigner ha sido y es un excelente catalizador para el mixed media y los exploradores audiovisuales resulta frustrante que un efecto bastante escueto quede como medalla de un software privativo que basa su metodología en, para suerte de todos, herramientas que se han mantenido con condiciones de uso sin restricciones para toda la comunidad.

Acepto propuestas, comentarios y críticas al código para consolidarlo progresivamente. Esto es una muestra borrador que ha sido funcional para el trabajo que exigió su creación:

[Sumergidos en Atlántico (Minidocumental)](https://www.youtube.com/embed/JyahuAla-Dk?si=SIVYNeVOu13_ogk6)

Agradecemos a los desarrolladores de TouchDesigner su existencia, ahorramos para una licencia de 300$ (actualizaciones por separado), confiamos en la progresiva convergencia de TiXL con su consecuente donación merecida ¡y seguimos buscando alternativas para mantenerlo creativo!
