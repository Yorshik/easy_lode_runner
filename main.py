import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.surface.Surface([20, 20])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]


class Platform(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.surface.Surface([50, 10])
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Stairs(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.surface.Surface([10, 50])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':
    LEFTBUTTON = 1
    RIGHTBUTTON = 3
    screen = pygame.display.set_mode([500, 500])
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    stairs = pygame.sprite.Group()
    game = True
    clock = pygame.time.Clock()
    FPS = 60
    player = None
    ctrl_pressed = False
    collided_with_stairs = False
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == RIGHTBUTTON:
                    if player:
                        player.set_position(event.pos)
                    else:
                        player = Player(all_sprites, x=event.pos[0], y=event.pos[1])
                elif event.button == LEFTBUTTON:
                    if ctrl_pressed:
                        Stairs(all_sprites, stairs, x=event.pos[0], y=event.pos[1])
                    else:
                        Platform(all_sprites, platforms, x=event.pos[0], y=event.pos[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player:
                        player.rect.x -= 10
                elif event.key == pygame.K_RIGHT:
                    if player:
                        player.rect.x += 10
                elif event.key == pygame.K_UP:
                    if player and collided_with_stairs:
                        player.rect.y -= 10
                elif event.key == pygame.K_DOWN:
                    if player and collided_with_stairs:
                        player.rect.y += 10
        if player:
            if pygame.sprite.spritecollide(player, stairs, False):
                collided_with_stairs = True
            elif lst := pygame.sprite.spritecollide(player, platforms, False):
                player.rect.y = lst[0].rect.y - 19
            else:
                player.rect.y += 50 / 60
                collided_with_stairs = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            ctrl_pressed = True
        else:
            ctrl_pressed = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    all_sprites.draw(screen)
    pygame.quit()
