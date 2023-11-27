import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def extract_tables(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    return tables

def tables_to_csv(tables, output_csv):
    dfs = []
    for i, table in enumerate(tables):
        html_string = str(table)
        print(html_string)
        try:
            df_list = pd.read_html(html_string, flavor='bs4')
            if df_list:
                df = df_list[0]
                # Check if the DataFrame has any rows
                if not df.empty:
                    dfs.append(df)
                    tempFileName = f'table_{i + 1}.csv'
                    df.to_csv(tempFileName, index=False)

                else:
                    print(f"Table {i + 1} has no data and will be skipped.")
        except: 
            print("bad table")

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_path = os.path.join(desktop_path, output_csv)
        combined_df.to_csv(output_path, index=False)
        print(f"Tables successfully combined and saved to {output_csv}")

        # Delete individual table files
        for i in range(len(tables)):
            table_file = f'table_{i + 1}.csv'
            if os.path.exists(table_file):
                os.remove(table_file)
                print(f"Deleted {table_file}")

    else:
        print("No valid tables found on the webpage.")

if __name__ == "__main__":
    url = "https://seaofthieves.wiki.gg/wiki/Commendations"
    output_csv = "combined_tables.csv"

    tables = extract_tables(url)
    tables_to_csv(tables, output_csv)
