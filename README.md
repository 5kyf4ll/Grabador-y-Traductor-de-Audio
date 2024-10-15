# Grabador-y-Traductor-de-Audio
Este proyecto es una aplicación de escritorio en Python que permite grabar audio, transcribirlo y traducir el texto transcrito de inglés a español. Utiliza la biblioteca PyAudio para la captura de audio y el modelo Whisper de OpenAI para la transcripción. Además, incorpora la API de googletrans para la traducción automática.

## Requisitos

### Para Windows

1. **Python 3.7 o superior**: [Descargar Python](https://www.python.org/downloads/)

2. **FFmpeg**: Necesario para la manipulación de audio. Puedes descargarlo desde [FFmpeg Download](https://ffmpeg.org/download.html).
   - **Instrucciones de instalación**:
     - Descarga la versión para Windows y extrae los archivos en una carpeta (por ejemplo, `C:\ffmpeg`).
     - Agrega la ruta a la carpeta `bin` de FFmpeg al PATH:
       - Haz clic derecho en "Este PC" o "Mi PC" y selecciona "Propiedades".
       - Haz clic en "Configuración avanzada del sistema" y luego en "Variables de entorno".
       - En "Variables del sistema", busca y selecciona la variable "Path", luego haz clic en "Editar".
       - Haz clic en "Nuevo" y agrega la ruta `C:\ffmpeg\bin`.
       - Haz clic en "Aceptar" para cerrar todas las ventanas.

3. **Librerías necesarias**:
   - `pyaudio`: Para la captura de audio.
   - `whisper`: Modelo de transcripción de OpenAI.
   - `googletrans`: Para la traducción automática.
   - `numpy`: Usado por algunas bibliotecas para operaciones matemáticas.

### Instalación de Requisitos

1. **Crear un entorno virtual (opcional pero recomendado)**:

   ```bash
   # Abre el símbolo del sistema y navega a tu directorio de proyecto
   cd ruta/a/tu/proyecto

   # Crear un entorno virtual
   python -m venv venv

   # Activar el entorno virtual
   venv\Scripts\activate

2. **Instalar las librerias**:

   ```bash
   # Abre el símbolo del sistema y navega a tu directorio de proyecto
   pip install -r requirements.txt

3. **Ejecutar proyecto**:
   ```bash
   # Abre el símbolo del sistema y navega a tu directorio de proyecto
   python grabador_transcriptor_traductor.py
