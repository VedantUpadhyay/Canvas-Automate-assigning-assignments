# Canvas-Automate-assigning-assignments

main.py file calls Canvas API with the API token, fetches all the students within a section, and assign a set of assignments to them in such fashion such that no two consectutive students has the same assignment assigned.

#Instruction
1. `pip install -r requirements.txt`
2. Generate your Canvas Account > Settings > New Access token. Add this to an .env file in your project as CANVAS_API_TOKEN.
3. In main.py, update API_URL, COURSE_ID, SECTION_ID, and ASSIGNMENTS_IDS as needed.
