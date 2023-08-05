from image_fetcher.multithread_image_fetching import concurrent_image_search, concurrent_images_download
from image_fetcher.download_images import download_images 
from time import time

before = time()

# concurrent_image_search(
#     search_terms=['cat'], 
#     max_similtanous_threads=2,
#     max_image_fetching_threads=20,
#     image_download_timeout=3,
#     total_images=200, 
#     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
#     verbose=True,
#     progress_bar=False
# )

# download_images(
#     search_term='cat', 
#     total_images=200,  
#     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
#     progress_bar=False
# )

# download_images(
#     search_term='dog', 
#     total_images=200,  
#     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
#     progress_bar=False
# )

# concurrent_images_download(
#     search_term='cat', 
#     max_image_fetching_threads=20,
#     image_download_timeout=3,
#     total_images=200, 
#     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
#     verbose=True,
#     progress_bar=False
# )

# concurrent_images_download(
#     search_term='dog', 
#     max_image_fetching_threads=20,
#     image_download_timeout=3,
#     total_images=200, 
#     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
#     verbose=True,
#     progress_bar=False
# )


response = google_images_download.googleimagesdownload()
arguments = {
    "keywords":"cat",
    "limit":200,
    "chromedriver": "chromedriver.exe", 
    "format": "jpg",
    "print_urls":False}
paths = response.download(arguments)

response = google_images_download.googleimagesdownload()
arguments = {
    "keywords":"dog",
    "limit":200,
    "chromedriver": "chromedriver.exe", 
    "format": "jpg",
    "print_urls":False}
paths = response.download(arguments)

print(time()-before)