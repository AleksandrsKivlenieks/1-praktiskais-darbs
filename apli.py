from tkinter import *
import random

# tiek izveidota poga, ar kuru var sākt spēli
def start_game_button():
    operation_frame = Frame()
    operation_frame.pack(fill="both")
    Start = Button(operation_frame,
                   text='Nospiediet šo pogu, lai sāktu spēli', command=start_game)
    Start.pack(fill="both")

# funkcija, kas tiek izpildīta pēc pogas "Nospiediet šo pogu, lai sāktu spēli" nospiešanas
def start_game():
    draw_ovals()  # tiek zīmēti apļi
    create_buttons()  # tiek izveidotas papildu pogas "Dators pirmais" un "Es esmu pirmais"
    window.delete('winner_button')  # tiek noņemts uzraksts ar uzvarētāju
    # funkcija "left_mouse_button" tiks izsaukta, kad tiks nospiesta kreisā peles poga
    window.bind("<Button-1>", func=left_mouse_button)

# tiek zīmēti apļi un piešķirti tagi, ar kuriem turpmāk būs vieglāk strādāt
# arī tiek iniciēts saraksts "position", kurā glabājas vērtības, kas atbilst apļu skaitam katrā kaudzītē
def draw_ovals():
    global position, clicked_on
    position = [7, 5, 3]
    clicked_on = 'NEW_GAME'
    for i in range(1, 8):
        temp_tag = "A"+f'{i}'
        if i <= 4:
            window.create_oval(60*i-40, 260, 60*i+10, 310,
                               fill="black", tags=temp_tag)
        if i <= 6 and i > 4:
            window.create_oval(120*i-550, 200, 120*i-500,
                               250, fill="black", tags=temp_tag)
        if i > 6:
            window.create_oval(110, 140, 160, 190, fill="black", tags=temp_tag)
    for i in range(1, 6):
        temp_tag = "B"+f'{i}'
        if i <= 4:
            window.create_oval(60*i+220, 260, 60*i+270, 310,
                               fill="black", tags=temp_tag)
        if i > 4:
            window.create_oval(370, 140, 420, 190, fill="black", tags=temp_tag)
    for i in range(1, 4):
        temp_tag = "C"+f'{i}'
        if i <= 2:
            window.create_oval(120*i+450, 200, 120*i+500,
                               250, fill="black", tags=temp_tag)
        if i > 2:
            window.create_oval(630, 140, 680, 190, fill="black", tags=temp_tag)

# tiek izveidotas pogas, ar kurām var veikt gājienu kā pirmajam vai otrajam
def create_buttons():
    window.delete("User_button")
    window.delete("PC_button")
    window.create_rectangle(
        2, 2, 202, 44, tags="User_button2")
    window.create_text(102, 23, text="Es esmu pirmais\n(Vispirms atlasiet šūnas)",
                       font="Arial 13 bold", tags="User_button", justify="center")
    window.create_rectangle(
        2, 48, 202, 90, tags="PC_button")
    window.create_text(102, 69, text="Dators pirmais",
                       font="Arial 18 bold", tags="PC_button", justify="center")

