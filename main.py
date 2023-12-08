import os
import shutil

from quiz import Quiz

RES_DIR = "./res"  # directory of resources
EXAM_DIR = "./exams"  # directory of exams


def read_exam(exam_dir):
    """Reads the exam from the exam directory and returns the exam as a string."""
    exams = os.listdir(exam_dir)
    exam_list = []
    for exam in exams:
        if os.path.isdir(f"{exam_dir}/{exam}"):
            exam_list.append(exam)
        else:
            pass
    return exam_list


def choose_exam(exam_dir):
    """Choose the exam to be read."""
    delete_current_exam(RES_DIR)

    exams = read_exam(exam_dir)
    print("Choose the exam you want to take: ")
    print("Available exams: ")

    for i, exam in enumerate(exams, start=1):
        print(f"{i}. {exam}")

    while True:
        try:
            exam_choice = int(
                input("Enter the number of the exam you want to take: "))
            if 0 < exam_choice <= len(exams):
                exam_choice -= 1
                break
            else:
                print("Invalid number, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")

    exam = exams[exam_choice]
    print(f"You chose {exam}.")
    return exam


def copy_exam(exam_dir, exam, res_dir):
    """Copy the exam to the resources directory."""
    # Path to the source exam directory and the HTML file
    src_exam_dir = os.path.join(exam_dir, exam)
    src_html_file = os.path.join(exam_dir, f"{exam}.html")

    # Path to the destination exam directory and the HTML file
    dest_exam_dir = os.path.join(res_dir, exam)
    dest_html_file = os.path.join(res_dir, f"{exam}.html")

    # Copy the exam directory
    if os.path.exists(dest_exam_dir):
        shutil.rmtree(dest_exam_dir)
    shutil.copytree(src_exam_dir, dest_exam_dir)

    # Copy the HTML file
    if os.path.exists(dest_html_file):
        os.remove(dest_html_file)
    shutil.copy2(src_html_file, dest_html_file)


def delete_current_exam(res_dir):
    """Delete the current exam."""
    if os.path.exists(res_dir):
        print("Folder exists. Deleting...")
        shutil.rmtree(res_dir)


if __name__ == "__main__":
    chosen_exam = choose_exam(EXAM_DIR)
    copy_exam(EXAM_DIR, chosen_exam, RES_DIR)
    quiz = Quiz(RES_DIR)
    quiz.start_quiz()
