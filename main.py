
import json
import logging

from analyzer import analyze_text
from config import MAX_INPUT_CHARACTERS


def main():

    print("\n================================")
    print("       AI TEXT ANALYZER")
    print("================================\n")

    print("Enter the text you want to analyze.")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    text = "\n".join(lines).strip()

    # Validate input
    if not text:

        print("\nError: Input text cannot be empty.")

        return

    if len(text) > MAX_INPUT_CHARACTERS:

        print(
            f"\nError: Maximum allowed text length "
            f"is {MAX_INPUT_CHARACTERS} characters."
        )

        return

    print("\nAnalyzing your text...\n")

    try:

        result = analyze_text(text)

        print("================================")
        print("         ANALYSIS RESULT")
        print("================================\n")

        print("SUMMARY")
        print(result["summary"])

        print("\nSENTIMENT")

        print(
            result["sentiment"]["label"].capitalize()
        )

        print(
            "Confidence:",
            result["sentiment"]["confidence"]
        )

        print("\nKEYWORDS")

        for keyword in result["keywords"]:

            print("-", keyword)

        print("\nTOPICS")

        for topic in result["topics"]:

            print("-", topic)

        print("\nCATEGORY")

        print(result["category"])

        print("\nUSAGE INFORMATION")

        print(
            json.dumps(
                result["usage"],
                indent=4
            )
        )

        # Save the analysis to a JSON file
        with open(
            "analysis_result.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            "\nAnalysis saved to analysis_result.json"
        )

    except Exception:

        logging.exception(
            "Unable to complete analysis."
        )

        print(
            "\nSomething went wrong. "
            "Check your API configuration and logs."
        )


if __name__ == "__main__":

    main()
