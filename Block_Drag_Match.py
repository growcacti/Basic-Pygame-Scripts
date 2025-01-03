import pygame
import random

class SlideAndMatchGame:
    def __init__(self, grid_size=25, block_size=50):
        pygame.init()

        self.grid_size = grid_size
        self.block_size = block_size
        self.window_size = (grid_size * block_size, grid_size * block_size)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Slide and Match with Random Colors")

        self.predefined_colors = self._generate_predefined_colors()
        self.grid = self._generate_grid(grid_size)

        self.dragging = False
        self.selected_block = None
        self.original_pos = None

        self.running = True

    def _generate_predefined_colors(self):
        return [
            (255, 0, 0),   # Red
            (0, 255, 0),   # Green
            (0, 0, 255),   # Blue
            (255, 255, 0), # Yellow
            (255, 165, 0), # Orange
            (128, 0, 128), # Purple
            (0, 255, 255), # Cyan
            (255, 192, 203), # Pink
            self._random_color(),
            self._random_color()
        ]

    def _random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def _generate_grid(self, size):
        return [[random.choice(self.predefined_colors) for _ in range(size)] for _ in range(size)]

    def _draw_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                pygame.draw.rect(
                    self.screen, 
                    self.grid[row][col], 
                    (col * self.block_size, row * self.block_size, self.block_size, self.block_size)
                )

    def _check_for_matches(self):
        # Placeholder for match checking logic
        return False

    def _expand_grid(self):
        new_row = [random.choice(self.predefined_colors) for _ in range(len(self.grid) + 1)]
        for row in self.grid:
            row.append(random.choice(self.predefined_colors))
        self.grid.append(new_row)

    def _get_block_at_pos(self, pos):
        x, y = pos
        col = x // self.block_size
        row = y // self.block_size
        if row < self.grid_size and col < self.grid_size:
            return row, col
        return None, None

    def _move_block(self, start_pos, end_pos):
        if start_pos and end_pos:
            start_row, start_col = start_pos
            end_row, end_col = end_pos
            self.grid[start_row][start_col], self.grid[end_row][end_col] = (
                self.grid[end_row][end_col],
                self.grid[start_row][start_col],
            )

    def _random_move(self):
        for _ in range(2):
            row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            direction = random.choice(["up", "down", "left", "right"])

            if direction == "up" and row > 0:
                self._move_block((row, col), (row - 1, col))
            elif direction == "down" and row < self.grid_size - 1:
                self._move_block((row, col), (row + 1, col))
            elif direction == "left" and col > 0:
                self._move_block((row, col), (row, col - 1))
            elif direction == "right" and col < self.grid_size - 1:
                self._move_block((row, col), (row, col + 1))

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))  # White background
            self._draw_grid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.original_pos = self._get_block_at_pos(pygame.mouse.get_pos())
                    if self.original_pos:
                        self.dragging = True
                        self.selected_block = self.original_pos

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging:
                        new_pos = self._get_block_at_pos(pygame.mouse.get_pos())
                        self._move_block(self.original_pos, new_pos)
                        self.dragging = False
                        self.selected_block = None
                        self._random_move()

            if self.dragging and self.selected_block:
                row, col = self.selected_block
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pygame.draw.rect(
                    self.screen, 
                    self.grid[row][col], 
                    (mouse_x - self.block_size // 2, mouse_y - self.block_size // 2, self.block_size, self.block_size)
                )

            if self._check_for_matches():
                self._expand_grid()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = SlideAndMatchGame()
    game.run()


