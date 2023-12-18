import os
import random
import re
from datetime import datetime
from io import TextIOWrapper

from _classes import CardList


class Quiz:

    def __init__(self, resources_dir=None) -> None:
        self.__cardlist = CardList(resources_dir)
        self.__log_dirname = "wrong_answers"
        self.__init_questions_per_quiz()
        self.__init_show_answer_immediately()
        self.__create_wrong_answers_directory()
        self.quiz_cards = self.__generate_quiz()

    def __init_questions_per_quiz(self):
        try:
            self.__questions_per_quiz = int(
                input("How many questions do you want to have? (Max: " + str(len(self.__cardlist.cards_list)) + ") "))
            while self.__questions_per_quiz > len(self.__cardlist.cards_list):
                self.__questions_per_quiz = int(
                    input("Please pick a NUMBER. (Max: " + str(len(self.__cardlist.cards_list)) + ")"))
        except ValueError:
            print("Defaulted to max number of questions.")
            self.__questions_per_quiz = len(self.__cardlist.cards_list)

        use_specific_range = (input("Do you want the questions to be from a specific range [y/N]? ").lower() == "y")
        if use_specific_range:
            self.__range_selection = input(
                f"Do you want the {self.__questions_per_quiz} questions to be from the \n[1] beginning\n[2] end\nPlease select 1 or 2: "
            )
        else:
            self.__range_selection = None

    def __init_show_answer_immediately(self):
        self.__show_answer_immediately = input(
            "Do you want to have the answer shown immediately after you respond? (If not, you will be shown a score at the end and a file will be generated with the wrong answers anyway.)[Y/n]"
        )

        if self.__show_answer_immediately == "":
            self.__show_answer_immediately = "y"

        self.__show_answer_immediately = self.__show_answer_immediately.lower()
        while (self.__show_answer_immediately != "n" and self.__show_answer_immediately != "y"):
            self.__show_answer_immediately = input("Please pick between 'y'(yes) or 'n'(no): ")
            self.__show_answer_immediately = self.__show_answer_immediately.lower()

    def __generate_quiz(self) -> list:
        if self.__range_selection == "1":
            selected_cards = self.__cardlist.cards_list[:self.__questions_per_quiz]
        elif self.__range_selection == "2":
            selected_cards = self.__cardlist.cards_list[-self.__questions_per_quiz:]
        else:
            selected_cards = self.__cardlist.cards_list

        shuffle = input("Do you want the questions to be shuffled? [Y/n] ").lower()
        if shuffle == "":
            shuffle = "y"
        if shuffle == "y":
            random.shuffle(selected_cards)
            return selected_cards[:self.__questions_per_quiz]
        selected_cards = selected_cards[:self.__questions_per_quiz]
        return selected_cards[:self.__questions_per_quiz]

    def __clear(self):
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
        filename = re.sub(" ", "_", str(datetime.now())).split(".")[0]
        filename = re.sub(":", "-", filename)
        filename += ".txt"
        filename = os.path.join(self.__log_dirname, filename)
        wrong_answers_file = open(filename, "w", encoding="UTF-8")
        return wrong_answers_file

    def __write_to_file(self, wrong_answers_file, card, your_answer):
        wrong_answers_file.write(card.question_number + " " + card.question + "\n")
        wrong_answers_file.write("-" * 40 + "\n")
        for ans in card.answers:
            try:
                wrong_answers_file.write(ans + "\n")
            except:
                wrong_answers_file.write(str(ans) + "\n")
        wrong_answers_file.write("Your answer: " + your_answer.upper() + "\n")
        wrong_answers_file.write("Correct answer: " + card.correct_answer + "\n")
        wrong_answers_file.write("-" * 40 + "\n\n")

    def start_quiz(self):
        self.__clear()
        correct_answers = 0
        wrong_answers_file = self.__init_answers_file()

        print(
            "Your quiz starts now. Please enter the characters corresponding to the answers (e.g., 'AB', 'C', 'DE'). Answers are NOT case sensitive."
        )
        input("Press Enter to continue..")

        for index, card in enumerate(self.quiz_cards):
            print("")
            print(str(index + 1) + "/" + str(self.__questions_per_quiz))
            print(card.question_number + " " + card.question)
            print("-" * 40)
            for ans in card.answers:
                print(ans)
            print("-" * 40)
            your_answer = input("Your answer: ").upper()

            correct_answer_set = set(card.correct_answer.upper())
            your_answer_set = set(your_answer)

            if your_answer_set == correct_answer_set:
                correct_answers += 1
            else:
                self.__write_to_file(wrong_answers_file, card, your_answer)

            if self.__show_answer_immediately == "y":
                print("Correct answer: ", card.correct_answer)
                print("Your percentage: " + str(round(correct_answers / (index + 1) * 100, 2)) + "%")
                input("Press Enter to continue..")
                self.__clear()

        wrong_answers_file.close()
        print("=^=" * 40)
        print("The quiz is DONE! Good job!")
        print("Your score: " + str(correct_answers) + "/" + str(self.__questions_per_quiz))
        print("Your percentage: " + str(round(correct_answers / self.__questions_per_quiz * 100, 2)) + "%")

    def clear(self):
        print("")
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")
