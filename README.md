# 🚀 Space Shooter - Instrucciones de Instalación y Ejecución

[https://margarita-forex.itch.io/miso-video-juego](https://margarita-forex.itch.io/miso-video-juego-enemies)
## 🛠️ Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone [https://github.com/MargaritaForex/miso_video_juegos]
   cd [miso_video_juegos]
   ```

2. **Crear un entorno virtual en Python**
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual**
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔤️ Generar Ejecutable (Versión de Escritorio - Windows)

Para compilar el juego en un archivo `.exe` listo para distribución:

```bash
pyinstaller --onefile --windowed --clean --exclude-module numpy --exclude-module mkl main.py
```

Esto generará:
- Un ejecutable en la carpeta `dist/`
- Puedes empaquetar el `.exe` en un `.zip` para subirlo a itch.io o distribuirlo.

---

## 🌐 Exportar para Web (Versión Navegador)

Para convertir tu juego en una versión web jugable directamente en el navegador usando **pygbag**:

```bash
python -m pygbag .
```

Esto creará una carpeta `build/web/` lista para publicar en plataformas como **Itch.io**, **GitHub Pages**, etc.

---

## 🎮 Controles del Juego

- **Mover nave**: Flechas del teclado
- **Disparo normal**: Clic izquierdo del mouse
- **Poder especial**: Presionar tecla `E` (requiere recarga de 15 segundos)
- **Pausar / Reanudar**: Tecla `P`

---

## 🛡️ Requisitos

- Python 3.10 o superior
- Pygame instalado (se instala automáticamente con `requirements.txt`)

---

## 👩‍💻 Créditos

Desarrollado como parte del curso **MISO-VideoJuegos** - Universidad de los Andes.
