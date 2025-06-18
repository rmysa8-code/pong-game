# -- coding: utf-8 --
import turtle
import time

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
win = turtle.Screen()
win.title("Pong Game - Rümeysa'nın Projesi")
win.bgcolor("black")
win.setup(width=WIDTH, height=HEIGHT)
win.tracer(0)

# Başlangıç menüsü
menu = turtle.Turtle()
menu.color("white")
menu.penup()
menu.hideturtle()
menu.write("🎮 Pong Oyununa Hoş Geldin!\nBaşlamak için ENTER'a bas 🎯", align="center", font=("Courier", 24, "normal"))

# Paddle sınıfı
class Paddle(turtle.Turtle):
    def _init_(self, position):
        super()._init_()
        self.shape("square")
        self.color("white")
        self.length = 5
        self.shapesize(stretch_wid=self.length, stretch_len=1)
        self.penup()
        self.goto(position)
        self.speed(0)

    def move_up(self):
        y = self.ycor()
        y += 20
        if y < HEIGHT // 2 - 50:
            self.sety(y)

    def move_down(self):
        y = self.ycor()
        y -= 20
        if y > -HEIGHT // 2 + 50:
            self.sety(y)

    def shrink(self):
        if self.length > 2:
            self.length -= 0.5
            self.shapesize(stretch_wid=self.length, stretch_len=1)

# Ball sınıfı
class Ball(turtle.Turtle):
    def _init_(self):
        super()._init_()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.speed(0)
        self.dx = 0.2
        self.dy = 0.2

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_y(self):
        self.dy *= -1

    def bounce_x(self):
        self.dx *= -1.1  # Zorluk artışı: hızlanır

    def reset_position(self):
        self.goto(0, 0)
        self.dx = 0.2 * (-1 if self.dx > 0 else 1)
        self.dy = 0.2

# ScoreBoard sınıfı
class ScoreBoard(turtle.Turtle):
    def _init_(self):
        super()._init_()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, HEIGHT // 2 - 40)
        self.score_left = 0
        self.score_right = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"{self.score_left} : {self.score_right}", align="center", font=("Courier", 24, "normal"))

    def left_scores(self):
        self.score_left += 1
        self.update_score()

    def right_scores(self):
        self.score_right += 1
        self.update_score()

# Game sınıfı
class Game:
    def _init_(self):
        self.paddle_left = Paddle((-WIDTH // 2 + 50, 0))
        self.paddle_right = Paddle((WIDTH // 2 - 50, 0))
        self.ball = Ball()
        self.scoreboard = ScoreBoard()
        self.running = True
        self.winner = None

    def setup_controls(self):
        win.listen()
        win.onkeypress(self.paddle_left.move_up, "w")
        win.onkeypress(self.paddle_left.move_down, "s")
        win.onkeypress(self.paddle_right.move_up, "1")
        win.onkeypress(self.paddle_right.move_down, "4")

    def check_collisions(self):
        if self.ball.ycor() > HEIGHT // 2 - 10 or self.ball.ycor() < -HEIGHT // 2 + 10:
            self.ball.bounce_y()

        if (self.ball.xcor() > WIDTH // 2 - 70 and
            self.paddle_right.ycor() - 50 < self.ball.ycor() < self.paddle_right.ycor() + 50):
            self.ball.bounce_x()

        if (self.ball.xcor() < -WIDTH // 2 + 70 and
            self.paddle_left.ycor() - 50 < self.ball.ycor() < self.paddle_left.ycor() + 50):
            self.ball.bounce_x()

        if self.ball.xcor() > WIDTH // 2:
            self.scoreboard.left_scores()
            self.ball.reset_position()
            if self.scoreboard.score_left % 2 == 0:
                self.paddle_right.shrink()

        if self.ball.xcor() < -WIDTH // 2:
            self.scoreboard.right_scores()
            self.ball.reset_position()
            if self.scoreboard.score_right % 2 == 0:
                self.paddle_left.shrink()

    def check_winner(self):
        if self.scoreboard.score_left >= 5:
            self.winner = "Sol Oyuncu (W/S)"
            return True
        elif self.scoreboard.score_right >= 5:
            self.winner = "Sağ Oyuncu (1/4)"
            return True
        return False

    def show_winner(self):
        self.scoreboard.goto(0, 0)
        self.scoreboard.write(f"{self.winner} Kazandı!", align="center", font=("Courier", 36, "bold"))

    def run(self):
        self.setup_controls()
        while self.running:
            win.update()
            self.ball.move()
            self.check_collisions()

            if self.check_winner():
                self.show_winner()
                self.running = False

            time.sleep(0.01)

# Oyunu başlat
def start_game():
    menu.clear()
    win.update()
    game = Game()
    game.run()

win.listen()
win.onkeypress(start_game, "Return")
win.mainloop()