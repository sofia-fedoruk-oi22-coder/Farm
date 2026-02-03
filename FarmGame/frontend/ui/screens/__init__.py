"""
Екрани гри
"""

from .main_menu import MainMenu
from .game_screen import GameScreen
from .shop_screen import ShopScreen
from .inventory_screen import InventoryScreen
from .settings_screen import SettingsScreen
from .new_game_screen import NewGameScreen
from .animal_details_screen import AnimalDetailsScreen

__all__ = [
    'MainMenu',
    'GameScreen', 
    'ShopScreen',
    'InventoryScreen',
    'SettingsScreen',
    'NewGameScreen',
    'AnimalDetailsScreen'
]
