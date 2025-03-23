from ocean_scraper import *
from scada_scraper import *
from utils import move_files

delete_folder_contents('/Users/connor/dev/hackArizona/Biosphere-Ocean-Data')
scrape_the_ocean()
scrape_the_scada()
move_files()