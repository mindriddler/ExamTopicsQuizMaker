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


def choose_exam(exam_dir, res_dir):
    """Choose the exam to be read."""
    folder_exists = check_if_folder_exists(res_dir)
    if folder_exists:
        print("Your current exam is: ")
        current_exams = os.listdir(res_dir)
        print(current_exams)

        user_input = input(
            "Do you want to delete the current exam? [Y/n] ").lower()
        if user_input != "n":
            delete_current_exam(res_dir)
            print("Deleted the current exam. Please choose a new one.")
        else:
            print("Keeping the current exam.")
            for item in current_exams:
                if os.path.isdir(os.path.join(res_dir, item)):
                    return item
            return None

    exams = read_exam(exam_dir)
    if not exams:
        print("No exams available.")
        return None

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
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
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


def check_if_folder_exists(dir):
    """Check if the folder exists."""
    if not os.path.exists(dir):
        return False

    return True


if __name__ == "__main__":
    chosen_exam = choose_exam(EXAM_DIR, RES_DIR)
    if chosen_exam is not None:
        if not os.path.exists(RES_DIR):
            os.mkdir(RES_DIR)
        # Only copy the exam if it's not the current one
        current_exams = os.listdir(RES_DIR)
        if chosen_exam not in current_exams:
            copy_exam(EXAM_DIR, chosen_exam, RES_DIR)
        quiz = Quiz(RES_DIR)
        quiz.start_quiz()
    else:
        print("No exam selected. Exiting.")
