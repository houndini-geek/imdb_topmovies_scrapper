import pandas as pd
from bs4 import BeautifulSoup
import requests

# Set headers for the HTTP request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

def scrape_movies():
 
    # Send GET request to IMDb's "Most Popular Movies" page
    response = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=chttp_ql_2', headers=headers)
   
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all movie cards in the HTML
    all_cards = soup.find_all('li', class_='ipc-metadata-list-summary-item')

    movies = []  # List to store movie details

    # Loop through the first few movie entries (you can adjust the range as needed)
    for card in all_cards[:50]:  # Adjust range for more movies
        # Get the title
        title_element = card.find('h3', class_='ipc-title__text')
        title = title_element.text if title_element else "No title found"
        
        # Get the first image source
        img_element = card.find('div', class_='ipc-media')
        img_src = img_element.img['src'] if img_element and img_element.img else "No image found"

        # Get year, duration, and rating
        metadata = card.find('div', class_='sc-5bc66c50-5 hVarDB cli-title-metadata')
        if metadata:
            year = metadata.find_all('span', class_='cli-title-metadata-item')[0].text
            duration = metadata.find_all('span', class_='cli-title-metadata-item')[1].text
            rating = metadata.find_all('span', class_='cli-title-metadata-item')[2].text
        else:
            year, duration, rating = "No year", "No duration", "No rating"

        # Get the IMDb rating
        imdb_rating_element = card.find('span', class_='ipc-rating-star--rating')
        imdb_rating = imdb_rating_element.text if imdb_rating_element else "No IMDb rating found"

        # Append movie details to the list as a dictionary
        movies.append({
            "Title": title,
            "Year": year,
            "Duration": duration,
            "Rating": rating,
            "IMDb Rating": imdb_rating,
            "Image Source": img_src
        })

    return movies  # Return the list of movie details

if __name__ == "__main__":
    movie_data = scrape_movies()
    
    # Convert the movie data to a DataFrame
    data = pd.DataFrame(movie_data)
    
    # Save the DataFrame to a CSV file
    data.to_csv('top_movies.csv', index=False)
    
    print('Data saved to top_movies.csv')
