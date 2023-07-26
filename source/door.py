import pygame.display
import tkinter.messagebox as msg
from source.items import InteractionObject, KeyItem
from source.const.map_objects import OBJECTS
from source.const import DoorState


class Door(InteractionObject):
    def __init__(self, game, location, position: tuple[int, int], destination: str | bytes, key: KeyItem = None, locked: bool = False):
        self.game = game
        self.location = location
        self.position = position
        self.destination = destination
        self.key = key
        if self.key is not None:
            self.key.set_parent(self)
        self.state = DoorState.LOCKED if locked else DoorState.UNLOCKED
        self.state = DoorState.LOCKED
    
    def interact(self) -> None | str:
        if self.state == DoorState.LOCKED:
            for item in self.game.player.inventory.items:
                if isinstance(item, KeyItem):
                    if item.parent != self:
                        continue
                    self.state = DoorState.UNLOCKED
                    return self.interact()
                continue
            return msg.showinfo("Knock Knock...", "The door appears to be locked!")

        self.game.map.tiles = []
        self.game.map.load(self.destination)  # Travel to next room.
        self.game.player.position = OBJECTS[self.location]['doors'][self.position][1]
        self.game.map_keys[0].set_parent(self.game.map_doors[0])

