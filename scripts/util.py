import json

###############################################################################
                            # Auth Info #
###############################################################################
CONNECTION_STRING = "sqlite:///../data/db.db"
DATA_DIR = "../data"
KEY_FILE = '../key/keys.json'
YOUR_API_KEY = 'AIzaSyBIUXa8vzR-pRPlFfXgiT4bIQOFIenznFo'

def loadKeys(key_file):
    data = []
    with open(key_file) as data_file:
        data = json.load(data_file)

    return data["api_key"],data["api_secret"],data["token"],data["token_secret"]


###############################################################################
                            # State Name Matching #
###############################################################################
states2abb = {'delaware': 'DE', 'colorado': 'CO', 'american samoa': 'AS', 'guam': 'GU', 'washington': 'WA', 'rhode island': 'RI', 'tennessee': 'TN', 'wisconsin': 'WI', 'nevada': 'NV', 'maine': 'ME', 'north dakota': 'ND', 'mississippi': 'MS', 'south dakota': 'SD', 'new jersey': 'NJ', 'oklahoma': 'OK', 'wyoming': 'WY', 'minnesota': 'MN', 'north carolina': 'NC', 'illinois': 'IL', 'new york': 'NY', 'arkansas': 'AR', 'puerto rico': 'PR', 'indiana': 'IN', 'maryland': 'MD', 'louisiana': 'LA', 'national': 'NA', 'texas': 'TX', 'district of columbia': 'DC', 'arizona': 'AZ', 'iowa': 'IA', 'virgin islands': 'VI', 'michigan': 'MI', 'kansas': 'KS', 'utah': 'UT', 'virginia': 'VA', 'oregon': 'OR', 'connecticut': 'CT', 'montana': 'MT', 'california': 'CA', 'new mexico': 'NM', 'alaska': 'AK', 'vermont': 'VT', 'georgia': 'GA', 'northern mariana islands': 'MP', 'pennsylvania': 'PA', 'florida': 'FL', 'hawaii': 'HI', 'kentucky': 'KY', 'missouri': 'MO', 'nebraska': 'NE', 'new hampshire': 'NH', 'idaho': 'ID', 'west virginia': 'WV', 'south carolina': 'SC', 'ohio': 'OH', 'alabama': 'AL', 'massachusetts': 'MA'}
abbrs = ['WA', 'WI', 'WV', 'FL', 'WY', 'NH', 'NJ', 'NM', 'NA', 'NC', 'ND', 'NE', 'NY', 'RI', 'NV', 'GU', 'CO', 'CA', 'GA', 'CT', 'OK', 'OH', 'KS', 'SC', 'KY', 'OR', 'SD', 'DE', 'DC', 'HI', 'PR', 'TX', 'LA', 'TN', 'PA', 'VA', 'VI', 'AK', 'AL', 'AS', 'AR', 'VT', 'IL', 'IN', 'IA', 'AZ', 'ID', 'ME', 'MD', 'MA', 'UT', 'MO', 'MN', 'MI', 'MT', 'MP', 'MS']
states = ['colorado', 'guam', 'nebraska', 'washington', 'rhode island', 'tennessee', 'nevada', 'maine', 'mississippi', 'south dakota', 'new jersey', 'wyoming', 'minnesota', 'north carolina', 'new york', 'puerto rico', 'indiana', 'maryland', 'louisiana', 'texas', 'iowa', 'west virginia', 'michigan', 'utah', 'virginia', 'oregon', 'connecticut', 'georgia', 'american samoa', 'kentucky', 'district of columbia', 'new hampshire', 'south carolina', 'ohio', 'north dakota', 'national', 'hawaii', 'oklahoma', 'delaware', 'illinois', 'virgin islands', 'arkansas', 'idaho', 'arizona', 'wisconsin', 'kansas', 'montana', 'california', 'new mexico', 'vermont', 'northern mariana islands', 'pennsylvania', 'florida', 'alaska', 'missouri', 'alabama', 'massachusetts']

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set


def assignStates(s):
    s = str(s)

    for i in abbrs:
        if i in s:
            return i

    s = s.lower()
    for i in states:
        if i in s:
            return states2abb[i]

    # for k,v in states2abb.iteritems():
    #     s = s.lower()
    #     comm =  ''.join(list(lcs(s,k)))
    #     if len(comm) == len(k):
    #         print comm
    #         return v

    return 'None'