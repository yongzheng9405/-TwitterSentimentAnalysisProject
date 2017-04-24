from scipy import stats
import numpy as np
import csv

sentiment_scores = np.random.random(52)

# input should be a numpy array of sentiment scores for the 50 states
def  calculateRegressions(sentiment_scores):

	white_ratios = []
	male_ratios = []
	educations = []
	populations = []
	incomes = []

	criteria = ("white ratio", "male ratio", "education level", "population", "median household income")
	r_values = []
	extents_of_correlation = []
	demographics = [("white ratio", white_ratios, 1),
					("male ratio", male_ratios, 2),
					("education level", educations, 6),
					("population", populations, 7),
					("median household income", incomes, 8)]

	with open('USdemographics_by_state.csv', 'r') as file:
		reader = csv.reader(file)
		# skip header
		next(reader)

		for row in reader:
			for (_, data, col) in demographics:
				num = row[col].replace(",", "", 10)
				num = num.replace("$", "")
				data.append(float(num))

	correlation = [[0.3, "not"],
					[0.5, "weakly"],
					[0.7, "moderately"],
					[1.0, "strongly"]]


	for (colname, data, _) in demographics:
		slope, intercept, r_value, p_value, std_err = stats.linregress(sentiment_scores, data)
		# print for debugging purposes
		# print(colname + " r value: " + str(r_value))
		r_values.append(str(r_value))

		abs_r = abs(r_value)
		for (num, extent) in correlation:
			if abs_r < num:
				# print for debugging purposes
				# print(extent + " correlated")
				extents_of_correlation.append(extent + " correlated")
				break


	file.close()
	# output is a tuple of 3 tuples of strings
	return (criteria, tuple(r_values), tuple(extents_of_correlation))

print(calculateRegressions(sentiment_scores))