import tkinter as tk
from tkinter import messagebox

quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "What is the largest planet in the solar system?",
        "options": ["Earth", "Jupiter", "Mars", "Saturn"],
        "answer": "Jupiter"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Leonardo da Vinci", "Picasso", "Michelangelo"],
        "answer": "Leonardo da Vinci"
    }
]

class MiniQuiz:
    def __init__(self, master):
        self.master = master
        self.master.title("Mini Quiz Trivia")
        self.master.geometry("400x300")
        
        self.points = 0
        self.index = 0
        
        self.question_label = tk.Label(master, text="", wraplength=380, font=("Arial", 14))
        self.question_label.pack(pady=20)
        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(master, text="", width=20, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.option_buttons.append(btn)
        
        self.next_question()
    
    def next_question(self):
        if self.index < len(quiz_data):
            self.question_label.config(text=quiz_data[self.index]["question"])
            for i, option in enumerate(quiz_data[self.index]["options"]):
                self.option_buttons[i].config(text=option)
        else:
            messagebox.showinfo("End of Quiz", f"You got {self.points} out of {len(quiz_data)} right!")
            self.master.destroy()
    
    def check_answer(self, i):
        selected = self.option_buttons[i].cget("text")
        correct = quiz_data[self.index]["answer"]
        if selected == correct:
            self.points += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror("Wrong!", f"The correct answer was: {correct}")
        self.index += 1
        self.next_question()


def main():
    root = tk.Tk()
    app = MiniQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()
