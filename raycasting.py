import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # --- HORIZONTAL ---
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # --- VERTICAL ---
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # --- FISHBOWL EFFECT (sem correção angular) ---
            depth = min(depth_vert, depth_hor)

            # PROPOSITALMENTE NÃO CORRIGIDO:
            # depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            # --- Preto e branco fixo ---
            color = (255, 255, 255)

            pg.draw.rect(
                self.game.screen, color,
                (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
            )

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
