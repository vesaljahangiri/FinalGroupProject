class InvalidCommandError(Exception):
    """Raised when the player enters an unknown command."""
class InvalidMoveError(Exception):
    """Raised when no map location exists in the requested direction."""
class SaveFileError(Exception):
    """Raised when a save slot contains invalid or incomplete data."""
class InventoryFullError(Exception):
    """Raised when an inventory change would exceed the weight limit."""
class NotEnoughGoldError(Exception):
    """Raised when the hero cannot afford an item."""
