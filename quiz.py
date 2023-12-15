import random
import textwrap
from datetime import datetime
from io import TextIOWrapper

from _classes import CardList, os, re


class Quiz:

    def __init__(self, resources_dir=None) -> None:
        self.__cardlist = CardList(resources_dir)
        self.__log_dirname = "wrong_answers"
        self.__init_questions_per_quiz()
        self.__init_show_answer_immediately()
        self.__create_wrong_answers_directory()
        self.quiz_cards = self.__generate_quiz()

    def __init_questions_per_quiz(self):
        """
        Initialize the variable that shows how many questions should be shown in a quiz run
        """
        try:
            self.__questions_per_quiz = int(
                input("How many questions do you want to have? (Max: " +
                      str(len(self.__cardlist.cards_list)) + ") "))
            while self.__questions_per_quiz > len(self.__cardlist.cards_list):
                self.__questions_per_quiz = int(
                    input("Please pick a NUMBER. (Max: " +
                          str(len(self.__cardlist.cards_list)) + ")"))
        except ValueError:
            print("Defaulted to max number of questions.")
            self.__questions_per_quiz = len(self.__cardlist.cards_list)

        use_specific_range = (input(
            "Do you want the questions to be from a specific range [y/N]? ").
                              lower() == "y")
        if use_specific_range:
            self.__range_selection = input(
                f"""Do you want the {self.__questions_per_quiz} questions to be from the 
[1] beginning
[2] end
Please select 1 or 2: """)
        else:
            self.__range_selection = None

    def __init_show_answer_immediately(self):
        """
        Initializes the variable that decides if you want the correct answer shown after you respond
        """
        self.__show_answer_immediately = input(
            """Do you want to have the answer shown immediately after you respond?
(If not, you will be shown a score at the end and a file will be generated with the wrong answers anyway.)[Y/n]"""
        )

        if self.__show_answer_immediately == "":
            self.__show_answer_immediately = "y"

        self.__show_answer_immediately = self.__show_answer_immediately.lower()
        while (self.__show_answer_immediately != "n" and
               self.__show_answer_immediately != "y"):
            self.__show_answer_immediately = input(
                "Please pick between 'y'(yes) or 'n'(no): ")
            self.__show_answer_immediately = self.__show_answer_immediately.lower(
            )

    def __generate_quiz(self) -> list:
        """
        Generate a random list of card objects that are limited by the size of how
        many questions the player wants to have
        """
        if self.__range_selection == "1":
            selected_cards = self.__cardlist.cards_list[:self.
                                                        __questions_per_quiz]
        elif self.__range_selection == "2":
            selected_cards = self.__cardlist.cards_list[-self.
                                                        __questions_per_quiz:]
        else:
            selected_cards = self.__cardlist.cards_list

        shuffle = input(
            "Do you want the questions to be shuffled? [Y/n] ").lower()

        if shuffle == "":
            shuffle = "y"

        if shuffle == "y":
            random.shuffle(selected_cards)
            return selected_cards[:self.__questions_per_quiz]
        selected_cards = selected_cards[:self.__questions_per_quiz]
        return selected_cards[:self.__questions_per_quiz]

    def __clear(self):
        """
        Clear the terminal window
        """
        print("")
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def __create_wrong_answers_directory(self):
        try:
            os.mkdir(self.__log_dirname)
        except:
            print("Wrong answers directory already exists. Continuing..")

    def __init_answers_file(self) -> TextIOWrapper:
        """
        Initialize the filename with the current datetime, while omitting spaces and colon
        """
        filename = re.sub(" ", "_", str(datetime.now())).split(".")[
            0]  # remove the miliseconds as they were delimited by '.'
        filename = re.sub(
            ":", "-",
            filename)  # remove ':' as they are a special char on Windows..
        filename += ".txt"
        filename = os.path.join(self.__log_dirname, filename)
        wrong_answers_file = open(
            filename, "w",
            encoding="UTF-8")  # file where the wrong answers will be written to

        return wrong_answers_file

    def __write_to_file(self, wrong_answers_file, card, your_answer):
        wrapper = textwrap.TextWrapper()  # wrap text so it looks better

        wrong_answers_file.write(card.question_number + " " +
                                 wrapper.fill(text=card.question) + "\n")
        wrong_answers_file.write("-" * 40 + "\n")
        for ans in card.answers:
            try:
                # ans = str(ans.encode('utf-8'))  # some answers give a UnicodeEncodeError: 'charmap' codec can't encode character '\u05d2' in position 192: character maps to <undefined>
                wrong_answers_file.write(
                    wrapper.fill(text=ans) +
                    "\n")  # one answer had a weird encoding
            except:
                wrong_answers_file.write(str(ans) + "\n")

        wrong_answers_file.write("Your answer: " + your_answer.upper() + "\n")
        wrong_answers_file.write("Correct answer: " + card.correct_answer +
                                 "\n")
        wrong_answers_file.write("-" * 40 + "\n\n")

    def start_quiz(self):
        """
        The main logic function for the quiz to run
        """
        self.__clear()

        correct_answers = 0  # initialize correct answers

        wrong_answers_file = self.__init_answers_file()
        wrapper = textwrap.TextWrapper()  # wrap text so it looks better

        print(
            """Your quiz starts now. Please enter the characters corresponding to the answers (e.g., 'AB', 'C', 'DE').
    Answers are NOT case sensitive.""")
        input("Press Enter to continue..")

        for index, card in enumerate(self.quiz_cards):
            print("")
            print(str(index + 1) + "/" + str(self.__questions_per_quiz))
            print(card.question_number + " " + wrapper.fill(text=card.question))
            print("-" * 40)
            for ans in card.answers:
                print(wrapper.fill(text=ans))
            print("-" * 40)
            your_answer = input("Your answer: ").upper()

            correct_answer_set = set(card.correct_answer.upper())
            your_answer_set = set(your_answer)

            if your_answer_set == correct_answer_set:
                correct_answers += 1
            else:
                # write to the wrong answer to the file
                self.__write_to_file(wrong_answers_file, card, your_answer)

            if self.__show_answer_immediately == "y":
                print("Correct answer: ", card.correct_answer)
                print("Your percentage: " +
                      str(round(correct_answers / (index + 1) * 100, 2)) + "%")
                input("Press Enter to continue..")
                self.clear()

        wrong_answers_file.close()  # writing is done so we close the file

        print("=^=" * 40)
        print("The quiz is DONE! Good job!")
        print("Your score: " + str(correct_answers) + "/" +
              str(self.__questions_per_quiz))
        print("Your percentage: " +
              str(round(correct_answers / self.__questions_per_quiz * 100, 2)) +
              "%")

    def clear(self):
        """
        Clear the terminal window
        """
        print("")
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")
