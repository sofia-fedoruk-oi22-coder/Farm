"""
Прогрес бари
"""

import pygame
from typing import Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, get_font


class ProgressBar:
    """
    Прогрес бар з анімацією
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        value: float = 100.0,
        max_value: float = 100.0,
        color: Tuple[int, int, int] = None,
        bg_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
        border_radius: int = 5,
        show_text: bool = True,
        text_color: Tuple[int, int, int] = None,
        animate: bool = True
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.max_value = max_value
        self.display_value = value
        
        self.color = color or COLORS["primary"]
        self.bg_color = bg_color or COLORS["panel_dark"]
        self.border_color = border_color or COLORS["border"]
        self.text_color = text_color or COLORS["white"]
        self.border_radius = border_radius
        
        self.show_text = show_text
        self.animate = animate
        
        # Шрифт
        self.font = get_font(min(height - 4, 12))
    
    def set_value(self, value: float):
        """Встановити значення"""
        self.value = max(0, min(self.max_value, value))
    
    def update(self, dt: float):
        """Оновлення анімації"""
        if self.animate:
            diff = self.value - self.display_value
            if abs(diff) > 0.1:
                self.display_value += diff * dt * 5
            else:
                self.display_value = self.value
        else:
            self.display_value = self.value
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)
        
        # Заповнення
        fill_width = int((self.display_value / self.max_value) * (self.rect.width - 4))
        if fill_width > 0:
            fill_rect = pygame.Rect(
                self.rect.x + 2,
                self.rect.y + 2,
                fill_width,
                self.rect.height - 4
            )
            pygame.draw.rect(surface, self.color, fill_rect, 
                           border_radius=max(1, self.border_radius - 2))
            
            # Світлий градієнт зверху
            highlight_rect = pygame.Rect(
                fill_rect.x,
                fill_rect.y,
                fill_rect.width,
                fill_rect.height // 2
            )
            highlight_surface = pygame.Surface(highlight_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (255, 255, 255, 30),
                           highlight_surface.get_rect(), 
                           border_radius=max(1, self.border_radius - 2))
            surface.blit(highlight_surface, highlight_rect)
        
        # Рамка
        pygame.draw.rect(surface, self.border_color, self.rect, 
                        width=1, border_radius=self.border_radius)
        
        # Текст
        if self.show_text:
            percent = int((self.display_value / self.max_value) * 100)
            text = self.font.render(f"{percent}%", True, self.text_color)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
    
    def get_percentage(self) -> float:
        """Отримати відсоток"""
        return (self.value / self.max_value) * 100


class HealthBar(ProgressBar):
    """
    Бар здоров'я з динамічним кольором
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, value: float = 100.0):
        super().__init__(x, y, width, height, value, 100.0, COLORS["success"])
    
    def update(self, dt: float):
        super().update(dt)
        
        # Динамічний колір
        percent = self.value / self.max_value
        if percent > 0.6:
            self.color = COLORS["success"]
        elif percent > 0.3:
            self.color = COLORS["warning"]
        else:
            self.color = COLORS["danger"]


class HungerBar(ProgressBar):
    """
    Бар голоду
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, value: float = 100.0):
        super().__init__(x, y, width, height, value, 100.0, COLORS["warning"])
    
    def update(self, dt: float):
        super().update(dt)
        
        # Динамічний колір
        percent = self.value / self.max_value
        if percent > 0.5:
            self.color = COLORS["success"]
        elif percent > 0.25:
            self.color = COLORS["warning"]
        else:
            self.color = COLORS["danger"]


class HappinessBar(ProgressBar):
    """
    Бар щастя
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, value: float = 100.0):
        super().__init__(x, y, width, height, value, 100.0, COLORS["info"])
    
    def update(self, dt: float):
        super().update(dt)
        
        # Динамічний колір
        percent = self.value / self.max_value
        if percent > 0.6:
            self.color = COLORS["info"]
        elif percent > 0.3:
            self.color = COLORS["warning"]
        else:
            self.color = COLORS["danger"]


class EnergyBar(ProgressBar):
    """
    Бар енергії фермера
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, value: float = 100.0):
        super().__init__(x, y, width, height, value, 100.0, COLORS["secondary"])
    
    def update(self, dt: float):
        super().update(dt)
        
        percent = self.value / self.max_value
        if percent > 0.5:
            self.color = COLORS["secondary"]
        elif percent > 0.25:
            self.color = COLORS["warning"]
        else:
            self.color = COLORS["danger"]
