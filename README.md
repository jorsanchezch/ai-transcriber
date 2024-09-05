# AI Coding Challenge

Wisable is hiring you to build a quick POC of a Python-based API with some AI capabilities to extract structured data from a raw audio file.

## Requirements:

1. The user will provide an Excel file(.xlsx) and audio files. The Excel containts the fields they want to extract.
2. Convert audio file into a transcript file(PDF format).
3. Analyze the transcript and extract the user specified fields.
4. Use the previous Excel file and populate it with the extracted information.

## Techinical Tasks:

1. Implement robust error handling:
   - Check for valid audio file formats.
   - Validate user input for fields to extract.

2. Add support for processing multiple audio files:
   - Combine results from all files into a single Excel sheet.

3. Create an UI using [Retool](https://retool.com/).
   - It should be able to call your API.
   - It should give the excel back to the user.

4. Provide a `README.md` with the instructions to setup the project and also talk about the project structure.

## Rules

- Use the language mentioned in the email in which you got this test.
- The use of third-party libraries is allowed and encouraged.
- Make use of .gitignore, keep it clean.

## Resources

Inside the email we are going to provide you an OpenAI Key for the project(it will only have around 5$ to spend) and also a link to a folder with multiple audio for testing.

## Evaluation Criteria

1. Technical requirements.
2. Organization and consistency of the file and folder structure.
3. Modifiability and extendability of the system where required. 
4. Commit history (commits are organized and descriptive).
5. Time used to complete the test.
6. Complexity of the solution.

## Steps to run project:

1. Install pip requirements
2. Run the flask app on port 5000
3. Use the docker-compose to bring the UI up locally on port 3000
4. Create your version of the .env file
5. You may clean up the json db files in ./dbs