"""
Головне меню гри
"""

import pygame
import math
import random
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES, 
    GAME_TITLE, GAME_SUBTITLE, VERSION, get_font, get_emoji_font
)
from game.game_state import GameState
from ..components.button import Button
from ..components.text import Text, AnimatedText
from ..components.panel import Panel


class MainMenu:
    """
    Головне меню з анімаціями та ефектами
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        # Шрифти
        self.title_font = get_font(FONT_SIZES["huge"], bold=True)
        self.subtitle_font = get_font(FONT_SIZES["large"])
        self.version_font = get_font(FONT_SIZES["small"])
        self.emoji_font = get_emoji_font(FONT_SIZES["huge"])
        
        # Анімаційні параметри
        self.time = 0.0
        self.particles = []
        self.clouds = []
        self._init_particles()
        self._init_clouds()
        
        # Тварини-декорації
        self.decorative_animals = []
        self._init_decorative_animals()
        
        # UI елементи
        self._create_ui()
    
    def _init_particles(self):
        """Ініціалізація часток (пилок, листя)"""
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(2, 5),
                'speed': random.uniform(20, 50),
                'angle': random.uniform(0, math.pi * 2),
                'color': random.choice([
                    COLORS["accent"],
                    (255, 200, 100),
                    (200, 255, 150)
                ])
            })
    
    def _init_clouds(self):
        """Ініціалізація хмар"""
        for i in range(5):
            self.clouds.append({
                'x': random.randint(-200, SCREEN_WIDTH),
                'y': random.randint(20, 150),
                'width': random.randint(100, 200),
                'speed': random.uniform(10, 30),
                'alpha': random.randint(100, 180)
            })
    
    def _init_decorative_animals(self):
        """Ініціалізація декоративних тварин"""
        animals = ['🐄', '🐔', '🐷', '🐑', '🐐', '🦆', '🐰', '🐴']
        for i, emoji in enumerate(animals):
            self.decorative_animals.append({
                'emoji': emoji,
                'x': 50 + (i % 4) * 320,
                'y': SCREEN_HEIGHT - 100 + (i // 4) * 40,
                'offset': random.uniform(0, math.pi * 2),
                'speed': random.uniform(0.5, 1.5)
            })
    
    def _create_ui(self):
        """Створення UI елементів"""
        center_x = SCREEN_WIDTH // 2
        button_width = 280
        button_height = 55
        button_spacing = 70
        start_y = SCREEN_HEIGHT // 2 - 20
        
        # Кнопки
        self.buttons = []
        
        # Нова гра
        self.btn_new_game = Button(
            center_x - button_width // 2,
            start_y,
            button_width,
            button_height,
            "Нова гра",
            self._on_new_game,
            color=COLORS["primary"],
            font_size=FONT_SIZES["large"]
        )
        self.buttons.append(self.btn_new_game)
        
        # Продовжити (якщо є збереження)
        if self.game_state.has_save_file():
            self.btn_continue = Button(
                center_x - button_width // 2,
                start_y + button_spacing,
                button_width,
                button_height,
                "Продовжити",
                self._on_continue,
                color=COLORS["success"],
                font_size=FONT_SIZES["large"]
            )
            self.buttons.append(self.btn_continue)
            offset = button_spacing
        else:
            self.btn_continue = None
            offset = 0
        
        # Налаштування
        self.btn_settings = Button(
            center_x - button_width // 2,
            start_y + button_spacing + offset,
            button_width,
            button_height,
            "Налаштування",
            self._on_settings,
            color=COLORS["secondary"],
            font_size=FONT_SIZES["large"]
        )
        self.buttons.append(self.btn_settings)
        
        # Вихід
        self.btn_exit = Button(
            center_x - button_width // 2,
            start_y + button_spacing * 2 + offset,
            button_width,
            button_height,
            "Вихід",
            self._on_exit,
            color=COLORS["danger"],
            font_size=FONT_SIZES["large"]
        )
        self.buttons.append(self.btn_exit)
        
        # Текст заголовка
        self.title_text = AnimatedText(
            center_x,
            100,
            GAME_TITLE,
            color=COLORS["primary"],
            font_size=FONT_SIZES["huge"],
            bold=True,
            shadow=True,
            align='center',
            animation='bounce',
            animation_speed=1.5
        )
        
        # Підзаголовок
        self.subtitle_text = AnimatedText(
            center_x,
            180,
            GAME_SUBTITLE,
            color=COLORS["text_secondary"],
            font_size=FONT_SIZES["large"],
            align='center',
            animation='fade'
        )
        self.subtitle_text.fade_in(2.0)
    
    def _on_new_game(self):
        """Обробник кнопки Нова гра"""
        self.game_engine.change_screen("new_game")
    
    def _on_continue(self):
        """Обробник кнопки Продовжити"""
        if self.game_state.load_game():
            self.game_engine.change_screen("game")
    
    def _on_settings(self):
        """Обробник кнопки Налаштування"""
        self.game_engine.change_screen("settings")
    
    def _on_exit(self):
        """Обробник кнопки Вихід"""
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        for button in self.buttons:
            button.handle_event(event)
    
    def update(self, dt: float):
        """Оновлення"""
        self.time += dt
        
        # Оновлення кнопок
        for button in self.buttons:
            button.update(dt)
        
        # Оновлення тексту
        self.title_text.update(dt)
        self.subtitle_text.update(dt)
        
        # Оновлення часток
        for particle in self.particles:
            particle['x'] += math.cos(particle['angle']) * particle['speed'] * dt
            particle['y'] += math.sin(particle['angle']) * particle['speed'] * dt
            
            # Повернення на екран
            if particle['x'] < -10:
                particle['x'] = SCREEN_WIDTH + 10
            elif particle['x'] > SCREEN_WIDTH + 10:
                particle['x'] = -10
            if particle['y'] < -10:
                particle['y'] = SCREEN_HEIGHT + 10
            elif particle['y'] > SCREEN_HEIGHT + 10:
                particle['y'] = -10
        
        # Оновлення хмар
        for cloud in self.clouds:
            cloud['x'] += cloud['speed'] * dt
            if cloud['x'] > SCREEN_WIDTH + 100:
                cloud['x'] = -cloud['width'] - 50
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Градієнтний фон (небо)
        self._draw_gradient_background(surface)
        
        # Хмари
        self._draw_clouds(surface)
        
        # Земля
        self._draw_ground(surface)
        
        # Декоративні тварини
        self._draw_decorative_animals(surface)
        
        # Частки
        self._draw_particles(surface)
        
        # Заголовок
        self.title_text.draw(surface)
        self.subtitle_text.draw(surface)
        
        # Кнопки
        for button in self.buttons:
            button.draw(surface)
        
        # Версія
        version_text = self.version_font.render(f"v{VERSION}", True, COLORS["text_secondary"])
        surface.blit(version_text, (SCREEN_WIDTH - version_text.get_width() - 10, SCREEN_HEIGHT - 25))
        
        # Копірайт
        copyright_text = self.version_font.render("© 2026 Курсова робота ООП", True, COLORS["text_secondary"])
        surface.blit(copyright_text, (10, SCREEN_HEIGHT - 25))
    
    def _draw_gradient_background(self, surface: pygame.Surface):
        """Градієнтний фон"""
        # Колір неба згори донизу
        top_color = (135, 206, 235)  # Блакитний
        mid_color = (200, 230, 255)  # Світло-блакитний
        
        for y in range(SCREEN_HEIGHT // 2):
            ratio = y / (SCREEN_HEIGHT // 2)
            color = tuple(
                int(top_color[i] + (mid_color[i] - top_color[i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Заповнюємо нижню частину
        pygame.draw.rect(
            surface,
            mid_color,
            (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        )
    
    def _draw_clouds(self, surface: pygame.Surface):
        """Відмальовка хмар"""
        for cloud in self.clouds:
            # Створюємо поверхню хмари
            cloud_surface = pygame.Surface((cloud['width'], 60), pygame.SRCALPHA)
            
            # Малюємо кілька кіл для хмари
            circles = [
                (cloud['width'] // 4, 30, 25),
                (cloud['width'] // 2, 25, 30),
                (cloud['width'] * 3 // 4, 30, 25),
                (cloud['width'] // 3, 35, 20),
                (cloud['width'] * 2 // 3, 35, 20),
            ]
            
            for cx, cy, radius in circles:
                pygame.draw.circle(
                    cloud_surface,
                    (255, 255, 255, cloud['alpha']),
                    (cx, cy),
                    radius
                )
            
            surface.blit(cloud_surface, (int(cloud['x']), cloud['y']))
    
    def _draw_ground(self, surface: pygame.Surface):
        """Відмальовка землі"""
        ground_y = SCREEN_HEIGHT - 150
        
        # Трава
        grass_color = (76, 153, 0)
        pygame.draw.rect(
            surface,
            grass_color,
            (0, ground_y, SCREEN_WIDTH, 150)
        )
        
        # Темніша лінія для текстури
        for i in range(5):
            y = ground_y + i * 30
            color = (60 + i * 5, 130 + i * 5, 0)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y), 2)
        
        # Паркан
        fence_y = ground_y - 40
        fence_color = (139, 90, 43)
        
        # Горизонтальні планки
        pygame.draw.rect(surface, fence_color, (0, fence_y + 10, SCREEN_WIDTH, 8))
        pygame.draw.rect(surface, fence_color, (0, fence_y + 30, SCREEN_WIDTH, 8))
        
        # Вертикальні планки
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.rect(surface, fence_color, (x, fence_y, 10, 50))
    
    def _draw_decorative_animals(self, surface: pygame.Surface):
        """Відмальовка декоративних тварин"""
        font = get_emoji_font(48)
        
        for animal in self.decorative_animals:
            # Анімація підстрибування
            offset_y = math.sin(self.time * animal['speed'] + animal['offset']) * 5
            
            emoji_surface = font.render(animal['emoji'], True, COLORS["text"])
            x = animal['x']
            y = animal['y'] + offset_y
            
            surface.blit(emoji_surface, (x, y))
    
    def _draw_particles(self, surface: pygame.Surface):
        """Відмальовка часток"""
        for particle in self.particles:
            alpha = int(150 + math.sin(self.time * 2) * 50)
            color = (*particle['color'], alpha)
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                color,
                (particle['size'], particle['size']),
                particle['size']
            )
            
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
