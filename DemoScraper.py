import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_answers(url):
    print(f"Fetching answers from URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve answers from {url} with status code {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    ol = soup.find('ol')
    answers = [li.text.strip() for li in ol.find_all('li')] if ol else []
    print(f"Number of answers found: {len(answers)}")
    return answers

def get_problems(url):
    print(f"Fetching problems from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data.")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    problems_data = []

    # Loop through each problem id from 1 to 15
    for i in range(1, 16):
        problem_id = f"Problem_{i}"
        header = soup.find('span', id=problem_id)
        if header:
            question_tag = header.parent.find_next_sibling('p')
            if question_tag:
                # Replace image tags with their alt text
                for img in question_tag.find_all('img'):
                    alt_text = img.get('alt', '')
                    img.replace_with(alt_text)
                question_text = question_tag.get_text(strip=True)
                problems_data.append(question_text)
        else:
            problems_data.append('No question found')

    return problems_data

def scrape_aime_data(start_year, end_year):
    all_data = []
    id_counter = 1
    for year in range(start_year, end_year + 1):
        print(f"Processing year: {year}")
        if year <= 1999:
            problems_url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AIME_Problems"
            answers_url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AIME_Answer_Key"
            answers = fetch_answers(answers_url)
            problems = get_problems(problems_url)
            data = [{'ID': f"{year}-{i + 1}", 'Year': year, 'Problem Number': i + 1, 'Question': q, 'Answer': answers[i]}
                    for i, q in enumerate(problems) if i < len(answers)]
            all_data.extend(data)
        else:
            for part in ['I', 'II']:
                problems_url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{part}_Problems"
                answers_url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{part}_Answer_Key"
                answers = fetch_answers(answers_url)
                problems = get_problems(problems_url)
                data = [{'ID': f"{year}-{part}-{i + 1}", 'Year': year, 'Part': part, 'Problem Number': i + 1, 'Question': q, 'Answer': answers[i]}
                        for i, q in enumerate(problems) if i < len(answers)]
                all_data.extend(data)

    df = pd.DataFrame(all_data)
    df.to_csv('AIME_Problems_and_Answers.csv', index=False)
    print("Data collection completed and saved to AIME_Problems_and_Answers.csv.")

# Example usage:
scrape_aime_data(1983, 2024)
