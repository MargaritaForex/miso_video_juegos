🚀 Space Shooter - Instrucciones de Instalación y Ejecución
🛠️ Instalación Local
Clonar el repositorio

bash
Copy
Edit
git clone [[URL del repositorio]](https://github.com/MargaritaForex/miso_video_juegos)
cd [miso_video_juegos]
Crear un entorno virtual en Python

bash
Copy
Edit
python -m venv .venv
Activar el entorno virtual

En Windows:

bash
Copy
Edit
.venv\Scripts\activate
(En MacOS/Linux sería source .venv/bin/activate, pero tu instrucción es para Windows)

Instalar las dependencias

bash
Copy
Edit
pip install -r requirements.txt
🖥️ Generar Ejecutable (Versión de Escritorio - Windows)
Para compilar el juego en un archivo .exe listo para distribución:

bash
Copy
Edit
pyinstaller --onefile --windowed --clean --exclude-module numpy --exclude-module mkl main.py
Esto generará:

Un ejecutable en la carpeta dist/

Puedes empaquetar el .exe en un .zip para subirlo a itch.io o distribuirlo.

🌐 Exportar para Web (Versión Navegador)
Para convertir tu juego en una versión web jugable directamente en el navegador usando pygbag:

bash
Copy
Edit
python -m pygbag .
Esto creará una carpeta build/web/ lista para publicar en plataformas como Itch.io, GitHub Pages, etc.

🎮 Controles del Juego
Mover nave: Flechas del teclado

Disparo normal: Clic izquierdo del mouse

Poder especial: Presionar tecla E (requiere recarga de 15 segundos)

Pausar / Reanudar: Tecla P

🛡️ Requisitos
Python 3.10 o superior

Pygame instalado (se instala automáticamente con requirements.txt)

👩‍💻 Créditos
Desarrollado como parte del curso MISO-VideoJuegos - Universidad de los Andes.

