from . import api_v2 as client
from .entities import Board, MondayClientCredentials
from .enums import BoardKind

def create_board(creds: MondayClientCredentials, board_name: str, board_kind: BoardKind, *argv):

    board_data = client.create_board(
            creds.api_key_v2, 
            board_name, 
            board_kind, 
            *argv)

    return Board(creds=creds, **board_data)