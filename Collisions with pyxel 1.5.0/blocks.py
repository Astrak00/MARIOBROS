from floor import Floor
from platforms import Platforms
from pipe import Pipes
from question_blocks import QuestionBlocks
from coins import Coin


class Blocks:
    def __init__(self):
        self.coins = Coin(0, 0)
        self.drawmushroom = False
        self.col_tiles = [(4, 14), (5, 14), (4, 15), (5, 15), (2, 2), (3, 2), (2, 3), (3, 3), (2, 0), (3, 0), (2, 1),
                          (3, 1), (0, 2), (1, 2), (0, 3), (1, 3), (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2)
                          , (7, 2)]
        self.underworld_col_tiles = [(0, 2), (1, 2), (0, 3), (1, 3),  # Bricks
                                     (2, 0), (3, 1), (2, 1), (3, 1),  # Question Block
                                     (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2), (7, 2), #Pipes
                                     (2, 6), (3, 6), (2, 7), (3, 7),  # Diagonal_block
                                     (4, 14), (5, 14), (4, 15), (5, 15)]  # Floor
        self.coins_tiles = self.coins.tile_coins
        self.underworld_coins_tiles = self.coins.underworld_coins_tile


        self.floor_list = []
        for i in range(143 + 1):
            self.floor_list.append(Floor(i * 8, 31 * 8))
            # We have to multiply everything by 8 because the data provided by Isa is from the tile map, which is made
            # up of 8x8 squares
        for i in range(148, 225 + 1):
            self.floor_list.append(Floor((i + 148) * 8, 31 * 8))
        # These are the question block positions on the map, by default, they have a coin in their interior
        self.question_block_list = [QuestionBlocks(29 * 8, 23 * 8, "coin"), QuestionBlocks(44 * 8, 15 * 8,"coin"),
                                    QuestionBlocks(42 * 8, 23 * 8, 'mushroom'), QuestionBlocks(43 * 8, 25 * 8),
                                    QuestionBlocks(46 * 8, 23 * 8), QuestionBlocks(47 * 8, 25 * 8),
                                    QuestionBlocks(86 * 8, 23 * 8), QuestionBlocks(87 * 8, 25 * 8),
                                    QuestionBlocks(90 * 8, 23 * 8),
                                    QuestionBlocks(114 * 8, 23 * 8), QuestionBlocks(115 * 8, 25 * 8),
                                    QuestionBlocks(162 * 8, 23 * 8, 'mushroom'), QuestionBlocks(163 * 8, 25 * 8),
                                    QuestionBlocks(202 * 8, 15 * 8), QuestionBlocks(203 * 8, 15 * 8),
                                    QuestionBlocks(221 * 8, 23 * 8), QuestionBlocks(222 * 8, 25 * 8),
                                    QuestionBlocks(227 * 8, 23 * 8), QuestionBlocks(228 * 8, 25 * 8),
                                    QuestionBlocks(221 * 8, 15 * 8), QuestionBlocks(222 * 8, 15 * 8)]

        self.platform_list = [Platforms(29 * 8, 23 * 8), Platforms(30 * 8, 23 * 8), Platforms(44 * 8, 15 * 8),
                              Platforms(45 * 8, 15 * 8), Platforms(202 * 8, 23 * 8), Platforms(202 * 8, 23 * 8),
                              Platforms(221 * 8, 15 * 8), Platforms(222 * 8, 15 * 8), Platforms(221 * 8, 23 * 8),
                              Platforms(222 * 8, 23 * 8), Platforms(227 * 8, 23 * 8), Platforms(228 * 8, 23 * 8),
                              Platforms(236 * 8, 29 * 8), Platforms(237 * 8, 29 * 8), Platforms(238 * 8, 27 * 8),
                              Platforms(239 * 8, 27 * 8), Platforms(240 * 8, 25 * 8), Platforms(241 * 8, 25 * 8),
                              Platforms(90 * 8, 23 * 8), Platforms(91 * 8, 23 * 8), Platforms(114 * 8, 23 * 8),
                              Platforms(115 * 8, 23 * 8)]

        for i in range(40, 48 + 1):
            self.platform_list.append(Platforms(i * 8, 23 * 8))
        for i in range(160, 165 + 1):
            self.platform_list.append(Platforms(i * 8, 23 * 8))
        for i in range(168, 187 + 1):
            self.platform_list.append(Platforms(i * 8, 15 * 8))
        for i in range(196, 203 + 1):
            self.platform_list.append(Platforms(i * 8, 15 * 8))
        for i in range(210, 213 + 1):
            self.platform_list.append(Platforms(i * 8, 23 * 8))

        self.pipes_list = []
        for i in range(56, 59 + 1):
            self.pipes_list.append(Pipes(i * 8, 27 * 8))
        for i in range(72, 75 + 1):
            self.pipes_list.append(Pipes(i * 8, 23 * 8))
        for i in range(96, 99 + 1):
            self.pipes_list.append(Pipes(i * 8, 20 * 8))
        for i in range(120, 123 + 1):
            self.pipes_list.append(Pipes(i * 8, 20 * 8))

        self.pfp_list = []
        self.pfp_list.append(self.floor_list)
        self.pfp_list.append(self.platform_list)
        self.pfp_list.append(self.pipes_list)

        self.sniper_tile = (4, 29)