# notikumu apstrādātājs (nospiešana uz apļiem un dažādām pogām)
def left_mouse_button(event):
    if window.find_withtag("current"):
        global last_clicked, clicked_on
        clicked_on = window.gettags("current")
        first_letter = clicked_on[0][0]
        if position == [7, 5, 3]:
            last_clicked = None
        # ja tiek nospiesta poga "Dators pirmais", dators veic gājienu un teksts mainās
        if clicked_on[0] == "PC_button":
            PC_move()
            window.itemconfig(
                'User_button', text='Veikt gājienu!\n (Vispirms atlasiet šūnas)')
        # klikšķi uz uzvarētāja uzraksta tiek ignorēti
        elif clicked_on[0] == 'winner_button':
            pass
        # Ja kaudzītes burtu apzīmējums, uz kuras spēlētājs ir klikšķinājis, nesakrīt ar kaudzīti,
        # uz kuras spēlētājs ir klikšķinājis pēdējo reizi, viņš mēģina ņemt apļus no dažādām kaudzītēm, un tiek parādīts attiecīgais brīdinājums
        elif first_letter != last_clicked and last_clicked != None and clicked_on[0] != 'User_button' and clicked_on[0] != 'User_button2':
            window.create_text(400, 60, text="Ir aizliegts ņemt apļus no vairāk nekā vienas kaudzes", font="Times 18 bold",
                               tags="Illegal_move", justify="center")
            window.update_idletasks()
            window.after(1000)
            window.delete("Illegal_move")
        else:
            # Ja tika izvēlēts vismaz viens aplis un spēlētājs nospiež pogu "Veikt gājienu!", dators veic gājienu
            if (clicked_on[0] == 'User_button' or clicked_on[0] == 'User_button2') and last_clicked != 'User_button' and last_clicked != None and last_clicked != 'User_button2':
                last_clicked = None
                PC_move()
            # Ja spēlētājs mēģina nospiest pogu "Veikt gājienu!", bet nav izvēlējies nevienu apli, tiek parādīts attiecīgais brīdinājums
            elif (clicked_on[0] == 'User_button' or clicked_on[0] == 'User_button2') and last_clicked == None:
                window.create_text(400, 60, text="Jūs neesat izvēlējies nevienu apli",
                                   font="Times 18 bold", tags="Empty_move", justify="center")
                window.update_idletasks()
                window.after(1000)
                window.delete("Empty_move")
            # Ja iepriekšējie nosacījumi nav darbojušies, tad spēlētājs noklikšķina uz apļiem
            else:
                # poga "Dators pirmais" tiek noņemta
                window.delete('PC_button')
                # tiek atjaunināts saraksts "position"
                change_position(clicked_on[0])
                # noklikšķinātais aplis tiek noņemts no lauka
                window.delete(clicked_on[0])
                # mainīgajam tiek piešķirts tā objekta nosaukums, uz kura spēlētājs noklikšķināja
                last_clicked = clicked_on[0][0]
                # tiek pārbaudīts spēles beigu nosacījums (ja spēlētājs noņem pēdējo apli, viņš zaudē) un tiek parādīts paziņojums "Dators uzvarēja"
                if sum(position) == 0:
                    congratulations('computer')
        window.itemconfig(
            'User_button', text="Veikt gājienu!\n (Vispirms atlasiet šūnas)")

# tiek atjaunināts saraksts "position"
def change_position(clicked_on):
    if clicked_on[0][0] == 'A':
        position[0] -= 1
    elif clicked_on[0][0] == 'B':
        position[1] -= 1
    elif clicked_on[0][0] == 'C':
        position[2] -= 1

# Tiek noteikts nākamais gājiens, ko dators veiks
def PC_move():
    next_move = minimax(position, float('-inf'), float('inf'), 1)[1][1]
    window.delete("PC_button")
    # Tiek noteikta starpība starp abiem sarakstiem: pozīcija šajā brīdī un pozīcija, kas būs pēc datora gājiena
    diff = [abs(b - a) for b, a in zip(position, next_move)]
    index = 0
    for item in diff:
        if item != 0:
            index = diff.index(item)
    # No attiecīgās kaudzes tiek izņemts noteikts apļu skaits, turklāt apļi tiek izņemti pa vienam ar nelielu aizkavēšanos (0.5 s) un iekrāsoti zaļā krāsā
    if index == 0:
        existing_objects = []
        for item in range(1, 8):
            if window.find_withtag(f'A{item}'):
                existing_objects.append(f'A{item}')
        delete_count = diff[index]
        delete_id = set()
        while len(delete_id) != delete_count:
            delete_id.add(random.choice(existing_objects))
        for item in delete_id:
            window.itemconfig(item, fill="green")
            window.update_idletasks()
            window.after(500)
            window.delete(item)

    if index == 1:
        existing_objects = []
        for item in range(1, 6):
            if window.find_withtag(f'B{item}'):
                existing_objects.append(f'B{item}')
        delete_count = diff[index]
        delete_id = set()
        while len(delete_id) != delete_count:
            delete_id.add(random.choice(existing_objects))
        for item in delete_id:
            window.itemconfig(item, fill="green")
            window.update_idletasks()
            window.after(500)
            window.delete(item)

    if index == 2:
        existing_objects = []
        for item in range(1, 4):
            if window.find_withtag(f'C{item}'):
                existing_objects.append(f'C{item}')
        delete_count = diff[index]
        delete_id = set()
        while len(delete_id) != delete_count:
            delete_id.add(random.choice(existing_objects))
        for item in delete_id:
            window.itemconfig(item, fill="green")
            window.update_idletasks()
            window.after(500)
            window.delete(item)
    # tiek atjaunināts saraksts un pārbaudīts spēles beigu nosacījums
    position[0] = next_move[0]
    position[1] = next_move[1]
    position[2] = next_move[2]
    if sum(position) == 0:
        congratulations('user')

