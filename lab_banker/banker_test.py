import banker
import os

if __name__ == "__main__":
    no_test_files = 6
    banker_file = "banker.py"

    for i in range(no_test_files):
        try:
            question_file = f"test_files/q{i}.txt"
            answer_file = f"test_files/q{i}_answer.txt"
            command = f"python3 {banker_file} {question_file} > answer.txt && diff -w answer.txt {answer_file} > result.txt"
            os.system(command)

            with open("result.txt", "r") as f:
                value = f.readlines()
                if len(value) == 0:
                    print(f"PASS TEST {i}")
                else:
                    print(f"FAIL TEST {i} with diff:")
                    print(" ".join(i for i in value))

            # remove files
            os.system("rm answer.txt result.txt")
        except:
            print(
                "Command failed to run. Please run this file in POSIX-compliant OS."
            )
