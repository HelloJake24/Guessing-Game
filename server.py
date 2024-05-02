import socket
import random

host = ""
port = 7777
banner = """
====GUESING GAME====
\nEnter Guess: """

# Dictionary to store user scores
leaderboard = {"easy": [], "medium": [], "hard": []}

def gen_random():
    return random.randint(1, 50)

def inter_random():
    return random.randint(1, 100)

def hard_random():
    return random.randint(1, 150)

def update_leaderboard(username, score, difficulty):
    leaderboard[difficulty].append({"username": username, "score": score})

def display_leaderboard():
    print("Leaderboard:")
    for difficulty, scores in leaderboard.items():
        print(f"\nDifficulty: {difficulty}")
        scores = sorted(scores, key=lambda x: x['score'])
        for idx, entry in enumerate(scores, 1):
            print(f"{idx}. {entry['username']} - {entry['score']} tries")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")

username = None
difficulty = None
while True:
    conn, addr = s.accept()
    print(f"New client: {addr[0]}")

    while True:  # Loop for each game

        # Get username
        if username is None:
            conn.sendall(b"""
                         \nEnter your username: """)
            username = conn.recv(1024).decode().strip()

        while True:  # Loop until a valid choice is made
            conn.sendall(b"Difficulty levels:\n1. Easy:1-50\n2. Medium:1-100\n3. Hard:1-150\nEnter your diffiiculty: ")
            choice = conn.recv(1024).decode().strip()
            if choice in ["1", "2", "3"]:
                break
            else:
                conn.sendall(b"Invalid choice. Please press Enter to select again and choose 1, 2, or 3.")

        if choice == "1":
            difficulty = "easy"
            guessme = guessme = gen_random()
        elif choice == "2":
            difficulty = "medium"
            guessme = inter_random()
        elif choice == "3":
            difficulty = "hard"
            guessme = hard_random()

        conn.sendall(banner.encode())
        attempts = 0

        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            attempts += 1
            print(f"{username} guess attempt: {guess}")

            if guess == guessme:
                update_leaderboard(username, attempts, difficulty)
                conn.sendall(f"Guessed Correctly in {attempts} tries!".encode())
                display_leaderboard()
                username = None
                difficulty = None
                break
            elif guess > guessme:
                conn.sendall(b"***Hint: Guess Lower*** \nEnter Guess: ")
            elif guess < guessme:
                conn.sendall(b"***Hint: Guess Higher*** \nEnter Guess: ")

s.close()
