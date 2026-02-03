"""
Екран інвентарю
"""

import pygame
from typing import Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES,
    FEED_TYPES, BUILDING_TYPES, get_font, get_emoji_font
)
from game.game_state import GameState
from ..components.button import Button
from ..components.panel import Panel
from ..components.text import Text
from ..components.progress_bar import ProgressBar
from ..components.notification import NotificationManager


class InventoryScreen:
    """
    Екран інвентарю - корми, продукція, будівлі
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        # Менеджер сповіщень
        self.notification_manager = NotificationManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Вкладки: feeds, products, buildings
        self.current_tab = "feeds"
        
        # Скролінг
        self.scroll_offset = 0
        self.max_scroll = 0
        
        self._create_ui()
    
    def _create_ui(self):
        """Створення UI"""
        # Верхня панель
        self.top_panel = Panel(
            0, 0, SCREEN_WIDTH, 70,
            color=COLORS["panel_dark"],
            border_radius=0,
            shadow=False
        )
        
        # Основна панель
        self.main_panel = Panel(
            10, 80, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 90,
            color=COLORS["panel"]
        )
        
        # Вкладки
        self.btn_feeds_tab = Button(
            20, 15, 140, 40,
            "🌾 Корми",
            lambda: self._set_tab("feeds"),
            color=COLORS["warning"]
        )
        
        self.btn_products_tab = Button(
            170, 15, 150, 40,
            "Продукція",
            lambda: self._set_tab("products"),
            color=COLORS["success"]
        )
        
        self.btn_buildings_tab = Button(
            330, 15, 140, 40,
            "Будівлі",
            lambda: self._set_tab("buildings"),
            color=COLORS["info"]
        )
        
        # Кнопка назад
        self.btn_back = Button(
            SCREEN_WIDTH - 130, 15, 120, 40,
            "← Назад",
            self._on_back,
            color=COLORS["gray"]
        )
        
        self._update_tab_buttons()
    
    def _set_tab(self, tab: str):
        """Змінити вкладку"""
        self.current_tab = tab
        self.scroll_offset = 0
        self._update_tab_buttons()
    
    def _update_tab_buttons(self):
        """Оновити стиль кнопок вкладок"""
        tabs = {
            "feeds": (self.btn_feeds_tab, COLORS["warning"]),
            "products": (self.btn_products_tab, COLORS["success"]),
            "buildings": (self.btn_buildings_tab, COLORS["info"])
        }
        
        for tab_name, (btn, color) in tabs.items():
            if tab_name == self.current_tab:
                btn.color = color
                btn.border_width = 3
                btn.border_color = COLORS["white"]
            else:
                btn.color = COLORS["secondary"]
                btn.border_width = 0
    
    def _on_back(self):
        """Повернутися до гри"""
        self.game_engine.change_screen("game")
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        # Скролінг
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.main_panel.rect.collidepoint(mouse_pos):
                self.scroll_offset -= event.y * 30
                self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
        
        # Кнопки
        self.btn_feeds_tab.handle_event(event)
        self.btn_products_tab.handle_event(event)
        self.btn_buildings_tab.handle_event(event)
        self.btn_back.handle_event(event)
        
        # Кліки на елементи (для будівель - апгрейд)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_tab == "buildings":
                self._handle_building_click(event.pos)
        
        # ESC - назад
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._on_back()
    
    def _handle_building_click(self, mouse_pos):
        """Обробка кліку на будівлю"""
        content_rect = self.main_panel.get_content_rect()
        
        card_height = 120
        card_spacing = 15
        
        for i, building in enumerate(self.game_state.buildings):
            y = content_rect.y + 10 + i * (card_height + card_spacing) - self.scroll_offset
            
            # Кнопка апгрейду
            upgrade_rect = pygame.Rect(
                content_rect.right - 150,
                y + 35,
                130,
                40
            )
            
            if upgrade_rect.collidepoint(mouse_pos):
                if self.game_state.upgrade_building(building.building_type):
                    self.notification_manager.add_success(
                        "Покращення",
                        f"{building.name} покращено до рівня {building.level}!"
                    )
    
    def update(self, dt: float):
        """Оновлення"""
        self.btn_feeds_tab.update(dt)
        self.btn_products_tab.update(dt)
        self.btn_buildings_tab.update(dt)
        self.btn_back.update(dt)
        
        self.notification_manager.update(dt)
        
        # Синхронізація сповіщень
        while self.game_state.notifications:
            notif = self.game_state.notifications.pop(0)
            self.notification_manager.add_info(notif['title'], notif['message'])
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        surface.fill(COLORS["background"])
        
        # Панелі
        self.top_panel.draw(surface)
        self.main_panel.draw(surface)
        
        # Заголовок
        title_font = get_font(FONT_SIZES["huge"], bold=True)
        emoji_font_huge = get_font(FONT_SIZES["huge"])
        title = emoji_font_huge.render("Інвентар", True, COLORS["text"])
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))
        
        # Вкладки
        self.btn_feeds_tab.draw(surface)
        self.btn_products_tab.draw(surface)
        self.btn_buildings_tab.draw(surface)
        self.btn_back.draw(surface)
        
        # Контент
        if self.current_tab == "feeds":
            self._draw_feeds(surface)
        elif self.current_tab == "products":
            self._draw_products(surface)
        else:
            self._draw_buildings(surface)
        
        # Сповіщення
        self.notification_manager.draw(surface)
    
    def _draw_feeds(self, surface: pygame.Surface):
        """Відмальовка кормів"""
        content_rect = self.main_panel.get_content_rect()
        
        font = get_font(FONT_SIZES["normal"], bold=True)
        small_font = get_font(FONT_SIZES["small"])
        emoji_font = get_emoji_font(28)
        
        if not self.game_state.feeds:
            hint = font.render("Немає кормів. Купіть у магазині!", True, COLORS["text_secondary"])
            hint_rect = hint.get_rect(center=(content_rect.centerx, content_rect.centery))
            surface.blit(hint, hint_rect)
            return
        
        card_height = 80
        card_spacing = 10
        
        # Обчислюємо max_scroll
        total_height = len(self.game_state.feeds) * (card_height + card_spacing)
        self.max_scroll = max(0, total_height - content_rect.height + 20)
        
        # Відсікання
        old_clip = surface.get_clip()
        surface.set_clip(content_rect)
        
        for i, (feed_type, feed_data) in enumerate(self.game_state.feeds.items()):
            y = content_rect.y + 10 + i * (card_height + card_spacing) - self.scroll_offset
            
            if y < content_rect.y - card_height or y > content_rect.bottom:
                continue
            
            card_rect = pygame.Rect(content_rect.x + 10, y, content_rect.width - 20, card_height)
            
            pygame.draw.rect(surface, COLORS["panel_dark"], card_rect, border_radius=10)
            pygame.draw.rect(surface, COLORS["border"], card_rect, width=1, border_radius=10)
            
            feed_info = FEED_TYPES.get(feed_type, {})
            
            # Emoji
            emoji = feed_info.get('emoji', '📦')
            emoji_surface = emoji_font.render(emoji, True, COLORS["text"])
            surface.blit(emoji_surface, (card_rect.x + 15, card_rect.y + 15))
            
            # Назва
            name = feed_info.get('name', feed_type)
            name_surface = font.render(name, True, COLORS["text"])
            surface.blit(name_surface, (card_rect.x + 60, card_rect.y + 15))
            
            # Кількість
            amount_surface = font.render(f"{feed_data.amount:.1f} кг", True, COLORS["success"])
            surface.blit(amount_surface, (card_rect.x + 60, card_rect.y + 45))
            
            # Якість та термін
            quality_surface = small_font.render(
                f"Якість: {feed_data.quality:.0f}% | Термін: {feed_data.days_remaining} дн.",
                True, COLORS["text_secondary"]
            )
            surface.blit(quality_surface, (card_rect.x + 200, card_rect.y + 50))
            
            # Прогрес бар кількості
            bar_rect = pygame.Rect(card_rect.right - 150, card_rect.y + 30, 130, 20)
            pygame.draw.rect(surface, COLORS["panel"], bar_rect, border_radius=5)
            fill_width = min(130, int(feed_data.amount / 100 * 130))
            fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_width, 20)
            pygame.draw.rect(surface, COLORS["success"], fill_rect, border_radius=5)
        
        surface.set_clip(old_clip)
    
    def _draw_products(self, surface: pygame.Surface):
        """Відмальовка продукції"""
        content_rect = self.main_panel.get_content_rect()
        
        font = get_font(FONT_SIZES["normal"], bold=True)
        small_font = get_font(FONT_SIZES["small"])
        
        if not self.game_state.products:
            hint = font.render("Немає продукції. Зберіть від тварин!", True, COLORS["text_secondary"])
            hint_rect = hint.get_rect(center=(content_rect.centerx, content_rect.centery))
            surface.blit(hint, hint_rect)
            return
        
        card_height = 80
        card_spacing = 10
        
        # Відсікання
        old_clip = surface.get_clip()
        surface.set_clip(content_rect)
        
        for i, (product_type, product_data) in enumerate(self.game_state.products.items()):
            y = content_rect.y + 10 + i * (card_height + card_spacing) - self.scroll_offset
            
            if y < content_rect.y - card_height or y > content_rect.bottom:
                continue
            
            card_rect = pygame.Rect(content_rect.x + 10, y, content_rect.width - 20, card_height)
            
            pygame.draw.rect(surface, COLORS["panel_dark"], card_rect, border_radius=10)
            pygame.draw.rect(surface, COLORS["border"], card_rect, width=1, border_radius=10)
            
            # Назва продукту
            name = product_type.replace('_product', '').title()
            emoji_font_normal = get_font(FONT_SIZES["normal"])
            name_surface = emoji_font_normal.render(f"📦 {name}", True, COLORS["text"])
            surface.blit(name_surface, (card_rect.x + 15, card_rect.y + 15))
            
            # Кількість
            amount_surface = font.render(f"{product_data.amount:.1f} од.", True, COLORS["success"])
            surface.blit(amount_surface, (card_rect.x + 200, card_rect.y + 15))
            
            # Якість
            quality_colors = {
                "poor": COLORS["danger"],
                "normal": COLORS["warning"],
                "good": COLORS["success"],
                "excellent": COLORS["primary"]
            }
            quality_names = {
                "poor": "Низька",
                "normal": "Звичайна",
                "good": "Хороша",
                "excellent": "Відмінна"
            }
            quality_color = quality_colors.get(product_data.quality, COLORS["text"])
            quality_name = quality_names.get(product_data.quality, product_data.quality)
            
            quality_surface = small_font.render(f"Якість: {quality_name}", True, quality_color)
            surface.blit(quality_surface, (card_rect.x + 15, card_rect.y + 50))
            
            # Термін придатності
            days_surface = small_font.render(f"Термін: {product_data.days_remaining} дн.", True, COLORS["text_secondary"])
            surface.blit(days_surface, (card_rect.x + 200, card_rect.y + 50))
        
        surface.set_clip(old_clip)
        
        # Кнопка продажу всього
        sell_btn_rect = pygame.Rect(
            content_rect.right - 200,
            content_rect.bottom - 50,
            180,
            40
        )
        pygame.draw.rect(surface, COLORS["success"], sell_btn_rect, border_radius=10)
        emoji_font_normal = get_font(FONT_SIZES["normal"])
        sell_text = emoji_font_normal.render("💰 Продати все", True, COLORS["white"])
        sell_text_rect = sell_text.get_rect(center=sell_btn_rect.center)
        surface.blit(sell_text, sell_text_rect)
    
    def _draw_buildings(self, surface: pygame.Surface):
        """Відмальовка будівель"""
        content_rect = self.main_panel.get_content_rect()
        
        font = get_font(FONT_SIZES["normal"], bold=True)
        small_font = get_font(FONT_SIZES["small"])
        emoji_font = get_emoji_font(32)
        
        card_height = 120
        card_spacing = 15
        
        # Відсікання
        old_clip = surface.get_clip()
        surface.set_clip(content_rect)
        
        for i, building in enumerate(self.game_state.buildings):
            y = content_rect.y + 10 + i * (card_height + card_spacing) - self.scroll_offset
            
            if y < content_rect.y - card_height or y > content_rect.bottom:
                continue
            
            card_rect = pygame.Rect(content_rect.x + 10, y, content_rect.width - 20, card_height)
            
            pygame.draw.rect(surface, COLORS["panel_dark"], card_rect, border_radius=10)
            pygame.draw.rect(surface, COLORS["border"], card_rect, width=2, border_radius=10)
            
            building_info = BUILDING_TYPES.get(building.building_type, {})
            
            # Emoji
            emoji = building_info.get('emoji', '🏠')
            emoji_surface = emoji_font.render(emoji, True, COLORS["text"])
            surface.blit(emoji_surface, (card_rect.x + 15, card_rect.y + 15))
            
            # Назва
            name_surface = font.render(building.name, True, COLORS["text"])
            surface.blit(name_surface, (card_rect.x + 65, card_rect.y + 15))
            
            # Рівень
            emoji_font_small = get_font(FONT_SIZES["small"])
            level_surface = emoji_font_small.render(f"⭐ Рівень {building.level}", True, COLORS["warning"])
            surface.blit(level_surface, (card_rect.x + 65, card_rect.y + 45))
            
            # Місткість
            capacity_surface = small_font.render(f"📊 Місткість: {building.capacity}", True, COLORS["text_secondary"])
            surface.blit(capacity_surface, (card_rect.x + 65, card_rect.y + 70))
            
            # Опис
            description = building_info.get('description', '')
            desc_surface = small_font.render(description, True, COLORS["text_secondary"])
            surface.blit(desc_surface, (card_rect.x + 200, card_rect.y + 70))
            
            # Кнопка апгрейду
            base_cost = building_info.get('base_cost', 5000)
            multiplier = building_info.get('upgrade_cost_multiplier', 1.5)
            upgrade_cost = int(base_cost * (multiplier ** building.level))
            
            upgrade_rect = pygame.Rect(card_rect.right - 150, card_rect.y + 35, 130, 40)
            
            can_afford = self.game_state.farmer.money >= upgrade_cost
            btn_color = COLORS["success"] if can_afford else COLORS["gray"]
            
            pygame.draw.rect(surface, btn_color, upgrade_rect, border_radius=8)
            
            upgrade_text = small_font.render(f"⬆️ {upgrade_cost} грн", True, COLORS["white"])
            upgrade_text_rect = upgrade_text.get_rect(center=upgrade_rect.center)
            surface.blit(upgrade_text, upgrade_text_rect)
        
        surface.set_clip(old_clip)
