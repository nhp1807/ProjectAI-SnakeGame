from tkinter import *
from PIL import ImageTk, Image
import agent
import agent2
import snake_game_human

root = Tk()
background_color = '#44546A'
text_color = '#E4D8B4'
text_size = 20

# Adjust size
root.geometry("818x516")
root.title('Snake game')
# Add image file
bg = PhotoImage(file="image/SnakeGameBG.png")

# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

# Set button action
def play_as_human():
    snake_game_human.SnakeGame.start_game()

def start_training():
    agent2.train()

def start_training_with_barrier():
    agent.train()

# Add buttons
button1 = Button(root, text="1. Play as human", bg=background_color, fg=text_color, font= ('Arial', text_size, 'bold'), 
                highlightthickness = 0, bd = 0, activebackground=background_color, command=play_as_human)
button1.place(x=178, y=228)

button2 = Button(root, text="2. Start training", bg=background_color, fg=text_color, font= ('Arial', text_size, 'bold'), 
                highlightthickness = 0, bd = 0, activebackground=background_color, command=start_training)
button2.place(x=178, y=317)

button3 = Button(root, text="3. Start training with barrier", bg=background_color, fg=text_color, font= ('Arial', text_size, 'bold'), 
                highlightthickness = 0, bd = 0, activebackground=background_color, command=start_training_with_barrier)
button3.place(x=178, y=406)


# Execute tkinter
root.mainloop()
