
Background
----------

MightySignal provides a window into the black box of the mobile app world by finding high-value signals for sales and marketing teams. As part of our awesome backend stack, we regularly scrape app metadata–such as app names, ratings, and descriptions–from public app pages. For this challenge, we want you to implement your own mini version of this scraper!

Instructions
------------

### Setup

*   Create a **private** GitHub repository. If you can’t create private repositories on GitHub, you can create a private GitLab repository or create a local one.
*   Add a Python project to the repository. Use Python 2.7.
*   Use `requirements.txt` for packages.

### Input

*   Create a module `scraper.py`. The program should be executed by the command `python scraper.py input_csv_path`. The argument `input_csv_path` is a string path to a local [CSV file with this format](/coding-challenge-directions/input.csv). It’s a CSV containing a list of apps to scrape.
    
    ### Scraping
    
*   Your code should scrape iTunes public pages, such as this: [https://itunes.apple.com/us/app/id1261357853](https://itunes.apple.com/us/app/id1261357853).
*   The data you need to scrape is described in the _Output_ section below.
*   Only scrape United States pages (ones with `/us/` in the URL).

### Output

*   Given the input CSV of apps, you’ll write two JSON files, `apps.json` and `filtered_apps.json`, to the same directory as `scraper.py`
*   `apps.json` [(example here)](/coding-challenge-directions/apps.json) should be a JSON array, with array elements in the same order as the CSV and each array element containing keys:
    *   `name` - string - The name of the app
    *   `app_identifier` - number - The App Store’s identifier of the app (eg. `1261357853` for Fortnite)
    *   `minimum_ios_version` - string - The minimum iOS version required to run the app
    *   `languages` - array of strings, sorted alphabetically - All of the languages that the app supports
*   `filtered_apps.json` [(example here)](/coding-challenge-directions/filtered_apps.json) should be a JSON dictionary, with keys:
    *   `apps_in_spanish_and_tagalog` - array of numbers, sorted ascending - App identifiers of all apps that are available in both Spanish and Tagalog
    *   `apps_with_insta_in_name` - array of numbers, sorted ascending - App identifiers of all apps apps that have “insta” in the name (case insensitive)

### How We’ll Execute Your Code

*   We’ll run your code by running `python scraper.py input_csv_path` with our own input CSV of less than 100 apps. You can create as many files as you need in the project, but we’ll run the project using that command from within your project directory.

Submission
----------

*   When you’re finished, add `jasonlew` as a collaborator to your GitHub project. If you didn’t use GitHub, just ZIP up the project and attach it to the email (see below).
*   Email [founders@mightysignal.com](mailto:founders@mightysignal.com) with the following information:
    *   `MightySignal Coding Challenge` as the Subject
    *   In the email body, please include:
        *   Your name
        *   Link to your GitHub repository
*   We’ll run your code against our own inputs for functionality, look at the code for quality, and get back to you soon!


