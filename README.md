# ⚡ Acelerador de Videos con Python y FFmpeg

Este proyecto permite acelerar archivos de video (`.mp4`) usando `FFmpeg`, controlado desde un script Python. Ideal para hacer versiones aceleradas de videos largos sin pérdida de calidad innecesaria.

---

## 🧰 Requisitos

- macOS (Intel o Apple Silicon)
- Python 3.x instalado
- [Homebrew](https://brew.sh/) instalado
- Acceso a terminal (Zsh recomendado)

---

## 📦 Instalación

### 1. Clonar o descargar este proyecto

```bash
git clone https://github.com/patriciodsgn/acelerar_video.git
cd acelerar_video
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install opencv-python tqdm
```

---

## 🎞️ Instalar FFmpeg

Descargar versión precompilada para Mac:

```bash
curl -L -o ffmpeg.zip https://evermeet.cx/ffmpeg/ffmpeg-6.1.zip
unzip ffmpeg.zip
chmod +x ffmpeg
```

📝 Asegurate de tener el archivo `ffmpeg` dentro del mismo directorio del script.

---

## 📂 Estructura de carpetas esperada

```
acelerar_video/
│
├── original/         ← coloca aquí los videos a acelerar
├── acelerados/       ← los archivos resultantes se guardarán aquí
├── ffmpeg            ← binario descargado
├── script.py         ← script principal
├── venv/             ← entorno virtual
└── README.md
```

---

## 🚀 Uso

Con el entorno activado:

```bash
python script.py
```

El script tomará un archivo específico (o lo podés ajustar para modo batch), y generará un video acelerado a 60x por defecto.

---

## ⚙️ Configuración en el script

Dentro de `script.py` podés cambiar:

```python
input_file = os.path.join("original", "VID_20250412_191816.mp4")
output_file = os.path.join("acelerados", "acelerado_191816.mp4")
speed_factor = 60  # o usar target_duration = 20
```

También se muestra el progreso del archivo de salida basado en su tamaño:

```
📦 84.52MB de ~360.30MB (23.46%)
```

---

## ✅ Resultado

Cuando finaliza, se imprime:

```
✅ ¡Listo! Video guardado en: acelerados/acelerado_XXXX.mp4
📦 Tamaño final: 359.82 MB
```

---

## 🧠 Notas

- El script no comprime ni reencoda en exceso, solo ajusta el tiempo (`setpts`) → proceso ligero.
- El avance se basa en el tamaño del archivo generado, lo cual es más realista para este flujo.

---

## 📌 Créditos

Creado por [@patriciodsgn](https://github.com/patriciodsgn) con ♥️ para automatizar edición de video en proyectos creativos.

