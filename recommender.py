import requests
import json

def askMovies():
    more = 'y'
    movieList = []
    while(more=='y'):
        movieName = input("Enter movie name : ")
        movieList.append(movieName)
        more = 'n'
        more = input("Want to conti.? ('y' for 'yes'/'n' for 'no') : ")
        more = more.lower()
    return movieList

def representList(lst):
    for i in range(len(lst)):
        print(str(i+1) + ".",lst[i])

def get_movies_from_tastedive(movieName):
    tasteDrive_BaseURL = "https://tastedive.com/api/similar"
    tasteDrive_KeyVal = {"q":movieName, "type":"movies", "limit":5}
    page = requests.get(tasteDrive_BaseURL, params = tasteDrive_KeyVal)
    return json.loads(page.text)

def extract_movie_titles(dict):
    lst = []
    for mdict in dict['Similar']['Results']:
        lst.append(mdict['Name'])
    return lst

def get_related_titles(lst):
    ultimate_list = []
    for movieName in lst:
        recommendedMoviesNameList = extract_movie_titles(get_movies_from_tastedive(movieName))
        for movie in recommendedMoviesNameList:
            if movie not in ultimate_list:
                ultimate_list.append(movie)
    return ultimate_list

def get_movie_data(movieName):
    OMDb_BaseURL = "http://www.omdbapi.com/"
    OMDb_KeyVal = {"t":movieName,"r":"json","apikey":"7880735c"}
    page = requests.get(OMDb_BaseURL, params = OMDb_KeyVal)
    dict = json.loads(page.text)
   # print(json.dumps(page.json(),indent=4))
    return dict

def get_movie_rating(info):
    for dict in info["Ratings"]:
        if dict["Source"] == "Rotten Tomatoes":
            rating = int(dict["Value"][:-1])
            return rating
    rating = 0
    return rating

def get_sorted_recommendations(lst):
    lst5n = get_related_titles(lst)
    ratings = []
    for title in lst5n:
        a = get_movie_rating(get_movie_data(title))
        ratings.append(a)
    zipped = list(zip(lst5n,ratings))
    zippedSorted = sorted(zipped, key = lambda ele : (ele[1],ele[0]),reverse = False)
    zippedSorted = zippedSorted[::-1]
    finalList = []
    for item in zippedSorted:
         finalList.append(item[0])
    print("\nRecommended movies for you :")
    representList(finalList)


list_of_movies = askMovies()
get_sorted_recommendations(list_of_movies)
