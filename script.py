import subprocess
import os
import re
import cv2
import time
import threading

def get_video_frames(input_file):
    try:
        cap = cv2.VideoCapture(input_file)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        cv2.destroyAllWindows()
        return int(frames)
    except:
        return None

def show_file_progress(output_file, estimated_final_size, process):
    """Muestra el crecimiento del archivo en una sola línea mientras FFmpeg trabaja."""
    while process.poll() is None:
        if os.path.exists(output_file):
            current_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            percent = (current_size / estimated_final_size) * 100 if estimated_final_size > 0 else 0
            print(f"\r📦 {current_size:.2f}MB de ~{estimated_final_size:.2f}MB ({percent:.2f}%)", end='')
        time.sleep(1)

def speed_up_video(input_file, output_file, speed_factor=None, target_duration=None):
    ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg')
    if not os.path.isfile(input_file):
        print(f"❌ No se encontró el archivo: {input_file}")
        return

    original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB

    if target_duration:
        total_frames = get_video_frames(input_file)
        if total_frames:
            original_duration = total_frames / 30  # estimamos 30fps
            speed_factor = original_duration / target_duration
            print(f"🎯 Frames estimados: {total_frames}, duración: ~{original_duration:.2f}s")
            print(f"📐 Factor de aceleración: {speed_factor:.2f}")
        else:
            print("⚠️ No se pudo calcular duración.")
            return

    if not speed_factor:
        print("⚠️ No se definió ni speed_factor ni duración.")
        return

    estimated_final_size = original_size / speed_factor
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    speed_filter = f"setpts=1/{speed_factor}*PTS"
    cmd = [
        ffmpeg_path, '-i', input_file,
        '-filter:v', speed_filter,
        '-an',
        '-progress', 'pipe:1',
        '-nostats',
        output_file
    ]

    print(f"\n⚡ Procesando {input_file} → {output_file}")
    print(f"📦 Tamaño estimado: ~{estimated_final_size:.2f} MB\n")

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # 🧵 Ejecutar la función de progreso como un hilo
    watcher_thread = threading.Thread(target=show_file_progress, args=(output_file, estimated_final_size, process))
    watcher_thread.start()

    # Leer output aunque no hagamos nada con él, para evitar bloqueo
    for _ in process.stdout:
        pass

    process.wait()
    watcher_thread.join()  # esperar a que el hilo termine también

    if process.returncode == 0:
        final_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✅ ¡Listo! Video guardado en: {output_file}")
        print(f"📦 Tamaño final: {final_size:.2f} MB")
    else:
        print("\n❌ Error al procesar el video.")

# === 👇 BLOQUE PRINCIPAL
if __name__ == '__main__':
    print("▶️ Ejecutando script...")

    input_file = os.path.join("original", "185142.mp4")
    output_file = os.path.join("acelerados", "185142.mp4")

    speed_factor = None  # Fijo (60x)
    target_duration = 50  # o podés usar target_duration = 20 para fijar duración final

    speed_up_video(
        input_file,
        output_file,
        speed_factor=speed_factor,
        target_duration=target_duration
    )