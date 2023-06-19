import socket
import time

SERVER_HOST = "localhost"
SERVER_PORT = 40008

# Citations
# https://www.geeksforgeeks.org/socket-programming-python/
# https://realpython.com/python-sockets/

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected with server at ({SERVER_HOST}, {SERVER_PORT})\n")
    mode = "CHAT"
    new_chat = 1  # if 1, print introduction message
    while True:
        if mode == "CHAT":
            # chatroom intro message
            if new_chat == 1:
                print(f"Welcome to the chatroom! Begin by writing your message when the input prompt appears. Then wait "
                      f"for the server's response.\nTo leave the chatroom, type '/q' in the input prompt.\nTo start a "
                      f"multiplayer game, type 'play 20 questions' in the input prompt.\n\n")
                new_chat = 0

            # sending message to server
            message = input("Enter your message here: ")
            byte_message = message.encode('utf-8')
            clientSocket.send(byte_message)
            if "/q" in message:
                print("You requested a shutdown. Shutting down!")
                time.sleep(5)
                clientSocket.close()
                break
            elif "play 20 questions" in message:
                print("You requested to play 20 questions! Redirecting...\n\n\n")
                mode = "GAME"
                question_countdown = 20
                continue

            # receiving message from server
            received = clientSocket.recv(4096)
            server_response = received.decode()
            if not server_response:
                print("The connection has been disrupted. Closing!")
                clientSocket.close()
                break
            if "/q" in server_response:
                print("Server has requested shutdown. Shutting down!")
                clientSocket.close()
                break
            elif "play 20 questions" in server_response:
                print("Server wants to play 20 Questions! Redirecting...\n\n")
                mode = "GAME"
                question_countdown = 20
                continue
            print(server_response)

        if mode == "GAME":
            while question_countdown >= 0:
                # game intro message
                if question_countdown == 20:
                    print(f"Welcome to 20 Questions! Think of a person, place, or thing and type it in the input prompt "
                          f"below.\nThe server does not know what you selected.\n"
                          f"The server will be sending you yes/no questions to try to guess your selection.\n"
                          f"If the server correctly guesses what you have chosen, type 'win' in the input prompt.\n"
                          f"Remember, you may only respond with 'yes' or 'no' or 'win' (case sensitive). Have fun!\n"
                          f"NOTE: To exit the game before its conclusion, type '/q' into the question prompt.\n"
                          f"You will then be returned to the chatroom.\n\n")
                    selection = input("Write your chosen selection (person, place, or thing) here: ")
                    print("\n")

                # receive question from server
                received = clientSocket.recv(4096)
                server_question = received.decode()
                if "/q" in server_question:
                    print("The server has requested for the game to end. Returning to chatroom...\n")
                    mode = "CHAT"
                    new_chat = 1
                    break
                print(server_question)
                question_countdown -= 1
                if question_countdown == 1:
                    print(f"The server has {question_countdown} question left.")
                else:
                    print(f"The server has {question_countdown} questions left.")

                # send answer to server
                answer = input("Answer the question with a yes, no, or win (case sensitive): ")
                print("\n")
                if "\q" in answer:
                    print("You requested for the game to end. Returning to chatroom...\n")
                    byte_answer = answer.encode('utf-8')
                    clientSocket.send(byte_answer)
                    mode = "CHAT"
                    new_chat = 1
                    break
                while answer != "yes" and answer != "no" and answer != "win":
                    print("Error! Your response must be yes, no, or win to continue.")
                    answer = input("Try again: ")
                    print("\n")
                byte_answer = answer.encode('utf-8')
                clientSocket.send(byte_answer)
                if "no" in answer and question_countdown == 0:
                    print("The game is now over! Returning to the chatroom...\n")
                    mode = "CHAT"
                    new_chat = 1
                    break
                if "win" in answer:
                    print("You reported that the server correctly guessed your selection. Game over! Returning to "
                          "chatroom...\n")
                    mode = "CHAT"
                    new_chat = 1
                    break










