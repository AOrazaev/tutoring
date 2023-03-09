from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class TetrisPiecePattern:
    text: str
    rgb: Tuple[int, int, int]


@dataclass
class TetrisPiece:
    x: int
    y: int
    pattern: TetrisPiecePattern


def pattern_rows(pattern: TetrisPiecePattern) -> List[str]:
    return list(x.strip() for x in pattern.text.strip('\n ').split('\n'))


def piece_height(piece: TetrisPiece) -> int:
    return len(piece.pattern.text.strip('\n ').split('\n'))


def piece_width(piece: TetrisPiece) -> int:
    return len(pattern_rows(piece.pattern)[0])


def rotate_clockwise(piece: TetrisPiece) -> TetrisPiece:
    lines = [x.strip() for x in piece.pattern.text.strip('\n ').split('\n')]
    return TetrisPiece(
        piece.x, piece.y,
        TetrisPiecePattern(
            '\n'.join(''.join(reversed(t)) for t in zip(*lines)),
            piece.pattern.rgb))


def rotate_counterclockwise(piece: TetrisPiece):
    lines = [x.strip() for x in piece.pattern.text.strip('\n ').split('\n')]
    return TetrisPiece(
        piece.x, piece.y,
        TetrisPiecePattern(
            '\n'.join(reversed(list(''.join(t) for t in zip(*lines)))),
            piece.pattern.rgb))


PATTERNS = (
    TetrisPiecePattern(
        '''
        #..
        ###
        ''',
        # yellow
        (255, 255, 0)),
    TetrisPiecePattern(
        '''
        ..#
        ###
        ''',
        # blue
        (0, 0, 255)),
    TetrisPiecePattern(
        '''
        ##
        ##
        ''',
        # red
        (255, 0, 0)),
    TetrisPiecePattern(
        '''
        ####
        ''',
        # green
        (0, 255, 0)),
    TetrisPiecePattern(
        '''
        .#.
        ###
        ''',
        # orange
        (255, 165, 0)),
    TetrisPiecePattern(
        '''
        .##
        ##.
        ''',
        # pink
        (255, 192, 203)),
    TetrisPiecePattern(
        '''
        ##.
        .##
        ''',
        # purple
        (128, 0, 128)),
)
