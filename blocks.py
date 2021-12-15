from floor import Floor
from pipe import Pipes
from question_blocks import QuestionBlocks


class Blocks:

    def __init__(self):
        # This list includes all object we wanted mario to collide, but as we learned afterwards, the brick blocks can't
        # be used with this method and if we want to change the sprite of them or how the representation of the world
        # is, we have to use another method, which is also implemented in the game, but in another section
        self.col_tiles_old = [(4, 14), (5, 14), (4, 15), (5, 15), (2, 2), (3, 2), (2, 3), (3, 3), (2, 0), (3, 0), (2, 1),
                          (3, 1), (0, 2), (1, 2), (0, 3), (1, 3), (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2)
                          , (7, 2)]
        # List of tiles:
        # (4, 14), (5, 14), (4, 15), (5, 15) --> Floor, also known as cobblestone
        # (2, 2), (3, 2), (2, 3), (3, 3) --> Solid unbreakable block, (jukebox)
        # (2, 0), (3, 0), (2, 1),(3, 1) --> Question block
        # (0, 2), (1, 2), (0, 3), (1, 3) --> Brick Blocks
        # (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2), (7, 2) --> Pipes

        self.col_tiles = [(4, 14), (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (5, 1), (6, 1), (7, 1), (4, 2), (5, 2),
                          (6, 2), (7, 2), (4, 3), (5, 3), (6, 3), (7, 3), (2, 2), (3, 2), (2, 3), (3, 3)]
        # List of tiles that actually collide with the mario
        # (4, 14), (5, 14), (4, 15), (5, 15) --> Floor, also known as cobblestone
        # (2, 2), (3, 2), (2, 3), (3, 3) --> Solid unbreakable block, (jukebox)
        # (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2), (7, 2) --> Pipes

        # This list was created in case we needed to modify the floor, before we discovered the other method of
        # collisions, but every block is its own object.
        self.floor_list = []
        # THis is the first half of the scenery, as there is a gap in the floor, we have to create two ranges.
        for i in range(143 + 1):
            self.floor_list.append(Floor(i * 8, 31 * 8))
            # We have to multiply everything by 8 because the data provided by Isa is from the tile map, which is made
            # up of 8x8 squares
        # This is the second list of blocks in the floor
        for i in range(148, 225 + 1):
            self.floor_list.append(Floor((i + 148) * 8, 31 * 8))

        # We have created a list with all the blocks that will appear in the map. They are named "question blocks",
        # but actually the question blocks are only those that contain coins or mushrooms, the rest of blocks are
        # breakable blocks:
        self.question_block_list = [QuestionBlocks(44 * 8, 15 * 8, "coins"), QuestionBlocks(42 * 8, 23 * 8, "mushroom"),
                                    QuestionBlocks(86 * 8, 23 * 8), QuestionBlocks(90 * 8, 23 * 8),
                                    QuestionBlocks(114 * 8, 23 * 8), QuestionBlocks(162 * 8, 23 * 8, "mushroom"),
                                    QuestionBlocks(202 * 8, 15 * 8), QuestionBlocks(221 * 8, 23 * 8),
                                    QuestionBlocks(227 * 8, 23 * 8)]

        # Here we are appending to the list of question blocks some other blocks that are next to one other, so
        # it was easier to append them with loops as they have similar coordinates:
        for i in range(32, 40 + 1, 2):
            self.question_block_list.append(QuestionBlocks(i * 8, 23 * 8))
        for i in range(160, 165 + 1, 2):
            self.question_block_list.append(QuestionBlocks(i * 8, 23 * 8))
        for i in range(168, 187 + 1, 2):
            self.question_block_list.append(QuestionBlocks(i * 8, 15 * 8))
        for i in range(196, 203 + 1, 2):
            self.question_block_list.append(QuestionBlocks(i * 8, 15 * 8))
        for i in range(210, 213 + 1, 2):
            self.question_block_list.append(QuestionBlocks(i * 8, 23 * 8))

        # We do the same thing here but with pipes:
        self.pipes_list = []
        for i in range(56, 59 + 1):
            self.pipes_list.append(Pipes(i * 8, 27 * 8))
        for i in range(72, 75 + 1):
            self.pipes_list.append(Pipes(i * 8, 23 * 8))
        for i in range(96, 99 + 1):
            self.pipes_list.append(Pipes(i * 8, 20 * 8))
        for i in range(120, 123 + 1):
            self.pipes_list.append(Pipes(i * 8, 20 * 8))

        # This list is the combined list of all object of every block of the floor and pipes
        self.pfp_list = []
        for i in self.floor_list:
            self.pfp_list.append(i)

        for j in self.pipes_list:
            self.pfp_list.append(j)

        for k in self.question_block_list:
            self.pfp_list.append(k)

        """self.pfp_list.append(self.floor_list)
        self.pfp_list.append(self.pipes_list)
        self.pfp_list.append(self.question_block_list)
"""