from movie_expert_view import MovieExpertView
from movie_expert_ctrl import MovieExpertController
from movie_expert_model import MovieExpertModel
import tkinter as tk

def main():
    root = tk.Tk()
    model = MovieExpertModel()
    view = MovieExpertView(root)
    MovieExpertController(model, view)
    root.mainloop()


if __name__ == "__main__":
    main()