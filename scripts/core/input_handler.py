import pygame

class InputHandler:
    def __init__(self, game):
        # Dictionary to store the state of keys
        self.key_states = {}
        self.game = game
        
    def poll(self):
        """Check for input events and update the key_states dictionary."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                self.key_states[event.key] = True
                if event.key == pygame.K_g:
                    self.game.debug = not self.game.debug
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

            elif event.type == pygame.KEYUP:
                self.key_states[event.key] = False

        # Handle player input outside of the event loop for continuous motion
        self.game.player.handle_input(self)



                
    def is_key_pressed(self, key):
        """Return True if the given key is pressed, otherwise False."""
        return self.key_states.get(key, False)