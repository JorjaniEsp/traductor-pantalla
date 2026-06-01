"""
core/hotkey.py — Listener de hotkey global (Ctrl+Shift+Q)
"""

from pynput import keyboard


class HotkeyListener:
    """
    Escucha en segundo plano la combinación Ctrl+Shift+Q
    y llama al callback cuando se detecta.
    """

    def __init__(self, callback):
        self.callback = callback
        self._pressed = set()
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def start(self):
        self._listener.start()

    def join(self):
        self._listener.join()

    def stop(self):
        self._listener.stop()

    def _on_press(self, key):
        self._pressed.add(key)

        ctrl  = (keyboard.Key.ctrl_l  in self._pressed or
                 keyboard.Key.ctrl_r  in self._pressed)
        shift = (keyboard.Key.shift   in self._pressed or
                 keyboard.Key.shift_r in self._pressed)
        q     = (keyboard.KeyCode(char='q')    in self._pressed or
                 keyboard.KeyCode(char='Q')    in self._pressed or
                 keyboard.KeyCode(char='\x11') in self._pressed)  # Ctrl+Shift+Q en Windows

        if ctrl and shift and q:
            self._pressed.clear()  # Evitar doble disparo
            self.callback()

    def _on_release(self, key):
        self._pressed.discard(key)
