import fitz

end_section_page = None
begin_section_page = None
section_title = None


def find_last_end_of_section(pdf_document, start_page, target_count):
    end_of_section_count = 0
    end_section_page = None
    for page_num in range(start_page, len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")
        if "END OF SECTION" in text:
            occurrences = text.count("END OF SECTION")
            end_of_section_count += occurrences

            if end_of_section_count >= target_count:
                end_section_page = page_num + 1  
                return end_section_page
    return None, end_section_page


def find_section_title(pdf_path):
    pdf_document = fitz.open(pdf_path)
    division_08_count = 0
    in_division_08 = False

    next_line = None
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")
        lines = text.split('\n')

        for idx, line in enumerate(lines):
            if "DIVISION 08 -- OPENINGS" in line:
                next_line = lines[idx + 1].strip()
                in_division_08 = True
                continue

            if "DIVISION 09" in line and in_division_08:
                in_division_08 = False
                break

            if in_division_08 and line.startswith("08"):
                division_08_count += 1

        if next_line:  
            break

    if next_line:
        parts = next_line.split(maxsplit=3)
        if len(parts) >= 4:
            section_title = (
                f"SECTION {parts[0]} {parts[1]} {parts[2]} - "
                f"{parts[3].upper()}"
            )
        else:
            section_title = (
                f"SECTION {parts[0]} {parts[1]} {parts[2]} - "
            )
    else:
        pdf_document.close()
        return

    matching_page = None
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")
        if section_title in text:
            matching_page = page_num + 1  
            break

    begin_section_page = matching_page
    end_section_page = find_last_end_of_section(
        pdf_document, matching_page, division_08_count)
    pdf_document.close()
    return section_title, begin_section_page, matching_page, end_section_page


pdf_path = 'S_00000000 Project Manual Vol 1of1_pdf.pdf'


(
    section_title,
    begin_section_page,
    matching_page,
    end_section_page
) = find_section_title(pdf_path)
message = (
    f"{section_title} starts at {begin_section_page}"
    f" ends on {end_section_page}"
)
print(message)
