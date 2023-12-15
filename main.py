import os
import shutil

from quiz import Quiz

RES_DIR = "./res"  # Directory of resources
EXAM_DIR = "./exams"  # Directory of exams


def read_exam(exam_dir):
    """Reads exam directories from the exam directory and returns them as a list."""
    return [
        exam for exam in os.listdir(exam_dir)
        if os.path.isdir(os.path.join(exam_dir, exam))
    ]


def choose_exam(exam_dir, res_dir):
    """Choose the exam to be read."""
    if os.path.exists(res_dir):
        current_exams = [
            item for item in os.listdir(res_dir)
            if os.path.isdir(os.path.join(res_dir, item))
        ]
        if current_exams:
            print("Your current exam(s):")
            for exam in current_exams:
                print(f"- {exam}")
        else:
            print("No current exams found in the resource directory.")

        if input("Do you want to delete the current exam? [Y/n] ").lower(
        ) != 'n':
            shutil.rmtree(res_dir)
            print("Deleted the current exam. Please choose a new one.")
        else:
            print("Keeping the current exam.")
            return next((item for item in os.listdir(res_dir)
                         if os.path.isdir(os.path.join(res_dir, item))), None)

    exams = read_exam(exam_dir)
    if not exams:
        print("No exams available.")
        return None

    print("Choose the exam you want to take: ")
    for i, exam in enumerate(exams, start=1):
        print(f"{i}. {exam}")

    while True:
        try:
            exam_choice = int(
                input("Enter the number of the exam you want to take: ")) - 1
            if 0 <= exam_choice < len(exams):
                return exams[exam_choice]
            print("Invalid number, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")


def copy_exam(exam_dir, exam, res_dir):
    """Copy the exam to the resources directory."""
    os.makedirs(res_dir, exist_ok=True)

    src_exam_dir = os.path.join(exam_dir, exam)
    src_html_file = os.path.join(exam_dir, f"{exam}.html")
    dest_exam_dir = os.path.join(res_dir, exam)
    dest_html_file = os.path.join(res_dir, f"{exam}.html")

    if os.path.exists(dest_exam_dir):
        shutil.rmtree(dest_exam_dir)
    shutil.copytree(src_exam_dir, dest_exam_dir)

    if os.path.exists(dest_html_file):
        os.remove(dest_html_file)
    shutil.copy2(src_html_file, dest_html_file)


if __name__ == "__main__":
    chosen_exam = choose_exam(EXAM_DIR, RES_DIR)
    if chosen_exam:
        os.makedirs(RES_DIR, exist_ok=True)
        current_exams = os.listdir(RES_DIR)
        if chosen_exam not in current_exams:
            copy_exam(EXAM_DIR, chosen_exam, RES_DIR)
        quiz = Quiz(RES_DIR)
        quiz.start_quiz()
    else:
        print("No exam selected. Exiting.")
