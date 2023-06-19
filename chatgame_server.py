import socket


HOST = "localhost"
PORT = 40008


# Citations
# https://www.geeksforgeeks.org/taking-input-in-python/

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    connSocket, addr = serverSocket.accept()
    with connSocket:
        mode = "CHAT"
        new_chat = 1        # if 1, print introduction message
        print(f"Connected by ({HOST}, {PORT})\n")
        while True:
            if mode == "CHAT":

                # chatroom intro message
                if new_chat == 1:
                    print(f"Welcome to the chatroom! You will receive messages from the client. You can enter your response when "
                        f"the input prompt appears.\nTo leave the chatroom, type '/q' in the input prompt.\nTo start a multiplayer "
                        f"game, type 'play 20 questions' in the input prompt.\n\n")
                    new_chat = 0

                # receive message from client
                received = connSocket.recv(4096)
                client_msg = received.decode()
                if not client_msg:  # check this
                    print("The connection has been disrupted. Closing!")
                    connSocket.close()
                    serverSocket.close()
                    break
                if "/q" in client_msg:
                    print("Client has requested shutdown. Shutting down!")
                    connSocket.close()
                    serverSocket.close()
                    break
                elif "play 20 questions" in client_msg:
                    print("Client wants to play 20 Questions! Redirecting...\n\n")
                    mode = "GAME"
                    question_countdown = 20
                    continue
                print(client_msg)

                # send response to client
                response = input("Enter your response here: ")
                byte_response = response.encode('utf-8')
                connSocket.send(byte_response)
                if "/q" in response:
                    print("You requested a shutdown. Shutting down!")
                    connSocket.close()
                    serverSocket.close()
                    break
                elif "play 20 questions" in response:
                    print("You requested to play 20 questions! Redirecting...\n\n")
                    mode = "GAME"
                    question_countdown = 20
                    continue

            if mode == "GAME":
                while question_countdown >= 1:

                    # game intro message
                    if question_countdown == 20:
                        print(f"Welcome to 20 Questions! The client will select a person, place, or thing.\n"
                              f"You must deduce what the client has chosen by asking a maximum of 20 questions.\n"
                              f"The client is only able to respond to your questions with a yes or no. Good luck!\n"
                              f"NOTE: To exit the game before its conclusion, type '/q' into the question prompt.\n"
                              f"You will then be returned to the chatroom.\n\n")
                    if question_countdown == 1:
                        print(f"You have {question_countdown} question left. You better make your best guess!")
                    else:
                        print(f"You have {question_countdown} questions left.")

                    # send question to client
                    question = input("Ask your yes/no question here: ")
                    if "/q" in question:
                        print("You requested for the game to end. Returning to chatroom...\n")
                        byte_question = question.encode('utf-8')
                        connSocket.send(byte_question)
                        mode = "CHAT"
                        new_chat = 1
                        break
                    byte_question = question.encode('utf-8')
                    connSocket.send(byte_question)
                    question_countdown -= 1

                    # receive answer from client
                    received = connSocket.recv(4096)
                    answer = received.decode()
                    if "/q" in answer:
                        print("The client requested for the game to end. Returning to chatroom...\n")
                        mode = "CHAT"
                        new_chat = 1
                        break
                    if "win" in answer:
                        print("Congratulations! You guessed correctly and won 20 questions! Now returning to chatroom...\n")
                        mode = "CHAT"
                        new_chat = 1
                        break
                    print(f"{answer}\n")

                # if end of game (loss)
                if question_countdown == 0:
                    print("Sorry, you ran out of questions. Game over! Now returning to chatroom...\n")
                    mode = "CHAT"
                    new_chat = 1















