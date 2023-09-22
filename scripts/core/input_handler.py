import pygame

class InputHandler:
    def __init__(self):
        # Dictionary to store the state of keys
        self.key_states = {}
        
    def poll(self):
        """Check for input events and update the key_states dictionary."""
        for event in pygame.event.get():
            # If the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                
            # Check for key down events
            if event.type == pygame.KEYDOWN:
                self.key_states[event.key] = True
                
            # Check for key up events
            if event.type == pygame.KEYUP:
                self.key_states[event.key] = False
                
    def is_key_pressed(self, key):
        """Return True if the given key is pressed, otherwise False."""
        return self.key_states.get(key, False)