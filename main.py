import random
import string
import tkinter as tk
from tkinter import messagebox

def get_random_letter() -> str:
    return random.choice(string.ascii_lowercase)

def load_word_list(filepath: str) -> set:
    with open(filepath, 'r', encoding='utf-8') as file:
        words = {line.strip().lower() for line in file}
    return words

def is_valid_word(word: str, word_list: set) -> bool:
    return word in word_list

class LetterGame:
    def __init__(self, root, word_list):
        self.root = root
        self.word_list = word_list
        self.original_word_list = word_list.copy()
        self.current_word = get_random_letter()
        self.turn = 0
        self.players = ["Joueur 1", "Joueur 2"]

        self.root.title("Jeu de Lettres")
        self.root.geometry("600x600")

        self.label = tk.Label(root, text="Bienvenue dans le jeu de lettres !", font=('Helvetica', 14, 'bold'))
        self.label.pack(pady=10)

        self.word_label = tk.Label(root, text=f"Lettre initiale : {self.current_word}", font=('Helvetica', 12))
        self.word_label.pack(pady=10)

        self.turn_label = tk.Label(root, text=f"{self.players[self.turn % 2]}, c'est à vous.", font=('Helvetica', 12))
        self.turn_label.pack(pady=10)

        self.info_text = tk.Text(root, height=10, width=50, state='disabled', font=('Helvetica', 12))
        self.info_text.pack(pady=10)

        self.keyboard_frame = tk.Frame(root)
        self.keyboard_frame.pack(pady=10)

        letters = string.ascii_lowercase + 'àâäéèêëîïôöùûüç'
        for i, letter in enumerate(letters):
            button = tk.Button(self.keyboard_frame, text=letter, command=lambda l=letter: self.add_letter(l), width=4, height=2, font=('Helvetica', 12))
            button.grid(row=i // 13, column=i % 13, padx=5, pady=5)

        self.restart_button = tk.Button(root, text="Recommencer", command=self.restart_game, font=('Helvetica', 12), bg='lightblue')
        self.restart_button.pack(pady=10)

        self.show_words_button = tk.Button(root, text="Voir les mots disponibles", command=self.show_available_words, font=('Helvetica', 12), bg='lightgreen')
        self.show_words_button.pack(pady=10)

    def add_letter(self, letter):
        self.current_word += letter
        self.word_label.config(text=f"Mot actuel : {self.current_word}")

        if is_valid_word(self.current_word, self.word_list):
            self.update_info(f"{self.players[self.turn % 2]} a complété un mot valide : {self.current_word}, mais le jeu continue !")

        self.word_list = {word for word in self.word_list if word.startswith(self.current_word)}

        if len(self.word_list) == 1:
            self.update_info(f"{self.players[(self.turn + 1) % 2]} gagne car il ne reste qu'un seul mot possible : {list(self.word_list)[0]}")
            self.disable_buttons()
            return

        if not self.word_list:
            self.update_info(f"{self.players[self.turn % 2]} a formé un mot non possible : {self.current_word}. {self.players[(self.turn + 1) % 2]} gagne !")
            self.disable_buttons()
            return

        self.turn += 1
        self.turn_label.config(text=f"{self.players[self.turn % 2]}, c'est à vous.")

    def disable_buttons(self):
        for widget in self.keyboard_frame.winfo_children():
            widget.config(state="disabled")

    def restart_game(self):
        self.word_list = self.original_word_list.copy()
        self.current_word = get_random_letter()
        self.turn = 0
        self.word_label.config(text=f"Lettre initiale : {self.current_word}")
        self.turn_label.config(text=f"{self.players[self.turn % 2]}, c'est à vous.")
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state='disabled')
        for widget in self.keyboard_frame.winfo_children():
            widget.config(state="normal")

    def show_available_words(self):
        words = ', '.join(sorted(self.word_list)[:10])
        self.update_info(f"Mots disponibles (max 10): {words}")

    def update_info(self, message):
        self.info_text.config(state='normal')
        self.info_text.insert(tk.END, message + '\n')
        self.info_text.config(state='disabled')

def main():
    word_list = load_word_list('french.txt')

    root = tk.Tk()
    game = LetterGame(root, word_list)
    root.mainloop()

if __name__ == "__main__":
    main()
