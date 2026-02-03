"""
Текстові компоненти
"""

import pygame
from typing import Tuple, Optional
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, get_font


class Text:
    """
    Текстовий компонент
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        color: Tuple[int, int, int] = None,
        font_size: int = None,
        bold: bool = False,
        italic: bool = False,
        font_name: str = 'Arial',
        shadow: bool = False,
        shadow_color: Tuple[int, int, int] = None,
        align: str = 'left',  # 'left', 'center', 'right'
        max_width: int = None
    ):
        self.x = x
        self.y = y
        self.text = text
        self.color = color or COLORS["text"]
        self.shadow = shadow
        self.shadow_color = shadow_color or COLORS["dark"]
        self.align = align
        self.max_width = max_width
        
        font_size = font_size or FONT_SIZES["normal"]
        # Використовуємо get_font для підтримки кирилиці
        self.font = get_font(font_size, bold=bold)
        
        self._rendered_text = None
        self._lines = []
        self._needs_render = True
    
    def set_text(self, text: str):
        """Встановити текст"""
        if self.text != text:
            self.text = text
            self._needs_render = True
    
    def set_color(self, color: Tuple[int, int, int]):
        """Встановити колір"""
        if self.color != color:
            self.color = color
            self._needs_render = True
    
    def _render(self):
        """Рендеринг тексту"""
        if self.max_width:
            self._lines = self._wrap_text()
        else:
            self._lines = [self.text]
        
        self._needs_render = False
    
    def _wrap_text(self) -> list:
        """Розбиття тексту на рядки"""
        words = self.text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= self.max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def get_size(self) -> Tuple[int, int]:
        """Отримати розмір тексту"""
        if self._needs_render:
            self._render()
        
        if not self._lines:
            return (0, 0)
        
        width = max(self.font.size(line)[0] for line in self._lines)
        height = len(self._lines) * self.font.get_linesize()
        return (width, height)
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка тексту"""
        if self._needs_render:
            self._render()
        
        y = self.y
        line_height = self.font.get_linesize()
        
        for line in self._lines:
            text_surface = self.font.render(line, True, self.color)
            
            # Вирівнювання
            if self.align == 'center':
                x = self.x - text_surface.get_width() // 2
            elif self.align == 'right':
                x = self.x - text_surface.get_width()
            else:
                x = self.x
            
            # Тінь
            if self.shadow:
                shadow_surface = self.font.render(line, True, self.shadow_color)
                surface.blit(shadow_surface, (x + 2, y + 2))
            
            surface.blit(text_surface, (x, y))
            y += line_height
    
    @property
    def rect(self) -> pygame.Rect:
        """Отримати прямокутник тексту"""
        width, height = self.get_size()
        
        if self.align == 'center':
            x = self.x - width // 2
        elif self.align == 'right':
            x = self.x - width
        else:
            x = self.x
        
        return pygame.Rect(x, self.y, width, height)


class AnimatedText(Text):
    """
    Текст з анімаціями
    """
    
    def __init__(self, *args, **kwargs):
        # Анімаційні параметри
        self.animation_type = kwargs.pop('animation', None)  # 'fade', 'bounce', 'pulse', 'typewriter'
        self.animation_speed = kwargs.pop('animation_speed', 2.0)
        
        super().__init__(*args, **kwargs)
        
        self.alpha = 255
        self.target_alpha = 255
        self.offset_y = 0
        self.scale = 1.0
        self.time = 0.0
        
        # Для typewriter
        self.displayed_chars = len(self.text) if self.animation_type != 'typewriter' else 0
        self.full_text = self.text
    
    def update(self, dt: float):
        """Оновлення анімації"""
        self.time += dt
        
        if self.animation_type == 'fade':
            # Плавне затухання
            diff = self.target_alpha - self.alpha
            if abs(diff) > 1:
                self.alpha += diff * dt * self.animation_speed
        
        elif self.animation_type == 'bounce':
            # Підстрибування
            self.offset_y = abs(math.sin(self.time * self.animation_speed * 3)) * 10
        
        elif self.animation_type == 'pulse':
            # Пульсація
            self.scale = 1.0 + math.sin(self.time * self.animation_speed * 2) * 0.1
        
        elif self.animation_type == 'typewriter':
            # Друкарська машинка
            self.displayed_chars = min(
                len(self.full_text),
                int(self.time * self.animation_speed * 10)
            )
            self.text = self.full_text[:self.displayed_chars]
            self._needs_render = True
    
    def fade_in(self, duration: float = 1.0):
        """Поява"""
        self.alpha = 0
        self.target_alpha = 255
        self.animation_speed = 1.0 / duration
    
    def fade_out(self, duration: float = 1.0):
        """Зникнення"""
        self.target_alpha = 0
        self.animation_speed = 1.0 / duration
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка з анімацією"""
        if self._needs_render:
            self._render()
        
        y = self.y + self.offset_y
        line_height = self.font.get_linesize()
        
        for line in self._lines:
            text_surface = self.font.render(line, True, self.color)
            
            # Масштабування
            if self.scale != 1.0:
                new_width = int(text_surface.get_width() * self.scale)
                new_height = int(text_surface.get_height() * self.scale)
                text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
            
            # Прозорість
            if self.alpha < 255:
                text_surface.set_alpha(int(self.alpha))
            
            # Вирівнювання
            if self.align == 'center':
                x = self.x - text_surface.get_width() // 2
            elif self.align == 'right':
                x = self.x - text_surface.get_width()
            else:
                x = self.x
            
            # Тінь
            if self.shadow and self.alpha > 0:
                shadow_surface = self.font.render(line, True, self.shadow_color)
                shadow_surface.set_alpha(int(self.alpha * 0.5))
                surface.blit(shadow_surface, (x + 2, y + 2))
            
            surface.blit(text_surface, (x, y))
            y += line_height
    
    def is_animation_complete(self) -> bool:
        """Чи завершена анімація"""
        if self.animation_type == 'typewriter':
            return self.displayed_chars >= len(self.full_text)
        elif self.animation_type == 'fade':
            return abs(self.alpha - self.target_alpha) < 1
        return True
    
    def reset_animation(self):
        """Скинути анімацію"""
        self.time = 0
        self.alpha = 255
        self.offset_y = 0
        self.scale = 1.0
        self.displayed_chars = 0 if self.animation_type == 'typewriter' else len(self.full_text)
