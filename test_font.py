import pygame

# Inicializar pygame
pygame.init()

# Crear una ventana
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test de Fuente")

# Cargar la fuente directamente
font = pygame.font.Font("assets/fnt/PressStart2P.ttf", 32)  # Usa la ruta relativa correcta

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fondo negro

    text_surface = font.render("Hola Mundo", True, (255, 255, 255))  # Texto blanco
    screen.blit(text_surface, (50, 200))

    pygame.display.flip()

pygame.quit()
