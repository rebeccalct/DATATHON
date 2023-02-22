# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2
import requests
import os 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True, #  --index , the path to where our index.csv file resides
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--queries", required = True, # 
	help = "Path to the query image folder")
ap.add_argument("-r", "--result-path", required = True,
	help = "Path to the result path")
args = vars(ap.parse_args())
# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
for query in os.listdir(args["queries"]):
	subfolder = os.path.splitext(os.path.basename(query))[0] 
	path_subfolder = os.path.join("results",subfolder)
	if not os.path.exists(path_subfolder):
		os.makedirs(path_subfolder)
	query  = os.path.join("queries",query)
	query = cv2.imread(query)
	features = cd.describe(query)
	# perform the search
	searcher = Searcher(args["index"])
	results = searcher.search(features)
	# display the query
	#cv2.imshow("Query", query)
	# loop over the results
	for (score, resultID) in results:
		# load the result image and display it
		result = cv2.imread(args["result_path"] + "/" + resultID)
		#cv2.imshow("Result", result)
		filename = os.path.join(path_subfolder,resultID)
		cv2.imwrite(filename, result)  # save the image
		cv2.waitKey(0)

# python searchcopy.py --index index2.csv --queries queries --result-path E:/datathon/images
