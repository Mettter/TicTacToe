from tkinter import messagebox

import gevent
import zerorpc


class GameClient:
    client = zerorpc.Client(timeout=2)
    is_host = False
    game_window = None
    game_buttons = None
    board = []

    def __init__(self, root):
        self.game_window = root

    def connect(self, ip, room_id):
        self.client.connect(f"tcp://{ip}:{room_id}")

    def start_server_room(self, ip, room_id, server):
        s = zerorpc.Server(server)
        s.bind(f"tcp://{ip}:{room_id}")
        self.is_host = True
        gevent.spawn(s.run)

    def make_move(self, value):
        move = self.client.rpc_make_move(
            value,
            self.is_host
        )
        if not move:
            messagebox.showwarning(
                "Enemy turn",
                "It is not your turn"
            )
        if move == -1:
            messagebox.showwarning(
                "Incorrect field",
                "Space occupied!"
            )

    def set_points(self):
        marks = {
            0: "O",
            1: "X",
            -1: " "
        }
        for i in range(len(self.board)):
            mark = marks.get(self.board[i])
            self.game_buttons[i].config(text=mark)

    def refresh_board(self):
        self.board = self.client.get_board()
        gevent.sleep(0.025)
        self.set_points()
        active_player = self.client.rpc_get_active_player()
        if active_player == self.is_host:
            self.game_window.title("Your turn")
        else:
            self.game_window.title("Enemy turn")
        self.game_window.after(50, self.refresh_board)