"""
Екран налаштувань
"""

import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES
from game.game_state import GameState
from ..components.button import Button
from ..components.panel import Panel
from ..components.progress_bar import ProgressBar
from ..components.text import Text


class SettingsScreen:
    """
    Екран налаштувань гри
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        # Налаштування
        self.game_speed = self.game_state.game_speed  # Читаємо з game_state
        self.fullscreen = False
        self.show_tutorials = True
        self.auto_save = True
        
        self._create_ui()
    
    def _create_ui(self):
        """Створення UI"""
        center_x = SCREEN_WIDTH // 2
        
        # Головна панель
        panel_width = 600
        panel_height = 550
        self.main_panel = Panel(
            center_x - panel_width // 2,
            SCREEN_HEIGHT // 2 - panel_height // 2,
            panel_width,
            panel_height,
            header="⚙️ Налаштування",
            header_color=COLORS["secondary"]
        )
        
        content_rect = self.main_panel.get_content_rect()
        
        # ===== Гра =====
        y = content_rect.y + 20
        self.game_label = Text(
            content_rect.x + 20, y,
            "Гра",
            font_size=FONT_SIZES["large"],
            bold=True
        )
        
        # Швидкість гри
        y += 35
        self.speed_label = Text(
            content_rect.x + 40, y,
            f"Швидкість: x{self.game_speed:.1f}",
            font_size=FONT_SIZES["normal"]
        )
        
        self.btn_speed_1x = Button(
            content_rect.x + 250, y - 5,
            60, 35, "x1",
            lambda: self._set_speed(1.0),
            color=COLORS["secondary"]
        )
        
        self.btn_speed_2x = Button(
            content_rect.x + 320, y - 5,
            60, 35, "x2",
            lambda: self._set_speed(2.0),
            color=COLORS["secondary"]
        )
        
        self.btn_speed_3x = Button(
            content_rect.x + 390, y - 5,
            60, 35, "x3",
            lambda: self._set_speed(3.0),
            color=COLORS["secondary"]
        )
        
        self.speed_buttons = [self.btn_speed_1x, self.btn_speed_2x, self.btn_speed_3x]
        self._update_speed_buttons()
        
        # ===== Параметри =====
        y += 60
        self.options_label = Text(
            content_rect.x + 20, y,
            "Параметри",
            font_size=FONT_SIZES["large"],
            bold=True
        )
        
        # Автозбереження
        y += 40
        self.btn_autosave = Button(
            content_rect.x + 40, y,
            panel_width - 100, 40,
            f"Автозбереження: {'Увімкнено' if self.auto_save else 'Вимкнено'}",
            self._toggle_autosave,
            color=COLORS["success"] if self.auto_save else COLORS["gray"]
        )
        
        # Підказки
        y += 50
        self.btn_tutorials = Button(
            content_rect.x + 40, y,
            panel_width - 100, 40,
            f"Підказки: {'Увімкнено' if self.show_tutorials else 'Вимкнено'}",
            self._toggle_tutorials,
            color=COLORS["info"] if self.show_tutorials else COLORS["gray"]
        )
        
        # ===== Кнопки внизу =====
        y = content_rect.y + panel_height - 150
        
        # Кнопка назад
        self.btn_back = Button(
            content_rect.x + 20,
            y,
            panel_width - 60,
            50,
            "← Повернутися",
            self._on_back,
            color=COLORS["primary"],
            font_size=FONT_SIZES["large"]
        )
        
        # Кнопка скидання
        y += 60
        self.btn_reset = Button(
            content_rect.x + 20,
            y,
            panel_width - 60,
            40,
            "Скинути налаштування",
            self._on_reset,
            color=COLORS["danger"]
        )
    
    def _set_speed(self, speed: float):
        self.game_speed = speed
        self.game_state.game_speed = speed
        self.speed_label.set_text(f"Швидкість: x{self.game_speed:.1f}")
        self._update_speed_buttons()
    
    def _update_speed_buttons(self):
        speeds = {1.0: self.btn_speed_1x, 2.0: self.btn_speed_2x, 3.0: self.btn_speed_3x}
        for speed, btn in speeds.items():
            if speed == self.game_speed:
                btn.color = COLORS["primary"]
                btn.border_width = 2
                btn.border_color = COLORS["white"]
            else:
                btn.color = COLORS["secondary"]
                btn.border_width = 0
    
    def _toggle_autosave(self):
        self.auto_save = not self.auto_save
        self.btn_autosave.text = f"Автозбереження: {'Увімкнено' if self.auto_save else 'Вимкнено'}"
        self.btn_autosave.color = COLORS["success"] if self.auto_save else COLORS["gray"]
    
    def _toggle_tutorials(self):
        self.show_tutorials = not self.show_tutorials
        self.btn_tutorials.text = f"Підказки: {'Увімкнено' if self.show_tutorials else 'Вимкнено'}"
        self.btn_tutorials.color = COLORS["info"] if self.show_tutorials else COLORS["gray"]
    
    def _on_back(self):
        # Якщо є хоча б якісь дані про ферму, вважаємо що ми в грі
        if len(self.game_state.animals) > 0 or self.game_state.farmer.money != 10000:
            self.game_engine.change_screen("game")
        else:
            self.game_engine.change_screen("main_menu")
    
    def _on_reset(self):
        self.game_speed = 1.0
        self.auto_save = True
        self.show_tutorials = True
        
        self._set_speed(1.0)
        self._toggle_autosave()
        self._toggle_autosave()
        self._toggle_tutorials()
        self._toggle_tutorials()
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        # Кнопки швидкості
        for btn in self.speed_buttons:
            btn.handle_event(event)
        
        # Перемикачі
        self.btn_autosave.handle_event(event)
        self.btn_tutorials.handle_event(event)
        
        # Кнопки дій
        self.btn_back.handle_event(event)
        self.btn_reset.handle_event(event)
        
        # ESC - назад
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._on_back()
    
    def update(self, dt: float):
        """Оновлення"""
        # Кнопки швидкості за допомогою speed_buttons
        for btn in self.speed_buttons:
            btn.update(dt)
        
        self.btn_autosave.update(dt)
        self.btn_tutorials.update(dt)
        self.btn_back.update(dt)
        self.btn_reset.update(dt)
        
        self.btn_reset.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        surface.fill(COLORS["background"])
        
        # Декоративний візерунок
        self._draw_background_pattern(surface)
        
        # Панель
        self.main_panel.draw(surface)
        
        # Секції
        self.game_label.draw(surface)
        self.speed_label.draw(surface)
        for btn in self.speed_buttons:
            btn.draw(surface)
        
        self.options_label.draw(surface)
        self.btn_autosave.draw(surface)
        self.btn_tutorials.draw(surface)
        
        self.btn_back.draw(surface)
        self.btn_reset.draw(surface)
    
    def _draw_background_pattern(self, surface: pygame.Surface):
        """Декоративний візерунок"""
        pattern_color = tuple(max(0, c - 10) for c in COLORS["background"])
        
        for y in range(0, SCREEN_HEIGHT, 50):
            for x in range(0, SCREEN_WIDTH, 50):
                offset = 25 if (y // 50) % 2 == 0 else 0
                pygame.draw.circle(surface, pattern_color, (x + offset, y), 4)
