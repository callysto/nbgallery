from upload_functions import bulk_upload
from pathlib import Path

tags = ["these tags are", "totally meaningless", "this is just an example", "of how you might do it"]
desc = ['this is a meaningless description as well', "it's just an example"]
titles = None # use the notebook title

#We might also want to explicitly define wait conditions
# on a particular element

paths = '/Users/alextennant/Callysto/curriculum-notebooks/'

bulk_upload('alex.tennant@cybera.ca', 'password', paths, tags, desc, titles)