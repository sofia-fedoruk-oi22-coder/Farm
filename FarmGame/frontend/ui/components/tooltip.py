"""
Tooltip компонент
"""

import pygame
from typing import Tuple, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, get_font


class Tooltip:
    """
    Підказка при наведенні
    """
    
    def __init__(
        self,
        text: str,
        color: Tuple[int, int, int] = None,
        bg_color: Tuple[int, int, int] = None,
        font_size: int = None,
        padding: int = 8,
        delay: float = 0.5
    ):
        self.text = text
        self.color = color or COLORS["white"]
        self.bg_color = bg_color or COLORS["dark"]
        self.padding = padding
        self.delay = delay
        
        font_size = font_size or FONT_SIZES["small"]
        self.font = get_font(font_size)
        
        # Стан
        self.visible = False
        self.hover_time = 0.0
        self.position = (0, 0)
        self.alpha = 0
        self.target_alpha = 0
    
    def set_text(self, text: str):
        """Встановити текст"""
        self.text = text
    
    def show(self, x: int, y: int):
        """Показати в позиції"""
        self.position = (x, y)
        self.target_alpha = 255
        self.visible = True
    
    def hide(self):
        """Сховати"""
        self.target_alpha = 0
        self.visible = False
        self.hover_time = 0.0
    
    def update_hover(self, is_hovering: bool, mouse_pos: Tuple[int, int], dt: float):
        """Оновлення при наведенні"""
        if is_hovering:
            self.hover_time += dt
            if self.hover_time >= self.delay:
                self.show(mouse_pos[0], mouse_pos[1] - 30)
        else:
            self.hide()
    
    def update(self, dt: float):
        """Оновлення анімації"""
        alpha_diff = self.target_alpha - self.alpha
        self.alpha += alpha_diff * dt * 15
        self.alpha = max(0, min(255, self.alpha))
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        if self.alpha <= 0:
            return
        
        # Рендер тексту
        lines = self.text.split('\n')
        text_surfaces = [self.font.render(line, True, self.color) for line in lines]
        
        # Розміри
        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() for surf in text_surfaces)
        
        width = max_width + self.padding * 2
        height = total_height + self.padding * 2
        
        # Позиція (щоб не виходило за екран)
        x = self.position[0] - width // 2
        y = self.position[1] - height
        
        screen_rect = surface.get_rect()
        if x < 5:
            x = 5
        if x + width > screen_rect.width - 5:
            x = screen_rect.width - width - 5
        if y < 5:
            y = self.position[1] + 20  # Показуємо знизу
        
        # Створюємо поверхню
        tooltip_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Фон
        pygame.draw.rect(
            tooltip_surface,
            (*self.bg_color, int(self.alpha * 0.9)),
            tooltip_surface.get_rect(),
            border_radius=5
        )
        
        # Текст
        text_y = self.padding
        for text_surf in text_surfaces:
            text_surf.set_alpha(int(self.alpha))
            text_x = (width - text_surf.get_width()) // 2
            tooltip_surface.blit(text_surf, (text_x, text_y))
            text_y += text_surf.get_height()
        
        surface.blit(tooltip_surface, (x, y))


class TooltipManager:
    """
    Менеджер підказок
    """
    
    def __init__(self):
        self.active_tooltip: Optional[Tooltip] = None
        self.registered_elements = {}  # element -> tooltip
    
    def register(self, element, tooltip: Tooltip):
        """Зареєструвати елемент з підказкою"""
        self.registered_elements[element] = tooltip
    
    def unregister(self, element):
        """Видалити реєстрацію"""
        if element in self.registered_elements:
            del self.registered_elements[element]
    
    def update(self, mouse_pos: Tuple[int, int], dt: float):
        """Оновлення"""
        hovering_element = None
        
        for element, tooltip in self.registered_elements.items():
            if hasattr(element, 'rect') and element.rect.collidepoint(mouse_pos):
                hovering_element = element
                self.active_tooltip = tooltip
                tooltip.update_hover(True, mouse_pos, dt)
            else:
                tooltip.update_hover(False, mouse_pos, dt)
            
            tooltip.update(dt)
        
        if hovering_element is None:
            self.active_tooltip = None
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка активної підказки"""
        for tooltip in self.registered_elements.values():
            tooltip.draw(surface)
