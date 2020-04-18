import sys
from openalpr import Alpr



def recognise(image: str) -> str:
    confUrl = "Path to\\openalpr\\openalpr-2.3.0\\config\\openalpr.conf.defaults"
    runDirUrl = "Path to\\openalpr\\openalpr-2.3.0\\runtime_data"
    alpr = Alpr('eu', confUrl, runDirUrl)

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(1)
    results = alpr.recognize_file(image)

    for plate in results['results']:
        platenumber = plate['plate'][-7:]

    if len(platenumber) != 0:
        return platenumber
    else:
        return "Plate number not found"



