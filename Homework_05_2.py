import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Функції для MapReduce
def map_function(text):
    words = text.split()
    return [(word.lower().strip('.,!?"()'), 1) for word in words if word.isalpha()]


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# Виконання MapReduce
def map_reduce(text):
    mapped_values = map_function(text)
    shuffled_values = shuffle_function(mapped_values)
    reduced_values = reduce_function(shuffled_values)
    return reduced_values

# Функція для візуалізації топ-слів
def visualize_top_words(word_freq, top_n=10):
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Top {top_n} слів за частотою використання')
    plt.xticks(rotation=45)
    plt.show()

# Завантаження тексту з URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка під час завантаження: {e}")
        return None

if __name__ == "__main__":
    url = input("Введіть URL-адресу: ")
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_text_from_url, url)
        text = future.result()

    if text:
        word_freq = map_reduce(text)
        visualize_top_words(word_freq, top_n=10)
 