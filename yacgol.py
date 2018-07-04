#!/usr/bin/env python3

import argparse
import tkinter

UNDER_POPULATION_COUNT = 2
OVER_POPULATION_COUNT = 3
REPRODUCTION_COUNT = 3


class CellButton(tkinter.Button):
    DEFAULT_COLOR = 'black'
    INVERTED_COLOR = 'white'

    def __init__(self, window, *args, **kwargs):
        super(CellButton, self).__init__(
            window,
            *args,
            command=self.flip,
            **kwargs
        )

        self.initialize()

    def initialize(self):
        self.configure(bg=self.DEFAULT_COLOR)
        self.alive = False

    def flip(self):
        if self.alive:
            self.configure(bg=self.DEFAULT_COLOR)
            self.alive = False
        else:
            self.configure(bg=self.INVERTED_COLOR)
            self.alive = True


class CellGrid:
    NEIGHBOR_COORDINATES = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
    ]

    def __init__(self, window, length, width):
        self.window = window
        self.length = length
        self.width = width

        self.cell_buttons = [
            [
                CellButton(self.window)
                for _ in range(self.length)
            ]
            for _ in range(self.width)
        ]

        self._apply_cell_buttons(
            lambda cell_button, x, y: cell_button.grid(row=y, column=x)
        )

    def _apply_cell_buttons(self, func):
        for y, row in enumerate(self.cell_buttons):
            for x, cell_button in enumerate(row):
                func(cell_button, x, y)

    def reset_cells(self):
        self._apply_cell_buttons(
            lambda cell_button, x, y: cell_button.initialize()
        )

    def neighbor_count(self, x, y):
        return sum(
            int(self.cell_buttons[(y + j) % self.width][(x + i) % self.length].alive)
            for i, j in self.NEIGHBOR_COORDINATES
        )

    def step(self):
        def add_neighbor_count(cell_button, x, y):
            cell_button.neighbor_count = self.neighbor_count(x, y)

        self._apply_cell_buttons(add_neighbor_count)

        def apply_rules(cell_button, x, y):
            if cell_button.alive and cell_button.neighbor_count < UNDER_POPULATION_COUNT:
                cell_button.flip()
            elif cell_button.alive and cell_button.neighbor_count > OVER_POPULATION_COUNT:
                cell_button.flip()
            elif not cell_button.alive and cell_button.neighbor_count == REPRODUCTION_COUNT:
                cell_button.flip()

        self._apply_cell_buttons(apply_rules)


def parse_args():
    p = argparse.ArgumentParser(description='''
        A pure Python implementation of Conway's Game of Life using Tkinter.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument(
        '-l',
        '--length',
        action='store',
        default=10,
        type=int,
        help='grid length'
    )

    p.add_argument(
        '-w',
        '--width',
        action='store',
        default=10,
        type=int,
        help='grid width'
    )

    args = p.parse_args()
    return args


def main():
    args = parse_args()

    root = tkinter.Tk()
    root.title("Conway's Game of Life")

    cell_frame = tkinter.Frame(root)
    cell_frame.pack()

    cell_grid = CellGrid(cell_frame, args.length, args.width)

    command_frame = tkinter.Frame(root)
    command_frame.pack(expand=True, fill=tkinter.BOTH)

    def step():
        cell_grid.step()

    step_button = tkinter.Button(command_frame, text='Step', command=step)
    step_button.pack(side=tkinter.TOP)

    def reset():
        cell_grid.reset_cells()

    reset_button = tkinter.Button(command_frame, text='Reset', command=reset)
    reset_button.pack(side=tkinter.TOP)

    reset_button = tkinter.Button(command_frame, text='Exit', command=root.destroy)
    reset_button.pack(side=tkinter.TOP)

    root.mainloop()


if __name__ == "__main__":
    main()
