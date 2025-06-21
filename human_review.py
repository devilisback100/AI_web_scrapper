def human_review(original, spun, reviewed, retry_callback):
    def preview_lines(text):
        if not text:
            return "(No content)"
        lines = text.splitlines()
        return '\n'.join(lines[:5]) + ("\n..." if len(lines) > 5 else "")

    while True:
        print("\n--- AI written Text (First 5 lines) ---\n")
        print(preview_lines(spun))
        print("\n--- AI Reviewed Text (First 5 lines) ---\n")
        print(preview_lines(reviewed))
        print("\nOptions:")
        print("  (A) Accept as is")
        print("  (E) Edit manually")
        print("  (R) Retry scraping/agents")

        choice = input("Choose an option [A/E/R]: ").strip().upper()
        if choice == 'E':
            print("\nEnter your edited text below. End with a single '.' on a line:")
            edited = []
            while True:
                line = input()
                if line.strip() == '.':
                    break
                edited.append(line)
            return '\n'.join(edited)
        elif choice == 'R':
            print(" Retrying scraping and AI agents...\n")
            original, spun, reviewed = retry_callback()
            continue  
        elif choice == 'A':
            return reviewed if reviewed else spun
        else:
            print("Invalid option. Please choose one of A, E, or R.")
