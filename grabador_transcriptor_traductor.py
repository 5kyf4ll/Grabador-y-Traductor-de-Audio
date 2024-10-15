import tkinter as tk
import wave
import pyaudio
import datetime
import threading
import whisper
import os
from googletrans import Translator

# Cargar el modelo Whisper
modelo_whisper = whisper.load_model("medium")  # Cambia "medium" por el modelo que desees usar

# Clase principal de la interfaz
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Grabador, Transcriptor y Traductor")
        self.is_recording = False
        self.frames = []
        self.archivo_audio = None  # Variable para almacenar el nombre del archivo
        self.translator = Translator()  # Inicializar traductor
        self.texto_transcrito = ""  # Almacena la transcripción

        # Cuadro de texto para la transcripción
        self.cuadro_texto = tk.Text(master, height=10, width=50)
        self.cuadro_texto.pack()

        # Cuadro de texto para la traducción
        self.cuadro_traduccion = tk.Text(master, height=10, width=50)
        self.cuadro_traduccion.pack()

        # Botones de control
        self.boton_grabar = tk.Button(master, text="Iniciar Grabación", command=self.iniciar_grabacion)
        self.boton_grabar.pack()

        self.boton_detener = tk.Button(master, text="Detener Grabación", command=self.detener_grabacion)
        self.boton_detener.pack()

        self.boton_transcribir = tk.Button(master, text="Transcribir", command=self.iniciar_transcripcion)
        self.boton_transcribir.pack()

        self.boton_traducir = tk.Button(master, text="Traducir", command=self.iniciar_traduccion)
        self.boton_traducir.pack()

    def iniciar_grabacion(self):
        self.is_recording = True
        self.frames = []
        self.cuadro_texto.delete(1.0, tk.END)
        # Iniciar un hilo para la grabación de audio
        self.grabacion_thread = threading.Thread(target=self.grabar_audio)
        self.grabacion_thread.start()

    def grabar_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("Grabando...")

        while self.is_recording:
            data = stream.read(CHUNK)
            self.frames.append(data)

        print("Grabación finalizada.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Guardar archivo
        self.guardar_audio()

    def detener_grabacion(self):
        self.is_recording = False
        # Esperar a que el hilo de grabación termine
        self.grabacion_thread.join()

    def guardar_audio(self):
        # Generar nombre de archivo
        fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.archivo_audio = f"grabacion_{fecha_hora}.wav"  # Guardar el nombre del archivo

        with wave.open(self.archivo_audio, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        print(f"Archivo guardado como: {self.archivo_audio} en la ruta: {os.path.abspath(self.archivo_audio)}")

    def iniciar_transcripcion(self):
        # Iniciar un hilo para la transcripción de audio
        self.transcripcion_thread = threading.Thread(target=self.transcribir_audio)
        self.transcripcion_thread.start()

    def transcribir_audio(self):
        if self.archivo_audio:  # Verificar si hay un archivo guardado
            try:
                # Llama a la función de Whisper para la transcripción
                resultado = modelo_whisper.transcribe(self.archivo_audio)
                self.texto_transcrito = resultado['text'].strip()  # Obtén el texto de la transcripción

                # Guardar el texto en un archivo de texto
                with open(f"{self.archivo_audio.replace('.wav', '')}_transcripcion.txt", 'w', encoding='utf-8') as f:
                    f.write(self.texto_transcrito)

                self.master.after(0, lambda: self.cuadro_texto.insert(tk.END, self.texto_transcrito + "\n"))
                print("Transcripción guardada.")
            except Exception as e:
                error_message = f"Error en la transcripción: {e}"
                self.master.after(0, lambda: self.cuadro_texto.insert(tk.END, error_message + "\n"))
        else:
            self.master.after(0, lambda: self.cuadro_texto.insert(tk.END, "No hay grabación para transcribir.\n"))

    def iniciar_traduccion(self):
        """Iniciar un hilo para traducir el texto transcrito."""
        self.traduccion_thread = threading.Thread(target=self.traducir_texto)
        self.traduccion_thread.start()

    def traducir_texto(self):
        """Traduce el texto transcrito del inglés al español."""
        if self.texto_transcrito:
            try:
                print("Traduciendo...")
                traduccion = self.translator.translate(self.texto_transcrito, dest='es')  # Cambia 'es' a otro idioma si es necesario
                texto_traducido = traduccion.text

                # Mostrar la traducción en el cuadro correspondiente
                self.master.after(0, lambda: self.cuadro_traduccion.delete(1.0, tk.END) or self.cuadro_traduccion.insert(tk.END, texto_traducido + "\n"))
                print("Traducción completada.")
            except Exception as e:
                error_message = f"Error en la traducción: {e}"
                self.master.after(0, lambda: self.cuadro_traduccion.insert(tk.END, error_message + "\n"))
        else:
            self.master.after(0, lambda: self.cuadro_traduccion.insert(tk.END, "No hay texto para traducir.\n"))

# Ejecutar la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