# Tiek parādīts uzraksts ar uzvarētāju
def congratulations(won):
    window.delete('User_button2')
    window.delete('User_button')
    if won == 'user':
        window.create_text(400, 200, text="JŪS UZVARĒJĀT!!!", font=("Times 30 bold"), tags="winner_button",
                           justify="center")
    elif won == 'computer':
        window.create_text(400, 200, text="DATORS UZVARĒJA", font=("Times 30 bold"), tags="winner_button",
                           justify="center")

# minimax algoritma ieviešana ar alfa-beta nogriešanu, kas nosaka nākamo gājienu
# tā kā algoritms ir rekursīvs, tiek konstruēts pilns spēles koks
def minimax(position, alpha, beta, max_turn):
    # rekursijas izejas nosacījums
    if (sum(position) == 0 and max_turn == 1):
        return (1, [position])
    if (sum(position) == 0 and max_turn == 0):
        return (-1, [position])
    # ja "maksimizētāja" gājiens
    if max_turn:
        max_score = float('-inf')
        best_move = None
        # visu gājienu iegūšana un analīze
        for move in get_moves(position):
            evaluation, temp = minimax(move, alpha, beta, 0)
            # Ja rezultāts ir uzlabojies (labāks gājiens), mainīgajiem tiek piešķirts jauns stāvoklis (labāks gājiens) un jauns novērtējums
            if evaluation > max_score:
                max_score = evaluation
                best_move = temp
            # tiek atjaunināta augšējā robeža
            alpha = max(alpha, evaluation)
            # ja jau bija atrasta labāka pozīcija, nav jēgas apsvērt šo zaru
            if alpha >= beta:
                break
        return max_score, [position] + best_move
    # tagad uz situāciju "skatās" no "minimizētāja" perspektīvas, kurš cenšas samazināt rezultātu
    else:
        min_score = float('inf')
        best_move = None
        for move in get_moves(position):
            evaluation, temp = minimax(move, alpha, beta, 1)
            if evaluation < min_score:
                min_score = evaluation
                best_move = temp
            # tiek atjaunināta apakšējā robeža
            beta = min(beta, evaluation)
            if alpha >= beta:
                break
        return min_score, [position] + best_move

# funkcija, kas atgriež visus iespējamos gājienus no dotās pozīcijas (sarakstu saraksts)
def get_moves(position):
    moves = []
    for i in range(position[0]):
        moves.append((i, position[1], position[2]))
    for i in range(position[1]):
        moves.append((position[0], i, position[2]))
    for i in range(position[2]):
        moves.append((position[0], position[1], i))
    return moves

# pamatmetode, kas tiek izpildīts rekursīvi, līdz logs tiek aizvērts
root = Tk()  # galvenais logs
root.resizable(False, False)  # logu stiepšanas aizliegums
root.title('Apļi')  # loga nosaukums
root.geometry("800x430+560+340") # Loga ģeometrijas iestatīšana (loga izmērs un pozīcija (nobīde ekrānā pa x un y asīm))
window = Canvas(root, width=800, height=400) # "audekla" objekta izmēri, uz kura tiks izvietoti dažādi objekti
window.pack()  # iepakotājs, viņš ir atbildīgs par to, kā logrīki tiks izvietoti galvenajā logā. Katram logrīkam ir jāizsauc iepakotāja metode, pretējā gadījumā tas netiks parādīts
start_game_button() # pogas "Nospiediet šo pogu, lai sāktu spēli" izveidošana, ar kuras palīdzību varētu sākt spēli
root.mainloop()