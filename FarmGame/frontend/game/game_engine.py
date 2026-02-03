"""
Головний ігровий движок
Відповідає за ініціалізацію та керування грою
"""

import pygame
import sys
import os
from typing import Optional, Dict, Any

# Додаємо шлях до модулів
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState
from game.constants import *


class GameEngine:
    """
    Головний клас ігрового движка
    Керує станами гри, екранами та основним циклом
    """
    
    def __init__(self):
        """Ініціалізація движка гри"""
        # Ініціалізація Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Налаштування екрану
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🌾 Ферма - Курсова робота з ООП")
        
        # Годинник для контролю FPS
        self.clock = pygame.time.Clock()
        
        # Ігровий стан
        self.game_state = GameState()
        
        # Поточний екран
        self.current_screen_name: Optional[str] = None
        self.current_screen = None
        self.screens: Dict[str, Any] = {}
        
        # Стан гри
        self.running = True
        self.paused = False
        
        # Шрифт для паузи
        self.pause_font = get_font(72, bold=True)
        self.pause_hint_font = get_font(24)
        
        # Ліниве завантаження
        self._screens_initialized = False
    
    def _lazy_init_screens(self):
        """Ліниве завантаження екранів"""
        if self._screens_initialized:
            return
        
        from ui.screens.main_menu import MainMenu
        from ui.screens.game_screen import GameScreen
        from ui.screens.shop_screen import ShopScreen
        from ui.screens.inventory_screen import InventoryScreen
        from ui.screens.settings_screen import SettingsScreen
        from ui.screens.new_game_screen import NewGameScreen
        from ui.screens.animal_details_screen import AnimalDetailsScreen
        
        self.screens = {
            "main_menu": MainMenu(self),
            "game": GameScreen(self),
            "shop": ShopScreen(self),
            "inventory": InventoryScreen(self),
            "settings": SettingsScreen(self),
            "new_game": NewGameScreen(self),
            "animal_details": AnimalDetailsScreen(self)
        }
        
        self._screens_initialized = True
    
    def change_screen(self, screen_name: str):
        """Перемикання на інший екран"""
        self._lazy_init_screens()
        
        if screen_name in self.screens:
            self.current_screen_name = screen_name
            self.current_screen = self.screens[screen_name]
    
    def toggle_pause(self):
        """Перемкнути паузу"""
        self.paused = not self.paused
    
    def run(self):
        """Головний ігровий цикл"""
        self._lazy_init_screens()
        self.change_screen("main_menu")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self._handle_events()
            
            if not self.paused and self.current_screen:
                self.current_screen.update(dt)
            
            self._render()
        
        self._cleanup()
    
    def _handle_events(self):
        """Обробка вхідних подій"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if self.current_screen:
                self.current_screen.handle_event(event)
    
    def _render(self):
        """Рендеринг гри"""
        self.screen.fill(COLORS["background"])
        
        if self.current_screen:
            self.current_screen.draw(self.screen)
        
        if self.paused:
            self._render_pause_overlay()
        
        pygame.display.flip()
    
    def _render_pause_overlay(self):
        """Рендеринг оверлею паузи"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        text = self.pause_font.render("⏸️ ПАУЗА", True, COLORS["white"])
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)
        
        hint = self.pause_hint_font.render("Натисніть ESC для продовження", True, COLORS["gray"])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(hint, hint_rect)
    
    def _cleanup(self):
        """Завершення роботи гри"""
        if self.current_screen_name == "game":
            self.game_state.save_game()
        
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()
    
    def new_game(self, farm_name: str, farmer_name: str):
        """Створення нової гри"""
        self.game_state.new_game(farm_name, farmer_name)
        self.change_screen("game")
    
    def load_game(self):
        """Завантаження збереженої гри"""
        if self.game_state.load_game():
            self.change_screen("game")
            return True
        return False
    
    def quit_game(self):
        """Вихід з гри"""
        self.running = False
