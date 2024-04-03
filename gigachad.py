import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gigachad Chase")

#Mewing music
pygame.mixer.music.load("mewing.mp3")
pygame.mixer.music.play(-1)

# Load gigachad image
gigachad_img = pygame.image.load("gigachad.png")
original_width, original_height = gigachad_img.get_size()
gigachad_img = pygame.transform.scale(gigachad_img, (original_width // 4, original_height // 4))

# List to hold gigachad instances
gigachad_list = [gigachad_img.get_rect()]

# Dictionary to hold collision status of each gigachad
collision_status = {(gigachad.x, gigachad.y): False for gigachad in gigachad_list}

# Font for the count display
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

num_images = 1  # Initial number of images

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move each gigachad towards the mouse
    for gigachad in gigachad_list:
        direction_x = 1 if gigachad.x < mouse_x else -1
        direction_y = 1 if gigachad.y < mouse_y else -1
        gigachad.x += random.randint(1, 3) * direction_x
        gigachad.y += random.randint(1, 3) * direction_y

        # Check if gigachad collides with the mouse
        if any(gigachad.collidepoint(mouse_x, mouse_y) for gigachad in gigachad_list):
            for gigachad in gigachad_list:
                if not collision_status.get((gigachad.x, gigachad.y), False):
                    # Duplicate and scale gigachad
                    new_gigachad = gigachad.copy()
                    new_gigachad.width //= 4
                    new_gigachad.height //= 4
                    
                    # Randomize the position of the duplicated gigachad
                    new_gigachad.x = random.randint(0, SCREEN_WIDTH - new_gigachad.width)
                    new_gigachad.y = random.randint(0, SCREEN_HEIGHT - new_gigachad.height)
                    
                    # Check for overlap with existing gigachads
                    while any(new_gigachad.colliderect(existing) for existing in gigachad_list):
                        new_gigachad.x = random.randint(0, SCREEN_WIDTH - new_gigachad.width)
                        new_gigachad.y = random.randint(0, SCREEN_HEIGHT - new_gigachad.height)
                    
                    gigachad_list.append(new_gigachad)
                    collision_status[(new_gigachad.x, new_gigachad.y)] = False

                    # Update collision status of the original gigachad
                    collision_status[(gigachad.x, gigachad.y)] = True
                    
                    # Increment the number of images
                    num_images *= 2
                    break  # Break out of the loop after duplicating one gigachad

    # Fill the screen with white
    screen.fill(WHITE)
    
    # Render count text
    count_text = font.render(f"Number of images: {num_images}", True, BLACK)
    screen.blit(count_text, (10, 10))

    # Draw gigachad(s)
    for gigachad in gigachad_list:
        screen.blit(gigachad_img, gigachad)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
