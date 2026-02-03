"""
Компонент панелі
"""

import pygame
from typing import Tuple, Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, get_font


class Panel:
    """
    Панель-контейнер для UI елементів
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = None,
        alpha: int = 255,
        border_radius: int = 15,
        border_width: int = 0,
        border_color: Tuple[int, int, int] = None,
        shadow: bool = True,
        header: str = None,
        header_color: Tuple[int, int, int] = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color or COLORS["panel"]
        self.alpha = alpha
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color or COLORS["border"]
        self.shadow = shadow
        self.header = header
        self.header_color = header_color or COLORS["primary"]
        self.header_height = 40 if header else 0
        
        # Дочірні елементи
        self.children = []
        
        # Поверхня для малювання
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._needs_redraw = True
    
    def add_child(self, child):
        """Додати дочірній елемент"""
        self.children.append(child)
    
    def remove_child(self, child):
        """Видалити дочірній елемент"""
        if child in self.children:
            self.children.remove(child)
    
    def clear_children(self):
        """Очистити всі дочірні елементи"""
        self.children.clear()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обробка подій"""
        for child in self.children:
            if hasattr(child, 'handle_event'):
                if child.handle_event(event):
                    return True
        return False
    
    def update(self, dt: float):
        """Оновлення"""
        for child in self.children:
            if hasattr(child, 'update'):
                child.update(dt)
    
    def _redraw_surface(self):
        """Перемалювати внутрішню поверхню"""
        self._surface.fill((0, 0, 0, 0))
        
        # Основний прямокутник
        base_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        
        if self.alpha < 255:
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.rect(self._surface, color_with_alpha, base_rect, 
                           border_radius=self.border_radius)
        else:
            pygame.draw.rect(self._surface, self.color, base_rect, 
                           border_radius=self.border_radius)
        
        # Заголовок
        if self.header:
            header_rect = pygame.Rect(0, 0, self.rect.width, self.header_height)
            pygame.draw.rect(self._surface, self.header_color, header_rect,
                           border_top_left_radius=self.border_radius,
                           border_top_right_radius=self.border_radius)
            
            font = get_font(18, bold=True)
            text = font.render(self.header, True, COLORS["white"])
            text_rect = text.get_rect(center=(self.rect.width // 2, self.header_height // 2))
            self._surface.blit(text, text_rect)
        
        # Рамка
        if self.border_width > 0:
            pygame.draw.rect(self._surface, self.border_color, base_rect,
                           width=self.border_width, border_radius=self.border_radius)
        
        self._needs_redraw = False
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка панелі"""
        if self._needs_redraw:
            self._redraw_surface()
        
        # Тінь
        if self.shadow:
            shadow_rect = self.rect.copy()
            shadow_rect.x += 5
            shadow_rect.y += 5
            shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (0, 0, 0, 50), 
                           shadow_surface.get_rect(), border_radius=self.border_radius)
            surface.blit(shadow_surface, shadow_rect)
        
        # Панель
        surface.blit(self._surface, self.rect)
        
        # Дочірні елементи
        for child in self.children:
            if hasattr(child, 'draw'):
                child.draw(surface)
    
    def get_content_rect(self) -> pygame.Rect:
        """Отримати область для контенту (без заголовка)"""
        return pygame.Rect(
            self.rect.x + 10,
            self.rect.y + self.header_height + 10,
            self.rect.width - 20,
            self.rect.height - self.header_height - 20
        )
    
    def set_position(self, x: int, y: int):
        """Встановити позицію"""
        dx = x - self.rect.x
        dy = y - self.rect.y
        self.rect.x = x
        self.rect.y = y
        
        # Зсуваємо дочірні елементи
        for child in self.children:
            if hasattr(child, 'rect'):
                child.rect.x += dx
                child.rect.y += dy


class AnimatedPanel(Panel):
    """
    Панель з анімаціями появи/зникнення
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Анімація
        self.visible = False
        self.target_alpha = 0
        self.animation_speed = 5.0
        
        # Позиція для анімації
        self.original_y = self.rect.y
        self.animation_offset_y = 20
        
    def show(self):
        """Показати панель"""
        self.visible = True
        self.target_alpha = self.alpha
        self.alpha = 0
    
    def hide(self):
        """Сховати панель"""
        self.visible = False
        self.target_alpha = 0
    
    def toggle(self):
        """Перемкнути видимість"""
        if self.visible:
            self.hide()
        else:
            self.show()
    
    def update(self, dt: float):
        """Оновлення анімації"""
        super().update(dt)
        
        # Анімація прозорості
        if self.alpha < self.target_alpha:
            self.alpha = min(self.target_alpha, self.alpha + int(255 * dt * self.animation_speed))
            self._needs_redraw = True
        elif self.alpha > self.target_alpha:
            self.alpha = max(0, self.alpha - int(255 * dt * self.animation_speed))
            self._needs_redraw = True
        
        # Анімація позиції
        if self.visible:
            target_y = self.original_y
        else:
            target_y = self.original_y + self.animation_offset_y
        
        y_diff = target_y - self.rect.y
        if abs(y_diff) > 1:
            self.rect.y += int(y_diff * dt * self.animation_speed)
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка з урахуванням анімації"""
        if self.alpha > 0:
            super().draw(surface)
    
    def is_fully_visible(self) -> bool:
        """Чи повністю видима панель"""
        return self.alpha >= self.target_alpha and self.visible
    
    def is_hidden(self) -> bool:
        """Чи повністю схована панель"""
        return self.alpha <= 0 and not self.visible
