import json
import sys
import util
import re


def get_data(body):
    lines = [text.strip("# ") for text in re.split('[\n\r]+', body)]
    
    data = {}
    if "no response" not in lines[3].lower():
        data["company_name"] = lines[3]
    if "no response" not in lines[5].lower():
        data["title"] = lines[5]
    if "no response" not in lines[7].lower():
        data["locations"] = [line.strip() for line in lines[7].split("|")]
    
    return data


def main():
    event_file_path = sys.argv[1]

    with open(event_file_path) as f:
        event_data = json.load(f)


    # CHECK IF NEW OR OLD INTERNSHIPS

    new_internship = "new_internship" in [label["name"] for label in event_data["issue"]["labels"]]
    edit_internship = "edit_internship" in [label["name"] for label in event_data["issue"]["labels"]]

    if not new_internship and not edit_internship:
        util.fail("Only new_internship and edit_internship issues can be approved")

    # GET DATA FROM ISSUE FORM

    issue_body = event_data['issue']['body']

    data = get_data(issue_body)
    
    issue_title = "{} | {} | {} Location(s)".format(
        data.get('company_name', '?'), 
        data.get('title', '?'), 
        len(data.get('locations', [])),
    )

    util.setOutput("issue_title", issue_title)


if __name__ == "__main__":
    main()
