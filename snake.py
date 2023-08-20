import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from random import randint
move_size=20
mps=10
speed=1000//mps
class Snake(tk.Canvas):
    global btn
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.new_food()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.key_press)
        try:
            self.snake_Image = Image.open("asset/snake.png")
            self.snake = ImageTk.PhotoImage(self.snake_Image)
            self.food_image = Image.open("asset/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except:
            print("image not exist")
        self.create_text(45, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=("TkDefaultFont", 14))
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake, tag="snake")
        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")
        self.after(75, self.action)

    def move(self):
        head_x,head_y=self.snake_positions[0]
        if self.direction=="Left":
            new_head = (head_x - move_size, head_y)
        elif self.direction=="Up":
            new_head = (head_x, head_y-move_size)
        elif self.direction=="Down":
            new_head = (head_x, head_y+move_size)
        else:
            new_head=(head_x+move_size,head_y)
        self.snake_positions=[new_head]+self.snake_positions[:-1]
        for segment,position in zip(self.find_withtag("snake"),self.snake_positions):
            self.coords(segment,position)
    def action(self):
        if self.check_collision():
            self.end()
            return
        self.ck_food()
        self.move()
        self.after(speed,self.action)
    def check_collision(self):
        head_x,head_y=self.snake_positions[0]
        return(head_x in (20,600) or head_y in (20,620) or (head_x,head_y) in self.snake_positions[1:])
    def ck_food(self):
        if self.snake_positions[0]==self.food_position:
            self.score+=1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1],image=self.snake,tag="snake")
            score=self.find_withtag("score")
            self.itemconfig(score,text=f"Score: {self.score}",tag="score")
            self.food_position=self.new_food()
            self.coords(self.find_withtag("food"),self.food_position)
    def key_press(self,e):
        new_direction=e.keysym
        all_direction=("Up","Down","Right","Left")
        opp=({"Up","Down"},{"Left","Right"})
        if(new_direction in all_direction and {new_direction,self.direction} not in opp):
            self.direction=new_direction
    def new_food(self):
        while True:
            x=randint(2,29)*move_size
            y=randint(3,30)*move_size
            fp=(x,y)
            if fp not in self.snake_positions:
                return fp
    def end(self):
        self.delete(tk.ALL)
        self.create_text(self.winfo_width()/2,self.winfo_height()/2,text=f"Game Over! Your Score: {self.score}",fill="#fff",font=("TkDefaultFont",24))
        btn.pack()

def rst():
    global board,btn
    board.destroy()
    btn.destroy()
    board=Snake()
    board.pack()
    btn=Button(text="RESTART",bg="black",command=rst,foreground="white",activeforeground="blue")
root=tk.Tk()
root.title("Snake")
root.resizable(False,False)
board=Snake()
board.pack()
btn=Button(text="RESTART",bg="black",command=rst,foreground="white",activeforeground="blue")
root.mainloop()