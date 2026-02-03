"""
Екран створення нової гри
"""

import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES
from game.game_state import GameState
from ..components.button import Button
from ..components.input_field import InputField
from ..components.panel import Panel
from ..components.text import Text


class NewGameScreen:
    """
    Екран налаштування нової гри
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        self._create_ui()
    
    def _create_ui(self):
        """Створення UI"""
        center_x = SCREEN_WIDTH // 2
        
        # Головна панель
        panel_width = 500
        panel_height = 450
        self.main_panel = Panel(
            center_x - panel_width // 2,
            SCREEN_HEIGHT // 2 - panel_height // 2,
            panel_width,
            panel_height,
            header="Нова ферма",
            header_color=COLORS["primary"]
        )
        
        content_rect = self.main_panel.get_content_rect()
        
        # Назва ферми
        self.farm_label = Text(
            content_rect.x + 20,
            content_rect.y + 20,
            "Назва ферми:",
            font_size=FONT_SIZES["normal"],
            bold=True
        )
        
        self.farm_input = InputField(
            content_rect.x + 20,
            content_rect.y + 50,
            panel_width - 60,
            45,
            placeholder="Введіть назву ферми...",
            text="Моя Ферма",
            max_length=30
        )
        
        # Ім'я фермера
        self.farmer_label = Text(
            content_rect.x + 20,
            content_rect.y + 120,
            "Ім'я фермера:",
            font_size=FONT_SIZES["normal"],
            bold=True
        )
        
        self.farmer_input = InputField(
            content_rect.x + 20,
            content_rect.y + 150,
            panel_width - 60,
            45,
            placeholder="Введіть ім'я фермера...",
            text="Фермер",
            max_length=20
        )
        
        # Вибір складності
        self.difficulty_label = Text(
            content_rect.x + 20,
            content_rect.y + 220,
            "Складність:",
            font_size=FONT_SIZES["normal"],
            bold=True
        )
        
        self.difficulty = "normal"
        button_width = (panel_width - 80) // 3
        
        self.btn_easy = Button(
            content_rect.x + 20,
            content_rect.y + 250,
            button_width,
            40,
            "Легка",
            lambda: self._set_difficulty("easy"),
            color=COLORS["success"]
        )
        
        self.btn_normal = Button(
            content_rect.x + 30 + button_width,
            content_rect.y + 250,
            button_width,
            40,
            "Нормальна",
            lambda: self._set_difficulty("normal"),
            color=COLORS["warning"]
        )
        
        self.btn_hard = Button(
            content_rect.x + 40 + button_width * 2,
            content_rect.y + 250,
            button_width,
            40,
            "Складна",
            lambda: self._set_difficulty("hard"),
            color=COLORS["danger"]
        )
        
        self.difficulty_buttons = [self.btn_easy, self.btn_normal, self.btn_hard]
        self._update_difficulty_buttons()
        
        # Кнопки дій
        self.btn_start = Button(
            content_rect.x + 20,
            content_rect.y + panel_height - 140,
            panel_width - 60,
            50,
            "Почати гру",
            self._on_start,
            color=COLORS["primary"],
            font_size=FONT_SIZES["large"]
        )
        
        self.btn_back = Button(
            content_rect.x + 20,
            content_rect.y + panel_height - 80,
            panel_width - 60,
            45,
            "← Назад",
            self._on_back,
            color=COLORS["secondary"]
        )
    
    def _set_difficulty(self, difficulty: str):
        """Встановити складність"""
        self.difficulty = difficulty
        self._update_difficulty_buttons()
    
    def _update_difficulty_buttons(self):
        """Оновити стан кнопок складності"""
        difficulties = {"easy": self.btn_easy, "normal": self.btn_normal, "hard": self.btn_hard}
        
        for diff, btn in difficulties.items():
            if diff == self.difficulty:
                btn.border_width = 3
                btn.border_color = COLORS["white"]
            else:
                btn.border_width = 0
    
    def _on_start(self):
        """Почати нову гру"""
        farm_name = self.farm_input.get_text().strip() or "Моя Ферма"
        farmer_name = self.farmer_input.get_text().strip() or "Фермер"
        
        # Налаштування складності
        if self.difficulty == "easy":
            starting_money = 15000
        elif self.difficulty == "hard":
            starting_money = 5000
        else:
            starting_money = 10000
        
        # Ініціалізація нової гри
        self.game_state.new_game(farm_name, farmer_name)
        self.game_state.farmer.money = starting_money
        
        # Переходимо до гри
        self.game_engine.change_screen("game")
    
    def _on_back(self):
        """Повернутися до меню"""
        self.game_engine.change_screen("main_menu")
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        self.farm_input.handle_event(event)
        self.farmer_input.handle_event(event)
        
        self.btn_start.handle_event(event)
        self.btn_back.handle_event(event)
        
        for btn in self.difficulty_buttons:
            btn.handle_event(event)
        
        # ESC - назад
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._on_back()
    
    def update(self, dt: float):
        """Оновлення"""
        self.farm_input.update(dt)
        self.farmer_input.update(dt)
        
        self.btn_start.update(dt)
        self.btn_back.update(dt)
        
        for btn in self.difficulty_buttons:
            btn.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        surface.fill(COLORS["background"])
        
        # Декоративний візерунок
        self._draw_background_pattern(surface)
        
        # Панель
        self.main_panel.draw(surface)
        
        # Елементи форми
        self.farm_label.draw(surface)
        self.farm_input.draw(surface)
        
        self.farmer_label.draw(surface)
        self.farmer_input.draw(surface)
        
        self.difficulty_label.draw(surface)
        for btn in self.difficulty_buttons:
            btn.draw(surface)
        
        self.btn_start.draw(surface)
        self.btn_back.draw(surface)
    
    def _draw_background_pattern(self, surface: pygame.Surface):
        """Декоративний візерунок на фоні"""
        # Повторюваний патерн
        pattern_color = tuple(c - 10 for c in COLORS["background"])
        
        for y in range(0, SCREEN_HEIGHT, 40):
            for x in range(0, SCREEN_WIDTH, 40):
                offset = 20 if (y // 40) % 2 == 0 else 0
                pygame.draw.circle(surface, pattern_color, (x + offset, y), 3)
