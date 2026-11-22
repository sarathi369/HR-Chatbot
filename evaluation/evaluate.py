
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.rag_pipeline import generate_answer

QUESTIONS_FILE = BASE_DIR / "evaluation" / "test_questions.json"
REPORT_FILE = BASE_DIR / "evaluation" / "evaluation_report.txt"


def evaluate_answer(expected_answer, generated_answer):
    expected_words = [
        word.lower().strip(".,!?()")
        for word in expected_answer.split()
        if len(word.strip(".,!?()")) > 3
    ]

    generated_text = generated_answer.lower()

    matched_words = [
        word for word in expected_words
        if word in generated_text
    ]

    if not expected_words:
        return False

    score = len(matched_words) / len(expected_words)
    return score >= 0.60


def run_evaluation():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    total_questions = len(questions)
    correct_answers = 0

    report = []

    report.append("HR CHATBOT - EVALUATION REPORT")
    report.append("=" * 60)

    for item in questions:
        question_id = item["id"]
        question = item["question"]
        expected_answer = item["expected_answer"]

        print(f"\nQuestion {question_id}: {question}")

        generated_answer = generate_answer(question)

        is_correct = evaluate_answer(
            expected_answer,
            generated_answer
        )

        if is_correct:
            correct_answers += 1
            result = "CORRECT"
        else:
            result = "NEEDS REVIEW"

        print("\nExpected Answer:")
        print(expected_answer)

        print("\nGenerated Answer:")
        print(generated_answer)

        print("\nResult:", result)
        print("-" * 60)

        report.append(f"\nQuestion {question_id}: {question}")
        report.append(f"\nExpected Answer:\n{expected_answer}")
        report.append(f"\nGenerated Answer:\n{generated_answer}")
        report.append(f"\nResult: {result}")
        report.append("-" * 60)

    accuracy = (correct_answers / total_questions) * 100

    summary = [
        "\nFINAL EVALUATION SUMMARY",
        "=" * 60,
        f"Total Questions: {total_questions}",
        f"Correct Answers: {correct_answers}",
        f"Incorrect / Needs Review: {total_questions - correct_answers}",
        f"Accuracy: {accuracy:.2f}%",
        "=" * 60
    ]

    print("\n".join(summary))
    report.extend(summary)

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"\nEvaluation report saved at:\n{REPORT_FILE}")


if __name__ == "__main__":
    run_evaluation()
