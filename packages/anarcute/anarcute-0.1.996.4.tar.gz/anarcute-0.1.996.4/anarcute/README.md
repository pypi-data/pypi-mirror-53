My toolbox for dynamic programming

#to be documented
#Chapter: tf-idf

from anarcute import *

import requests, json

sentence="Eat more of those french fries and drink cola"

alice=requests.get("https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt").text

print(tf_idf(sentence,alice))

>> {'eat': 168.7962962962963, 'more': 62.006802721088434, 'of': 5.9111543450064845, 'those': 303.8333333333333, 'french': 759.5833333333333, 'and': 3.4843272171253816, 'drink': 434.047619047619}

#If text is too big it's frequencies can be pre-cached.

filename="alice.json"

vector=vectorize(alice)

open(filename,"w+").write(json.dumps(vector))

vector=json.load(open(filename,"r+"))

print(tf_idf(sentence,vector))

>>{'eat': 168.7962962962902, 'more': 62.00680272108618, 'of': 5.91115434500627, 'those': 303.8333333333223, 'french': 759.5833333333056, 'and': 3.484327217125255, 'drink': 434.0476190476033}



#we can sort by value

print(sort_by_value(tf_idf(sentence,vector)))

>>{'french': 759.5833333332979, 'drink': 434.04761904759886, 'those': 303.8333333333192, 'eat': 168.7962962962885, 'more': 62.006802721085556, 'of': 5.911154345006209, 'and': 3.4843272171252204}


#Chapter: Google

#We have Google Translate and Google Custom Search Engine now

key="MY_GOOGLE_KEY"

gt=GT(key)

gt.translate("pl","en","Jeszcze Polska nie zginęła, Kiedy my żyjemy. Co nam obca przemoc wzięła, Szablą odbierzemy.")

>> {'data': {'translations': [{'translatedText': 'Poland is not dead yet, When we live. What foreign violence has taken from us, we will take away the Saber.'}]}}

cx="MY_CUSTOM_SEARCH_ENGINE_KEY"

gs=GS(cx,key)

gs.search("krakauer sausage recipe")

>> dict with search result, up to 10 items

gs.items("krakauer sausage recipe"")

>> array of results, up to 100 items

#Chapter: Multithreading

#based on multithreading_on_dill library

#let's reverse every string of Alice in Wonderland

url="https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt"

alice=requests.get(url).text

alice_reversed=mapp(lambda s: str(s[::-1]),alice.split('\n'))

#as you see we have no problem with lambda

#by default the number of processes equals to cpu number, but you can make it bigger for highly async tasks or smaller to prevent overload

alice_reversed=mapp(lambda s: str(s[::-1]),alice.split('\n'),processes=2)

#decorator @timeit also included in the library

@timeit

def test(p=None):

    r=mapp(lambda s: math.factorial(150*len(s)),alice.split('\n'),processes=p)

    return None


test()

>> 'test' 2563.11 ms

test(1)

>> 'test' 5287.27 ms


#multithreading filter

alice_special=filterp(lambda s: "alice" in s.lower(),alice.split('\n'))

#run one async function

run(print,["A B C"])

#you can wait for it's result when you need to catch up

p=run(lambda x: request.get(x).text,url)

some_other_stuff()

p.join()

#apply - function that executes functions. Used to run few different functions in one multithreading process

r=mapp(apply,[lambda:requests.get("https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt").text,lambda: math.factorial(9000)])

#Chapter predicates

#in_or(a,b) - returns if at least one element of array is in array/string b

a=["Some","important","array"]

b=["Another","array"]

in_or(a,b)

>> True

c=["Something", "Else"]

in_or(a,c)

>> False

d="Some string"

in_or(a,d)

>> True