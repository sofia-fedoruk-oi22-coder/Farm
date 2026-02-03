"""
Поле вводу тексту
"""

import pygame
from typing import Tuple, Callable, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, get_font


class InputField:
    """
    Поле для вводу тексту
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        placeholder: str = "",
        text: str = "",
        max_length: int = 50,
        font_size: int = None,
        color: Tuple[int, int, int] = None,
        bg_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
        focus_color: Tuple[int, int, int] = None,
        border_radius: int = 10,
        on_change: Callable[[str], None] = None,
        on_submit: Callable[[str], None] = None,
        password: bool = False
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.max_length = max_length
        
        self.color = color or COLORS["text"]
        self.bg_color = bg_color or COLORS["white"]
        self.border_color = border_color or COLORS["border"]
        self.focus_color = focus_color or COLORS["primary"]
        self.placeholder_color = COLORS["gray"]
        self.border_radius = border_radius
        
        self.on_change = on_change
        self.on_submit = on_submit
        self.password = password
        
        # Стан
        self.focused = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.cursor_position = len(text)
        
        # Шрифт
        font_size = font_size or FONT_SIZES["normal"]
        self.font = get_font(font_size)
        
        # Скроллінг
        self.scroll_offset = 0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обробка подій"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                was_focused = self.focused
                self.focused = self.rect.collidepoint(event.pos)
                
                if self.focused and not was_focused:
                    self.cursor_position = len(self.text)
                    self.cursor_visible = True
                    self.cursor_timer = 0
                
                return self.focused
        
        elif event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
                    self._on_text_change()
            
            elif event.key == pygame.K_DELETE:
                if self.cursor_position < len(self.text):
                    self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
                    self._on_text_change()
            
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
            
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
            
            elif event.key == pygame.K_HOME:
                self.cursor_position = 0
            
            elif event.key == pygame.K_END:
                self.cursor_position = len(self.text)
            
            elif event.key == pygame.K_RETURN:
                if self.on_submit:
                    self.on_submit(self.text)
                return True
            
            elif event.key == pygame.K_ESCAPE:
                self.focused = False
                return True
            
            elif event.unicode and len(self.text) < self.max_length:
                # Фільтруємо непотрібні символи
                if event.unicode.isprintable():
                    self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                    self.cursor_position += 1
                    self._on_text_change()
            
            self.cursor_visible = True
            self.cursor_timer = 0
            return True
        
        return False
    
    def _on_text_change(self):
        """Виклик callback при зміні тексту"""
        if self.on_change:
            self.on_change(self.text)
        self._update_scroll()
    
    def _update_scroll(self):
        """Оновлення скролінгу"""
        display_text = self._get_display_text()
        cursor_x = self.font.size(display_text[:self.cursor_position])[0]
        
        available_width = self.rect.width - 20
        
        if cursor_x - self.scroll_offset > available_width:
            self.scroll_offset = cursor_x - available_width + 20
        elif cursor_x - self.scroll_offset < 0:
            self.scroll_offset = max(0, cursor_x - 20)
    
    def _get_display_text(self) -> str:
        """Отримати текст для відображення"""
        if self.password:
            return '*' * len(self.text)
        return self.text
    
    def update(self, dt: float):
        """Оновлення курсора"""
        if self.focused:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка поля"""
        # Фон
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)
        
        # Рамка
        border_color = self.focus_color if self.focused else self.border_color
        border_width = 2 if self.focused else 1
        pygame.draw.rect(surface, border_color, self.rect, 
                        width=border_width, border_radius=self.border_radius)
        
        # Створюємо область відсікання
        clip_rect = pygame.Rect(self.rect.x + 10, self.rect.y, self.rect.width - 20, self.rect.height)
        old_clip = surface.get_clip()
        surface.set_clip(clip_rect)
        
        # Текст або placeholder
        if self.text:
            display_text = self._get_display_text()
            text_surface = self.font.render(display_text, True, self.color)
        else:
            text_surface = self.font.render(self.placeholder, True, self.placeholder_color)
        
        text_x = self.rect.x + 10 - self.scroll_offset
        text_y = self.rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
        
        # Курсор
        if self.focused and self.cursor_visible:
            display_text = self._get_display_text()
            cursor_x = self.rect.x + 10 + self.font.size(display_text[:self.cursor_position])[0] - self.scroll_offset
            cursor_y1 = self.rect.centery - text_surface.get_height() // 2
            cursor_y2 = cursor_y1 + text_surface.get_height()
            pygame.draw.line(surface, self.color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
        
        # Відновлюємо область відсікання
        surface.set_clip(old_clip)
    
    def get_text(self) -> str:
        """Отримати текст"""
        return self.text
    
    def set_text(self, text: str):
        """Встановити текст"""
        self.text = text[:self.max_length]
        self.cursor_position = len(self.text)
        self._update_scroll()
    
    def clear(self):
        """Очистити поле"""
        self.text = ""
        self.cursor_position = 0
        self.scroll_offset = 0
    
    def focus(self):
        """Встановити фокус"""
        self.focused = True
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def unfocus(self):
        """Зняти фокус"""
        self.focused = False
