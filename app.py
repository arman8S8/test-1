import pygame
import random
import sys

# مقداردهی اولیه
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 نبرد فضایی - Space Defender")
clock = pygame.time.Clock()

# رنگ‌ها
BG_COLOR = (15, 15, 30)
WHITE = (255, 255, 255)
RED = (230, 57, 70)
CYAN = (69, 123, 157)
YELLOW = (241, 250, 238)

# ویژگی‌های سفینه
player_w, player_h = 50, 40
player_x = WIDTH // 2 - player_w // 2
player_y = HEIGHT - 70
player_speed = 7

# لیست‌ها
lasers = []
laser_speed = 10
enemies = []
enemy_w, enemy_h = 40, 40
enemy_speed = 4

score = 0
font = pygame.font.SysFont("arial", 24)

running = True
game_over = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                lasers.append(pygame.Rect(player_x + player_w // 2 - 3, player_y, 6, 15))
            if event.key == pygame.K_r and game_over:
                game_over = False
                enemies.clear()
                lasers.clear()
                score = 0
                player_x = WIDTH // 2 - player_w // 2

    if not game_over:
        # حرکت با کیبورد
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_w:
            player_x += player_speed

        # حرکت تیرها
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.bottom < 0:
                lasers.remove(laser)

        # ایجاد دشمنان تصادفی
        if random.randint(1, 25) == 1:
            enemies.append(pygame.Rect(random.randint(0, WIDTH - enemy_w), -enemy_h, enemy_w, enemy_h))

        # حرکت دشمنان و برخورد
        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        for enemy in enemies[:]:
            enemy.y += enemy_speed

            # برخورد با تیر
            for laser in lasers[:]:
                if enemy.colliderect(laser):
                    enemies.remove(enemy)
                    lasers.remove(laser)
                    score += 10
                    break

            # برخورد با سفینه یا خروج از صفحه
            if enemy.colliderect(player_rect):
                game_over = True
            elif enemy.top > HEIGHT:
                enemies.remove(enemy)

    # رسم المان‌ها
    screen.fill(BG_COLOR)

    if not game_over:
        # رسم سفینه (مثلثی)
        ship_points = [
            (player_x + player_w // 2, player_y),
            (player_x, player_y + player_h),
            (player_x + player_w, player_y + player_h)
        ]
        pygame.draw.polygon(screen, CYAN, ship_points)

        # رسم تیرها
        for laser in lasers:
            pygame.draw.rect(screen, YELLOW, laser)

        # رسم موانع/دشمنان
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy, border_radius=6)

        # امتیاز
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
    else:
        msg = font.render("GAME OVER! Press R to Restart", True, RED)
        screen.blit(msg, (WIDTH // 2 - 170, HEIGHT // 2 - 20))

    pygame.display.flip()

pygame.quit()
sys.exit()