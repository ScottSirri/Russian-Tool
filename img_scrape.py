from icrawler.builtin import GoogleImageCrawler
import time

# Scrapes images from Google images for query, returns the name of the 
# directory that they're downloaded into
def get_imgs(query, num=3):
    
    program_start_time = time.time()
    dir_name = "imgs_" + query + "_" + str(program_start_time)

    google_Crawler = GoogleImageCrawler(storage = {'root_dir': dir_name})
    google_Crawler.crawl(keyword = query, max_num = num)

    return dir_name
