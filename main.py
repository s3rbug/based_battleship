import pygame
import sys
import random
import copy
import colors
from stuff import left_margin, upper_margin, block_size, size, LETTERS, font
from AutoShips import AutoShips
from Button import Button
from Grid import Grid


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Battleship")
        self.computer_available_to_fire_set = {(x, y) for x in range(16, 26) for y in range(1, 11)}
        self.around_last_computer_hit_set = set()
        self.dotted_set_for_computer_not_to_shoot = set()
        self.hit_blocks_for_computer_not_to_shoot = set()
        self.last_hits_list = []
        self.hit_blocks = set()
        self.dotted_set = set()
        self.destroyed_computer_ships = []
        self.ships_creation_not_decided = True
        self.ships_not_created = True
        self.drawing = False
        self.game_over = False
        self.computer_turn = False
        self.start = (0, 0)
        self.end = (0, 0)
        self.ship_size = (0, 0)
        self.human_ships_working = None
        # Screen parameters
        self.computer = AutoShips(0)
        self.computer_ships_working = copy.deepcopy(self.computer.ships)
        self.screen = pygame.display.set_mode((0, 0))
        # This ratio is purely for scaling the font according to the block size
        self.game_over_font = pygame.font.SysFont('arial', 3 * block_size)
        # Create AUTO and MANUAL buttons and explanatory message for them
        self.auto_button = Button(left_margin + 17 * block_size,
                                  "AUTO", "How do you want to create your ships? Click the button", self.screen)
        self.manual_button = Button(left_margin + 20 * block_size, "MANUAL",
                                    "How do you want to create your ships? Click the button", self.screen)
        # Create UNDO message and button
        self.undo_button = Button(left_margin + 12 * block_size, "UNDO LAST SHIP",
                                  "To undo the last ship click the button", self.screen)

        # Create PLAY AGAIN and QUIT buttons and message for them
        self.play_again_button = Button(left_margin + 15 * block_size, "PLAY AGAIN",
                                        "Do you want to play again or quit?", self.screen)
        self.quit_game_button = Button(left_margin + 20 * block_size, "QUIT", "", self.screen)

        self.rect_for_grids = (0, 0, size[0], upper_margin + 12 * block_size)
        self.rect_for_messages_and_buttons = (
            0, upper_margin + 11 * block_size, size[0], 5 * block_size)
        self.message_rect_for_drawing_ships = (self.undo_button.rect_for_draw[0] + self.undo_button.rect_for_draw[2],
                                               upper_margin + 11 * block_size, size[0] -
                                               (self.undo_button.rect_for_draw[0] + self.undo_button.rect_for_draw[2]),
                                               4 * block_size)
        self.message_rect_computer = (left_margin - 2 * block_size,
                                      upper_margin + 11 * block_size, 14 * block_size,
                                      4 * block_size)
        self.message_rect_human = (left_margin + 15 * block_size,
                                   upper_margin + 11 * block_size,
                                   10 * block_size,
                                   4 * block_size)

        self.human_ships_to_draw = []
        self.human_ships_set = set()
        self.used_blocks_for_manual_drawing = set()
        self.num_ships_list = [0, 0, 0, 0]

    def game(self):
        self.screen.fill(colors.WHITE)
        Grid("COMPUTER", 0, self.screen)
        Grid("HUMAN", 15, self.screen)

        while self.ships_creation_not_decided:
            self.auto_button.draw_button()
            self.manual_button.draw_button()
            self.auto_button.change_color_on_hover()
            self.manual_button.change_color_on_hover()
            self.auto_button.print_message_for_button()

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    self.ships_creation_not_decided = False
                    self.ships_not_created = False
                # If AUTO button is pressed - create human ships automatically
                elif event.type == pygame.MOUSEBUTTONDOWN and self.auto_button.rect.collidepoint(mouse):
                    human = AutoShips(15)
                    self.human_ships_to_draw = human.ships
                    self.human_ships_working = copy.deepcopy(human.ships)
                    self.human_ships_set = human.ships_set
                    self.ships_creation_not_decided = False
                    self.ships_not_created = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.manual_button.rect.collidepoint(mouse):
                    self.ships_creation_not_decided = False

            pygame.display.update()
            self.screen.fill(colors.WHITE, self.rect_for_messages_and_buttons)
        x_start = y_start = 0
        while self.ships_not_created:
            self.screen.fill(colors.WHITE, self.rect_for_grids)
            Grid("COMPUTER", 0, self.screen)
            Grid("HUMAN", 15, self.screen)
            self.undo_button.draw_button()
            self.undo_button.print_message_for_button()
            self.undo_button.change_color_on_hover()
            mouse = pygame.mouse.get_pos()
            if not self.human_ships_to_draw:
                self.undo_button.draw_button(colors.LIGHT_GRAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ships_not_created = False
                    self.game_over = True
                elif self.undo_button.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.human_ships_to_draw:
                        self.screen.fill(colors.WHITE, self.message_rect_for_drawing_ships)
                        deleted_ship = self.human_ships_to_draw.pop()
                        self.num_ships_list[len(deleted_ship) - 1] -= 1
                        self.update_used_blocks(
                            deleted_ship, self.used_blocks_for_manual_drawing.discard)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.drawing = True
                    x_start, y_start = event.pos
                    self.start = x_start, y_start
                    self.ship_size = (0, 0)
                elif self.drawing and event.type == pygame.MOUSEMOTION:
                    x_end, y_end = event.pos
                    self.end = x_end, y_end
                    self.ship_size = x_end - x_start, y_end - y_start
                elif self.drawing and event.type == pygame.MOUSEBUTTONUP:
                    x_end, y_end = event.pos
                    self.end = x_end, y_end
                    self.drawing = False
                    self.ship_size = (0, 0)
                    start_block = self.get_start_block(x_start, y_start)
                    end_block = self.get_end_block(x_end, y_end)
                    if start_block > end_block:
                        start_block, end_block = end_block, start_block
                    temp_ship = []
                    if self.check_if_inside_of_board(x_start, y_start, x_end, y_end):
                        self.screen.fill(colors.WHITE, self.message_rect_for_drawing_ships)
                        if start_block[0] == end_block[0] and (end_block[1] - start_block[1]) < 4:
                            for block in range(start_block[1], end_block[1] + 1):
                                temp_ship.append((start_block[0], block))
                        elif start_block[1] == end_block[1] and (end_block[0] - start_block[0]) < 4:
                            for block in range(start_block[0], end_block[0] + 1):
                                temp_ship.append((block, start_block[1]))
                        else:
                            self.show_message_at_rect_center(
                                "Ship is too large! Try again!", self.message_rect_for_drawing_ships)
                    else:
                        self.show_message_at_rect_center(
                            "Ship is beyond your grid! Try again!", self.message_rect_for_drawing_ships)
                    if temp_ship:
                        temp_ship_set = set(temp_ship)
                        if self.ship_is_valid(temp_ship_set, self.used_blocks_for_manual_drawing):
                            if self.check_ships_numbers(temp_ship, self.num_ships_list):
                                self.num_ships_list[len(temp_ship) - 1] += 1
                                self.human_ships_to_draw.append(temp_ship)
                                self.human_ships_set |= temp_ship_set
                                self.update_used_blocks(
                                    temp_ship, self.used_blocks_for_manual_drawing.add)
                            else:
                                self.show_message_at_rect_center(
                                    f"There already are enough of {len(temp_ship)} ships!",
                                    self.message_rect_for_drawing_ships)
                        else:
                            self.show_message_at_rect_center(
                                "Ships are touching! Try again", self.message_rect_for_drawing_ships)
                if len(self.human_ships_to_draw) == 10:
                    self.ships_not_created = False
                    self.human_ships_working = copy.deepcopy(self.human_ships_to_draw)
                    self.screen.fill(colors.WHITE, self.rect_for_messages_and_buttons)
            x_start, y_start = self.start
            x_end, y_end = self.end
            if self.check_if_inside_of_board(x_start, y_start, x_end, y_end):
                abs_ship_size = abs(self.ship_size[0]), abs(self.ship_size[1])
                changed_start = (self.start[0] if self.ship_size[0] >= 0 else self.start[0] + self.ship_size[0],
                                 self.start[1] if self.ship_size[1] >= 0 else self.start[1] + self.ship_size[1])
                pygame.draw.rect(self.screen, colors.BLACK, (changed_start, abs_ship_size), 3)
            self.draw_ships(self.human_ships_to_draw)
            pygame.display.update()
        shown = False
        while not self.game_over:
            self.draw_ships(self.destroyed_computer_ships)
            self.draw_ships(self.human_ships_to_draw)
            if not (self.dotted_set | self.hit_blocks):
                if not shown:
                    self.show_message_at_rect_center(
                        "GAME STARTED! YOUR MOVE!", self.message_rect_computer)
                shown = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif not self.computer_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (left_margin < x < left_margin + 10 * block_size) and (
                            upper_margin < y < upper_margin + 10 * block_size):
                        fired_block = ((x - left_margin) // block_size + 1,
                                       (y - upper_margin) // block_size + 1)
                        self.computer_turn = self.check_hit_or_miss(fired_block, self.computer_ships_working, False,
                                                                    self.computer.ships, self.computer.ships_set)
                        if self.computer_turn is None:
                            continue
                        else:
                            self.computer_turn = not self.computer_turn
                        self.draw_from_dotted_set(self.dotted_set)
                        self.draw_hit_blocks(self.hit_blocks)
                        self.screen.fill(colors.WHITE, self.message_rect_computer)
                        self.show_message_at_rect_center(
                            f"Your last shot: {LETTERS[fired_block[0] - 1] + str(fired_block[1])}",
                            self.message_rect_computer,
                            color=colors.BLACK)
                    else:
                        self.show_message_at_rect_center(
                            "Your shot is outside of grid! Try again", self.message_rect_computer)
            if self.computer_turn:
                set_to_shoot_from = self.computer_available_to_fire_set
                if self.around_last_computer_hit_set:
                    set_to_shoot_from = self.around_last_computer_hit_set
                fired_block = self.computer_shoots(set_to_shoot_from)
                self.computer_turn = self.check_hit_or_miss(
                    fired_block, self.human_ships_working, True, self.human_ships_to_draw, self.human_ships_set)
                self.draw_from_dotted_set(self.dotted_set)
                self.draw_hit_blocks(self.hit_blocks)
                self.screen.fill(colors.WHITE, self.message_rect_human)
                self.show_message_at_rect_center(
                    f"Computer's last shot: {LETTERS[fired_block[0] - 16] + str(fired_block[1])}",
                    self.message_rect_human,
                    color=colors.BLACK)
            if not self.computer.ships_set:
                self.show_message_at_rect_center(
                    "YOU WON!", (0, 0, size[0], size[1]), self.game_over_font, color=colors.GREEN)
                self.game_over = True
            if not self.human_ships_set:
                self.show_message_at_rect_center(
                    "YOU LOST!", (0, 0, size[0], size[1]), self.game_over_font)
                self.game_over = True
            pygame.display.update()

        while self.game_over:
            self.screen.fill(colors.WHITE, self.rect_for_messages_and_buttons)
            self.play_again_button.draw_button()
            self.play_again_button.print_message_for_button()
            self.play_again_button.change_color_on_hover()
            self.quit_game_button.draw_button()
            self.quit_game_button.change_color_on_hover()

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.quit_game_button.rect.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.play_again_button.rect.collidepoint(mouse):
                    self.__init__()
                    self.game()
            pygame.display.update()

    @staticmethod
    def get_start_block(x_start, y_start):
        """Calculates index of start block in the grid"""
        return ((x_start - left_margin) // block_size + 1,
                (y_start - upper_margin) // block_size + 1)

    @staticmethod
    def get_end_block(x_end, y_end):
        """Calculates index of end block in the grid"""
        return ((x_end - left_margin) // block_size + 1,
                (y_end - upper_margin) // block_size + 1)

    def check_if_inside_of_board(self, x_start, y_start, x_end, y_end):
        """Check if coordinates are out of board range"""
        start_block = self.get_start_block(x_start, y_start)
        end_block = self.get_end_block(x_end, y_end)
        if start_block > end_block:
            start_block, end_block = end_block, start_block
        if 15 < start_block[0] < 26 and 0 < start_block[1] < 11 and 15 < end_block[0] < 26 \
                and 0 < end_block[1] < 11:
            return True
        else:
            return False

    def computer_shoots(self, set_to_shoot_from):
        """Randomly chooses a block from available to shoot from set"""
        computer_fired_block = random.choice(tuple(set_to_shoot_from))
        self.computer_available_to_fire_set.discard(computer_fired_block)
        return computer_fired_block

    def check_hit_or_miss(self, fired_block, opponents_ships_list, computer_turn,
                          opponents_ships_list_original_copy, opponents_ships_set):
        """
        Checks whether the block that was shot at either by computer or by human is a hit or a miss.
        Update sets with dots (in missed blocks or in diagonal blocks around hit block) and 'X's
        (in hit blocks).
        Removes destroyed ships from the list of ships.
        """
        if not computer_turn:
            for elem in set.union(self.hit_blocks, self.dotted_set):
                if elem == fired_block:
                    return None
        for elem in opponents_ships_list:
            diagonal_only = True
            if fired_block in elem:
                # This is to put dots before and after a destroyed ship
                # and to draw computer's destroyed ships (which are hidden until destroyed)
                ind = opponents_ships_list.index(elem)
                if len(elem) == 1:
                    diagonal_only = False
                self.update_dotted_and_hit_sets(
                    fired_block, computer_turn, diagonal_only)
                elem.remove(fired_block)
                # This is to check who loses - if ships_set is empty
                opponents_ships_set.discard(fired_block)
                if computer_turn:
                    self.last_hits_list.append(fired_block)
                    self.update_around_last_computer_hit(fired_block, True)
                # If the ship is destroyed
                if not elem:
                    self.update_destroyed_ships(
                        ind, computer_turn, opponents_ships_list_original_copy)
                    if computer_turn:
                        self.last_hits_list.clear()
                        self.around_last_computer_hit_set.clear()
                    else:
                        # Add computer's destroyed ship to the list to draw it (computer ships are hidden)
                        self.destroyed_computer_ships.append(self.computer.ships[ind])
                return True
        self.add_missed_block_to_dotted_set(fired_block)
        if computer_turn:
            self.update_around_last_computer_hit(fired_block, False)
        return False

    def update_destroyed_ships(self, ind, computer_turn, opponents_ships_list_original_copy):
        """
        Adds blocks before and after a ship to dotted_set to draw dots on them.
        Adds all blocks in a ship to hit_blocks set to draw 'X's within a destroyed ship.
        """
        ship = sorted(opponents_ships_list_original_copy[ind])
        for i in range(-1, 1):
            self.update_dotted_and_hit_sets(ship[i], computer_turn, False)

    def update_around_last_computer_hit(self, fired_block, computer_hits):
        """
        Updates around_last_computer_hit_set (which is used to choose for computer to fire from) if it
        hit the ship but not destroyed it. Adds to this set vertical or horizontal blocks around the
        block that was last hit. Then removes those block from that set which were shot at but missed.
        around_last_computer_hit_set makes computer choose the right blocks to quickly destroy the ship
        instead of just randomly shooting at completely random blocks.
        """
        if computer_hits and fired_block in self.around_last_computer_hit_set:
            self.around_last_computer_hit_set = self.computer_hits_twice()
        elif computer_hits and fired_block not in self.around_last_computer_hit_set:
            self.computer_first_hit(fired_block)
        elif not computer_hits:
            self.around_last_computer_hit_set.discard(fired_block)

        self.around_last_computer_hit_set -= self.dotted_set_for_computer_not_to_shoot
        self.around_last_computer_hit_set -= self.hit_blocks_for_computer_not_to_shoot
        self.computer_available_to_fire_set -= self.around_last_computer_hit_set
        self.computer_available_to_fire_set -= self.dotted_set_for_computer_not_to_shoot

    def computer_first_hit(self, fired_block):
        """
        Adds blocks above, below, to the right and to the left from the block hit
        by computer to a temporary set for computer to choose its next shot from.
        Args:
            fired_block (tuple): coordinates of a block hit by computer
        """
        x_hit, y_hit = fired_block
        if x_hit > 16:
            self.around_last_computer_hit_set.add((x_hit - 1, y_hit))
        if x_hit < 25:
            self.around_last_computer_hit_set.add((x_hit + 1, y_hit))
        if y_hit > 1:
            self.around_last_computer_hit_set.add((x_hit, y_hit - 1))
        if y_hit < 10:
            self.around_last_computer_hit_set.add((x_hit, y_hit + 1))

    def computer_hits_twice(self):
        """
        Adds blocks before and after two or more blocks of a ship to a temporary list
        for computer to finish the ship faster.
        Returns:
            set: temporary set of blocks where potentially a human ship should be
            for computer to shoot from
        """
        self.last_hits_list.sort()
        new_around_last_hit_set = set()
        for i in range(len(self.last_hits_list) - 1):
            x1 = self.last_hits_list[i][0]
            x2 = self.last_hits_list[i + 1][0]
            y1 = self.last_hits_list[i][1]
            y2 = self.last_hits_list[i + 1][1]
            if x1 == x2:
                if y1 > 1:
                    new_around_last_hit_set.add((x1, y1 - 1))
                if y2 < 10:
                    new_around_last_hit_set.add((x1, y2 + 1))
            elif y1 == y2:
                if x1 > 16:
                    new_around_last_hit_set.add((x1 - 1, y1))
                if x2 < 25:
                    new_around_last_hit_set.add((x2 + 1, y1))
        return new_around_last_hit_set

    def update_dotted_and_hit_sets(self, fired_block, computer_turn, diagonal_only=True):
        """
        Puts dots in center of diagonal or all around a block that was hit (either by human or
        by computer). Adds all diagonal blocks or all-around chosen block to a separate set
        block: hit block (tuple)
        """
        x, y = fired_block
        a = 15 * computer_turn
        b = 11 + 15 * computer_turn
        # Adds a block hit by computer to the set of his hits to later remove
        # them from the set of blocks available for it to shoot from
        self.hit_blocks_for_computer_not_to_shoot.add(fired_block)
        # Add hit blocks on either grid1 (x:1-10) or grid2 (x:16-25)
        self.hit_blocks.add(fired_block)
        # Add blocks in diagonal or all-around a block to respective sets
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not diagonal_only or i != 0 and j != 0) and a < x + i < b and 0 < y + j < 11:
                    self.add_missed_block_to_dotted_set((x + i, y + j))
        self.dotted_set -= self.hit_blocks

    def add_missed_block_to_dotted_set(self, fired_block):
        """
        Adds a fired_block to the set of missed shots (if fired_block is a miss then) to then draw dots on them.
        Also needed for computer to remove these dotted blocks from the set of available blocks for it to shoot from.
        """
        self.dotted_set.add(fired_block)
        self.dotted_set_for_computer_not_to_shoot.add(fired_block)

    # ===========DRAWING SECTION==============
    def draw_ships(self, ships_coordinates_list):
        """
        Draws rectangles around the blocks that are occupied by a ship
        Args:
            ships_coordinates_list (list of tuples): a list of ships' coordinates
        """
        for elem in ships_coordinates_list:
            ship = sorted(elem)
            x_start = ship[0][0]
            y_start = ship[0][1]
            # Horizontal and 1block ships
            ship_width = block_size * len(ship)
            ship_height = block_size
            # Vertical ships
            if len(ship) > 1 and ship[0][0] == ship[1][0]:
                ship_width, ship_height = ship_height, ship_width
            x = block_size * (x_start - 1) + left_margin
            y = block_size * (y_start - 1) + upper_margin
            pygame.draw.rect(
                self.screen, colors.BLACK, ((x, y), (ship_width, ship_height)), width=block_size // 10)

    def draw_from_dotted_set(self, dotted_set_to_draw_from):
        """
        Draws dots in the center of all blocks in the dotted_set
        """
        for elem in dotted_set_to_draw_from:
            pygame.draw.circle(self.screen, colors.BLACK, (block_size * (
                    elem[0] - 0.5) + left_margin, block_size * (elem[1] - 0.5) + upper_margin), block_size // 6)

    def draw_hit_blocks(self, hit_blocks_to_draw_from):
        """
        Draws 'X' in the blocks that were successfully hit either by computer or by human
        """
        for block in hit_blocks_to_draw_from:
            x1 = block_size * (block[0] - 1) + left_margin
            y1 = block_size * (block[1] - 1) + upper_margin
            pygame.draw.line(self.screen, colors.BLACK, (x1, y1),
                             (x1 + block_size, y1 + block_size), block_size // 6)
            pygame.draw.line(self.screen, colors.BLACK, (x1, y1 + block_size),
                             (x1 + block_size, y1), block_size // 6)

    def show_message_at_rect_center(self, message, rect, which_font=font, color=colors.RED):
        """
        Prints message to screen at a given rectangle's center.
        Args:
            message (str): Message to print
            rect (tuple): rectangle in (x_start, y_start, width, height) format
            which_font (pygame font object, optional): What font to use to print message. Defaults to font.
            color (tuple, optional): Color of the message. Defaults to RED.
        """
        message_width, message_height = which_font.size(message)
        message_rect = pygame.Rect(rect)
        x_start = message_rect.centerx - message_width / 2
        y_start = message_rect.centery - message_height / 2
        background_rect = pygame.Rect(
            x_start - block_size / 2, y_start, message_width + block_size, message_height)
        message_to_blit = which_font.render(message, True, color)
        self.screen.fill(colors.WHITE, background_rect)
        self.screen.blit(message_to_blit, (x_start, y_start))

    @staticmethod
    def ship_is_valid(ship_set, blocks_for_manual_drawing):
        """
        Checks if ship is not touching other ships
        Args:
            ship_set (set): Set with tuples of new ships' coordinates
            blocks_for_manual_drawing (set): Set with all used blocks for other ships, including all blocks around ships

        Returns:
            Bool: True if ships are not touching, False otherwise.
        """
        return ship_set.isdisjoint(blocks_for_manual_drawing)

    @staticmethod
    def check_ships_numbers(ship, num_ships_list):
        """
        Checks if a ship of particular length (1-4) does not exceed necessary quantity (4-1).

        Args:
            ship (list): List with new ships' coordinates
            num_ships_list (list): List with numbers of particular ships on respective indexes.

        Returns:
            Bool: True if the number of ships of particular length is not greater than needed,
                False if there are enough of such ships.
        """
        return (5 - len(ship)) > num_ships_list[len(ship) - 1]

    @staticmethod
    def update_used_blocks(ship, method):
        for block in ship:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    method((block[0] + i, block[1] + j))


if __name__ == "__main__":
    main = Main()
    main.game()
