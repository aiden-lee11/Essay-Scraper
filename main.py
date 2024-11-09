from os import error
import requests
from bs4 import BeautifulSoup
import os


def main():
    url = "https://essaysthatworked.com/personal-statement-examples?utm_source=header"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    LIMIT = None

    main_paragraphs = soup.find_all(
        "div",
        {"class": "my-8 block text-base md:text-lg leading-7 md:leading-8"},
        limit=LIMIT,
    )

    review_sections = soup.find_all(
        "div",
        {"class": "mt-2 flex flex-col rounded-md bg-stone-100 py-3 px-3 md:flex-row"},
        limit=LIMIT,
    )

    # Why It Works
    # Only specific sections have this attribute so we define the array beforehand and then index accordingly
    positive_feedback_sections = [1,2,3,4,6,7,8,9,11,12,13,14,16,18,19,20]
    negative_feedback_sections = [2,6,7, 8,9, 10, 11, 12, 13, 14, 16, 19]

    feedback_sections = (soup.find_all(
        "ul",
        {"class": "text-base md:text-lg leading-7 md:leading-8 mb-8 list-none"},
    ))


    clean_feedback_sections = {}
    for i in range(len(main_paragraphs)):
        cleaned = ""
        if i in positive_feedback_sections:
            cleaned += "Positive Feedback: \n" + (feedback_sections.pop(0).get_text(separator=" ").strip()) + "\n\n"
        if i in negative_feedback_sections:
            cleaned += "Negative Feedback: \n" + (feedback_sections.pop(0).get_text(separator=" ").strip()) + "\n\n"

        clean_feedback_sections[i] = cleaned
    

    if not main_paragraphs:
        error("Main paragraphs not found.")
    if not review_sections:
        error("Review sections not found.")
    if not feedback_sections:
        error("Feedback sections not found.")

    if not os.path.exists("essays"):
        os.makedirs("essays")


    for i, (main_paragraph, review_section) in enumerate(
        zip(main_paragraphs, review_sections)
    ):
        feedback_section = clean_feedback_sections.get(i)

        cur_essay = (
            main_paragraph.find("div", {"class": "relative mt-8"})
            .get_text(separator=" ")
            .strip()
        )

        cur_prompt = (
            main_paragraph.find(
                "div",
                {"class": "[&>p>strong]:font-bold"},
            )
            .get_text(separator=" ")
            .strip()
        )

        cur_review = review_section.get_text(separator=" ").strip()

        to_write = (
            "Prompt: \n\n"
            + cur_prompt
            + "\n\n Essay: \n\n"
            + cur_essay
            + "\n\n Review: \n\n"
            + cur_review
        )

        if feedback_section:
            to_write += "\n\n Why This Essay Works \n\n"+ feedback_section

        with open(f"essays/essay_{i + 1}.txt", "w") as f:
            f.write(to_write)


if __name__ == "__main__":
    exit(main())
