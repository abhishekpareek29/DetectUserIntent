import nltk
from nltk import FreqDist

def main():
    data = []
    with open("/Users/saurabh/Downloads/Bad_Citation_Searches.csv") as f:
        data.append(f.readlines())
    flat_data = [item for sublist in data for item in sublist]

    print(fdist.items())

if __name__ == '__main__':
    main()