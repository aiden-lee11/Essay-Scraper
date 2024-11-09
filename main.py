import requests
from bs4 import BeautifulSoup
import os
import json

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

    positive_feedback_sections = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 18, 19, 20]
    negative_feedback_sections = [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 19]

    feedback_sections = soup.find_all(
        "ul",
        {"class": "text-base md:text-lg leading-7 md:leading-8 mb-8 list-none"},
    )

    clean_feedback_sections = {}
    for i in range(len(main_paragraphs)):
        positive_feedback = ""
        negative_feedback = ""

        if i in positive_feedback_sections:
            positive_feedback = feedback_sections.pop(0).get_text(separator=" ").strip()
        if i in negative_feedback_sections:
            negative_feedback = feedback_sections.pop(0).get_text(separator=" ").strip()

        clean_feedback_sections[i] = {
            "Positive_Feedback": positive_feedback,
            "Negative_Feedback": negative_feedback
        }

    if not main_paragraphs:
        raise ValueError("Main paragraphs not found.")
    if not review_sections:
        raise ValueError("Review sections not found.")
    if not clean_feedback_sections:
        raise ValueError("Feedback sections not found.")

    os.makedirs("essays", exist_ok=True)
    os.makedirs("essay_jsons", exist_ok=True)

    for i, (main_paragraph, review_section) in enumerate(zip(main_paragraphs, review_sections)):
        feedback_section = clean_feedback_sections.get(i)

        cur_essay = main_paragraph.find("div", {"class": "relative mt-8"}).get_text(separator=" ").strip()
        cur_prompt = main_paragraph.find("div", {"class": "[&>p>strong]:font-bold"}).get_text(separator=" ").strip()
        cur_review = review_section.get_text(separator=" ").strip()

        # Prepare the text content
        to_write = (
            f"Prompt:\n\n{cur_prompt}\n\n"
            f"Essay:\n\n{cur_essay}\n\n"
            f"Review:\n\n{cur_review}\n\n"
        )
        
        if feedback_section["Positive_Feedback"]:
            to_write += f"Why This Essay Works (Positive Feedback):\n\n{feedback_section['Positive_Feedback']}\n\n"
        
        if feedback_section["Negative_Feedback"]:
            to_write += f"Why This Essay Needs Improvement (Negative Feedback):\n\n{feedback_section['Negative_Feedback']}\n\n"

        # Write to text file
        with open(f"essays/essay_{i + 1}.txt", "w") as f:
            f.write(to_write)

        # Prepare JSON data
        essay_data = {
            "Prompt": cur_prompt,
            "Essay": cur_essay,
            "Review": cur_review,
            "Positive_Feedback": feedback_section["Positive_Feedback"],
            "Negative_Feedback": feedback_section["Negative_Feedback"]
        }

        # Write to JSON file
        with open(f"essay_jsons/essay_{i + 1}.json", "w") as f:
            json.dump(essay_data, f, indent=4)

if __name__ == "__main__":
    exit(main())
