import json
import os
import re


# ============================================================
# PATHS
# ============================================================

SOP_FILE = "data/sop/flow.json"
TRANSCRIPT_FOLDER = "data/transcripts"
REPORT_FOLDER = "data/reports"


# ============================================================
# LOAD SOP
# ============================================================

try:
    with open(SOP_FILE, "r", encoding="utf-8") as file:
        flow = json.load(file)

except FileNotFoundError:
    print("ERROR: SOP file not found:")
    print(SOP_FILE)
    exit()

except json.JSONDecodeError as error:
    print("ERROR: Your flow.json contains invalid JSON.")
    print(error)
    exit()


# ============================================================
# CREATE REPORT FOLDER
# ============================================================

os.makedirs(REPORT_FOLDER, exist_ok=True)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):
    """
    Convert text to lowercase,
    remove extra spaces,
    and normalize punctuation.
    """

    text = text.lower()

    # Replace apostrophes
    text = text.replace("’", "'")

    # Remove punctuation
    text = re.sub(r"[^\w\s']", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# GET PHRASES FROM A RULE
# ============================================================

def get_rule_phrases(rule):
    """
    Supports multiple JSON formats:

    "required_phrase": "hello"

    OR

    "required_phrases": [
        "hello",
        "hi"
    ]

    OR

    "phrases": [
        "hello",
        "hi"
    ]

    OR

    "match": [
        "hello"
    ]
    """

    if "required_phrase" in rule:
        return [rule["required_phrase"]]

    if "required_phrases" in rule:
        return rule["required_phrases"]

    if "phrases" in rule:
        return rule["phrases"]

    if "match" in rule:
        return rule["match"]

    return []


# ============================================================
# PHRASE VARIATIONS
# ============================================================

def phrase_variations(phrase):
    """
    Create small variations to handle normal
    transcription differences.

    Example:

    inquire
    inquired
    inquiry

    are treated as related.
    """

    phrase = normalize(phrase)

    variations = {phrase}

    # Specific common transcription variations
    replacements = {
        "inquire": [
            "inquire",
            "inquired",
            "inquiry"
        ],

        "inquired": [
            "inquire",
            "inquired",
            "inquiry"
        ],

        "inquiry": [
            "inquire",
            "inquired",
            "inquiry"
        ],

        "zipcode": [
            "zipcode",
            "zip code"
        ],

        "zip code": [
            "zipcode",
            "zip code"
        ]
    }

    words = phrase.split()

    for index, word in enumerate(words):

        if word in replacements:

            for replacement in replacements[word]:

                new_words = words.copy()
                new_words[index] = replacement

                variations.add(
                    " ".join(new_words)
                )

    return list(variations)


# ============================================================
# CHECK PHRASE
# ============================================================

def contains_phrase(text, phrases):

    text = normalize(text)

    for phrase in phrases:

        for variation in phrase_variations(phrase):

            if normalize(variation) in text:
                return True

    return False


# ============================================================
# PARSE TRANSCRIPT
# ============================================================

def parse_transcript(lines):

    conversation = []

    for index, line in enumerate(lines):

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # ----------------------------------------------------
        # REPRESENTATIVE
        # ----------------------------------------------------

        if lower.startswith("rep:"):

            original_text = line[4:].strip()

            conversation.append({
                "line_number": index + 1,
                "speaker": "rep",
                "text": normalize(original_text),
                "original_text": original_text
            })

        # ----------------------------------------------------
        # CUSTOMER
        # ----------------------------------------------------

        elif lower.startswith("customer:"):

            original_text = line[9:].strip()

            conversation.append({
                "line_number": index + 1,
                "speaker": "customer",
                "text": normalize(original_text),
                "original_text": original_text
            })

        # ----------------------------------------------------
        # CX
        # ----------------------------------------------------

        elif lower.startswith("cx:"):

            original_text = line[3:].strip()

            conversation.append({
                "line_number": index + 1,
                "speaker": "customer",
                "text": normalize(original_text),
                "original_text": original_text
            })

    return conversation


# ============================================================
# ADD VIOLATION
# ============================================================

def add_violation(
    violations,
    rule_id,
    title,
    severity,
    line_number,
    evidence,
    reason
):

    violations.append({

        "rule_id": rule_id,

        "title": title,

        "severity": severity,

        "line_number": line_number,

        "evidence": evidence,

        "reason": reason
    })


# ============================================================
# CHECK OPENING + WEBSITE
# ============================================================

def check_opening_and_website(conversation):

    violations = []

    ordered_rules = flow.get("ordered_rules", [])

    if len(ordered_rules) < 2:
        return violations

    opening_rule = ordered_rules[0]

    website_rule = ordered_rules[1]

    rep_messages = [
        message
        for message in conversation
        if message["speaker"] == "rep"
    ]

    # ========================================================
    # NO REPRESENTATIVE
    # ========================================================

    if not rep_messages:

        add_violation(
            violations,
            opening_rule.get("id", 1),
            opening_rule.get("title", "Opening Greeting"),
            "CRITICAL",
            0,
            "",
            "No representative conversation was found."
        )

        return violations

    # ========================================================
    # RULE 1 - OPENING
    # ========================================================

    opening_phrases = get_rule_phrases(opening_rule)

    first_rep = rep_messages[0]

    if not contains_phrase(
        first_rep["text"],
        opening_phrases
    ):

        add_violation(
            violations,
            opening_rule.get("id", 1),
            opening_rule.get("title", "Opening Greeting"),
            "CRITICAL",
            first_rep["line_number"],
            first_rep["original_text"],
            "The representative's first statement did not contain the required opening greeting."
        )

    # ========================================================
    # FIND WEBSITE INQUIRY
    # ========================================================

    website_phrases = get_rule_phrases(website_rule)

    website_index = None

    for i, message in enumerate(conversation):

        if message["speaker"] != "rep":
            continue

        if contains_phrase(
            message["text"],
            website_phrases
        ):

            website_index = i

            break

    # ========================================================
    # WEBSITE INQUIRY MISSING
    # ========================================================

    if website_index is None:

        add_violation(
            violations,
            website_rule.get("id", 2),
            website_rule.get("title", "Website Inquiry"),
            "CRITICAL",
            0,
            "",
            "Required website inquiry statement was not detected."
        )

        return violations

    # ========================================================
    # WEBSITE MUST COME AFTER OPENING
    # ========================================================

    opening_index = None

    for i, message in enumerate(conversation):

        if message["speaker"] != "rep":
            continue

        if contains_phrase(
            message["text"],
            opening_phrases
        ):

            opening_index = i

            break

    if opening_index is not None:

        if website_index <= opening_index:

            message = conversation[website_index]

            add_violation(
                violations,
                website_rule.get("id", 2),
                website_rule.get("title", "Website Inquiry"),
                "CRITICAL",
                message["line_number"],
                message["original_text"],
                "Website inquiry must be spoken after the opening greeting."
            )

    return violations


# ============================================================
# CHECK QUALIFICATION QUESTIONS
# ============================================================

def check_qualification_rules(conversation):

    violations = []

    ordered_rules = flow.get("ordered_rules", [])

    if len(ordered_rules) < 3:
        return violations

    qualification_rule = ordered_rules[2]

    questions = qualification_rule.get(
        "required_questions",
        []
    )

    for question in questions:

        found = False

        phrases = question.get(
            "phrases",
            []
        )

        for message in conversation:

            if message["speaker"] != question.get("speaker"):
                continue

            if contains_phrase(
                message["text"],
                phrases
            ):

                found = True

                break

        if not found:

            add_violation(
                violations,
                300,
                question.get(
                    "name",
                    "Qualification Question"
                ),
                "CRITICAL",
                0,
                "",
                "Required qualification question was not detected."
            )

    return violations


# ============================================================
# CHECK DISCLAIMER
# ============================================================

def find_disclaimer(conversation):

    ordered_rules = flow.get(
        "ordered_rules",
        []
    )

    if len(ordered_rules) < 4:
        return None

    disclaimer_rule = ordered_rules[3]

    phrases = get_rule_phrases(
        disclaimer_rule
    )

    for i, message in enumerate(conversation):

        if message["speaker"] != "rep":
            continue

        if contains_phrase(
            message["text"],
            phrases
        ):

            return i

    return None


def check_disclaimer(conversation):

    violations = []

    ordered_rules = flow.get(
        "ordered_rules",
        []
    )

    if len(ordered_rules) < 4:
        return violations

    disclaimer_rule = ordered_rules[3]

    disclaimer_index = find_disclaimer(
        conversation
    )

    # ========================================================
    # DISCLAIMER MISSING
    # ========================================================

    if disclaimer_index is None:

        add_violation(
            violations,
            disclaimer_rule.get("id", 4),
            disclaimer_rule.get(
                "title",
                "Audio Disclaimer"
            ),
            "CRITICAL",
            0,
            "",
            "Required audio disclaimer was not detected."
        )

        return violations

    # ========================================================
    # QUALIFICATION QUESTIONS MUST COME BEFORE DISCLAIMER
    # ========================================================

    if len(ordered_rules) >= 3:

        qualification_rule = ordered_rules[2]

        for question in qualification_rule.get(
            "required_questions",
            []
        ):

            found_before = False

            for message in conversation[
                :disclaimer_index
            ]:

                if message["speaker"] != question.get("speaker"):
                    continue

                if contains_phrase(
                    message["text"],
                    question.get(
                        "phrases",
                        []
                    )
                ):

                    found_before = True

                    break

            if not found_before:

                disclaimer_message = conversation[
                    disclaimer_index
                ]

                add_violation(
                    violations,
                    304,
                    "Qualification Before Disclaimer",
                    "CRITICAL",
                    disclaimer_message["line_number"],
                    disclaimer_message["original_text"],
                    f"{question.get('name', 'Qualification question')} was not detected before the disclaimer."
                )

    return violations


# ============================================================
# CUSTOMER CONSENT
# ============================================================

def check_customer_consent(conversation):

    violations = []

    disclaimer_index = find_disclaimer(
        conversation
    )

    if disclaimer_index is None:
        return violations

    consent_phrases = [
        "yes",
        "yeah",
        "i agree"
    ]

    consent_found = False

    for message in conversation[
        disclaimer_index + 1:
    ]:

        if message["speaker"] != "customer":
            continue

        text = normalize(
            message["text"]
        )

        # Clear consent only
        if text in consent_phrases:

            consent_found = True

            break

    if not consent_found:

        add_violation(
            violations,
            5,
            "Customer Consent",
            "CRITICAL",
            0,
            "",
            "Customer did not provide a clear YES, YEAH, or I AGREE after the disclaimer."
        )

    return violations


# ============================================================
# CUSTOMER CRITICAL EVENTS
# ============================================================

def check_customer_events(conversation):

    violations = []

    events = flow.get(
        "critical_customer_events",
        []
    )

    for event in events:

        trigger_index = None

        # ====================================================
        # FIND EVENT
        # ====================================================

        for i, message in enumerate(conversation):

            if message["speaker"] != "customer":
                continue

            if contains_phrase(
                message["text"],
                event.get("phrases", [])
            ):

                trigger_index = i

                break

        if trigger_index is None:
            continue

        action = event.get(
            "required_action"
        )

        # ====================================================
        # DNC / SCAM / LOCATION
        # ====================================================

        if action == "END_CALL":

            rep_after_event = [
                message
                for message in conversation[
                    trigger_index + 1:
                ]
                if message["speaker"] == "rep"
            ]

            if rep_after_event:

                first_rep = rep_after_event[0]

                add_violation(
                    violations,
                    event.get("id"),
                    event.get("title"),
                    event.get(
                        "severity",
                        "CRITICAL"
                    ),
                    first_rep["line_number"],
                    first_rep["original_text"],
                    f"Customer triggered '{event.get('title')}' but the representative continued the conversation instead of ending the call."
                )

        # ====================================================
        # NOT INTERESTED
        # ====================================================

        elif action == "MAX_ONE_REBUTTAL":

            max_rebuttals = event.get(
                "max_rebuttals",
                1
            )

            rebuttal_count = 0

            rebuttal_phrases = [

                "but",

                "however",

                "let me explain",

                "just to qualify",

                "you may qualify",

                "you might qualify",

                "additional benefits",

                "let me tell you",

                "before you go",

                "just hear me out",

                "i understand but",

                "i completely understand",

                "i understand you are not interested",

                "i understand you're not interested",

                "give me just a moment",

                "just give me a moment"
            ]

            for message in conversation[
                trigger_index + 1:
            ]:

                if message["speaker"] != "rep":
                    continue

                if contains_phrase(
                    message["text"],
                    rebuttal_phrases
                ):

                    rebuttal_count += 1

                    # =================================================
                    # SECOND REBUTTAL = RED
                    # =================================================

                    if rebuttal_count > max_rebuttals:

                        add_violation(
                            violations,
                            event.get("id"),
                            event.get("title"),
                            event.get(
                                "severity",
                                "CRITICAL"
                            ),
                            message["line_number"],
                            message["original_text"],
                            f"Customer said they were not interested and the representative made more than {max_rebuttals} rebuttal."
                        )

                        break

    return violations


# ============================================================
# PROHIBITED REPRESENTATIVE RULES
# ============================================================

def check_prohibited_rep_rules(
    conversation
):

    violations = []

    rules = flow.get(
        "prohibited_rep_rules",
        []
    )

    for rule in rules:

        phrases = rule.get(
            "phrases",
            []
        )

        for message in conversation:

            if message["speaker"] != "rep":
                continue

            if contains_phrase(
                message["text"],
                phrases
            ):

                add_violation(
                    violations,
                    rule.get("id"),
                    rule.get("title"),
                    rule.get(
                        "severity",
                        "CRITICAL"
                    ),
                    message["line_number"],
                    message["original_text"],
                    "Prohibited representative statement detected."
                )

    return violations


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_call(conversation):

    violations = []

    # --------------------------------------------------------
    # Opening + Website
    # --------------------------------------------------------

    violations.extend(
        check_opening_and_website(
            conversation
        )
    )

    # --------------------------------------------------------
    # Qualification Questions
    # --------------------------------------------------------

    violations.extend(
        check_qualification_rules(
            conversation
        )
    )

    # --------------------------------------------------------
    # Disclaimer
    # --------------------------------------------------------

    violations.extend(
        check_disclaimer(
            conversation
        )
    )

    # --------------------------------------------------------
    # Customer Consent
    # --------------------------------------------------------

    violations.extend(
        check_customer_consent(
            conversation
        )
    )

    # --------------------------------------------------------
    # Customer Events
    # --------------------------------------------------------

    violations.extend(
        check_customer_events(
            conversation
        )
    )

    # --------------------------------------------------------
    # Prohibited Rep Statements
    # --------------------------------------------------------

    violations.extend(
        check_prohibited_rep_rules(
            conversation
        )
    )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    if violations:

        status = "RED"

    else:

        status = "GREEN"

    return status, violations


# ============================================================
# CREATE RED CALL REPORT
# ============================================================

def create_report(
    filename,
    violations
):

    base_name = os.path.splitext(
        filename
    )[0]

    report_path = os.path.join(
        REPORT_FOLDER,
        f"{base_name}_report.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "========================================\n"
        )

        report.write(
            "        AI CALL QA REPORT\n"
        )

        report.write(
            "========================================\n\n"
        )

        report.write(
            f"Call File: {filename}\n"
        )

        report.write(
            "Status: RED\n\n"
        )

        report.write(
            "VIOLATIONS\n"
        )

        report.write(
            "----------------------------------------\n\n"
        )

        for violation in violations:

            report.write(
                f"Rule ID: {violation['rule_id']}\n"
            )

            report.write(
                f"Violation: {violation['title']}\n"
            )

            report.write(
                f"Severity: {violation['severity']}\n"
            )

            if violation["line_number"]:

                report.write(
                    f"Transcript Line: {violation['line_number']}\n"
                )

            if violation["evidence"]:

                report.write(
                    f"Evidence: {violation['evidence']}\n"
                )

            report.write(
                f"Reason: {violation['reason']}\n"
            )

            report.write(
                "\n----------------------------------------\n\n"
            )

    return report_path


# ============================================================
# START SYSTEM
# ============================================================

print()
print("==============================================")
print("             AI CALL QA SYSTEM")
print("==============================================")
print()


# ============================================================
# CHECK TRANSCRIPT FOLDER
# ============================================================

if not os.path.exists(
    TRANSCRIPT_FOLDER
):

    print(
        "ERROR: Transcript folder does not exist."
    )

    print(
        TRANSCRIPT_FOLDER
    )

    exit()


# ============================================================
# GET ALL TRANSCRIPTS
# ============================================================

transcript_files = sorted(

    file

    for file in os.listdir(
        TRANSCRIPT_FOLDER
    )

    if file.lower().endswith(
        ".txt"
    )
)


total_calls = len(
    transcript_files
)

red_count = 0

green_count = 0

call_results = []


# ============================================================
# PROCESS EVERY CALL
# ============================================================

for filename in transcript_files:

    filepath = os.path.join(
        TRANSCRIPT_FOLDER,
        filename
    )

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

    except Exception as error:

        print(
            f"ERROR reading {filename}: {error}"
        )

        continue

    # --------------------------------------------------------
    # PARSE
    # --------------------------------------------------------

    conversation = parse_transcript(
        lines
    )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    status, violations = analyze_call(
        conversation
    )

    call_results.append(
        (filename, status, len(violations))
    )

    # ========================================================
    # RED CALL
    # ========================================================

    if status == "RED":

        red_count += 1

        print()
        print("🔴 RED CALL")
        print("----------------------------------------------")

        print(
            f"File: {filename}"
        )

        print()

        print(
            "Violations:"
        )

        for violation in violations:

            print(
                f"  • {violation['title']}"
            )

            print(
                f"    Severity: {violation['severity']}"
            )

            if violation["line_number"]:

                print(
                    f"    Transcript line: {violation['line_number']}"
                )

            if violation["evidence"]:

                print(
                    f"    Evidence: {violation['evidence']}"
                )

            print(
                f"    Reason: {violation['reason']}"
            )

            print()

        # ----------------------------------------------------
        # SAVE REPORT
        # ----------------------------------------------------

        report_path = create_report(
            filename,
            violations
        )

        print(
            f"Report saved: {report_path}"
        )

        print(
            "----------------------------------------------"
        )

    # ========================================================
    # GREEN CALL
    # ========================================================

    else:

        green_count += 1

        print()
        print("🟢 GREEN CALL")
        print("----------------------------------------------")

        print(
            f"File: {filename}"
        )

        print(
            "No violations found."
        )

        print(
            "----------------------------------------------"
        )

        # Green calls are printed, but NO report file is created.


# ============================================================
# SUMMARY
# ============================================================

print()
print("==============================================")
print("              SCAN COMPLETE")
print("==============================================")

print(
    f"Total Calls : {total_calls}"
)

print(
    f"Red Calls   : {red_count}"
)

print(
    f"Green Calls : {green_count}"
)

# ------------------------------------------------------------
# STATUS OF EVERY CALL
# ------------------------------------------------------------

print()
print("CALL STATUS LIST")
print("----------------------------------------------")

summary_lines = []

for name, call_status, violation_count in call_results:

    if call_status == "RED":
        line = f"{name:<20} RED    ({violation_count} violations)"
        print(f"🔴 {line}")
    else:
        line = f"{name:<20} GREEN"
        print(f"🟢 {line}")

    summary_lines.append(line)

summary_path = os.path.join(
    REPORT_FOLDER,
    "summary.txt"
)

with open(
    summary_path,
    "w",
    encoding="utf-8"
) as summary_file:

    summary_file.write("AI CALL QA SUMMARY\n")
    summary_file.write("==================\n\n")
    summary_file.write(f"Total Calls : {total_calls}\n")
    summary_file.write(f"Red Calls   : {red_count}\n")
    summary_file.write(f"Green Calls : {green_count}\n\n")

    for line in summary_lines:
        summary_file.write(line + "\n")

print()
print(f"Summary saved: {summary_path}")

print()