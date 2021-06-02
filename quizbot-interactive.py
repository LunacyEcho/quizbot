#!/usr/bin/env python3

# CMPU 366, Spring 2021

import nltk
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas
import re
import ftfy
import time
import sys
import math
import select

train_file = sys.argv[1]
game_file = sys.argv[2]


#### SETTINGS ####

test_fracs = False # make true to run tests on various fractions of TUs
remove_stopwords = True # make true to remove stopwords
playgame = True # make true to enable game
guess_threshold = 0.1 # change this to adjust the certainty threshold at which quizbot buzzes
chunk_size = 1 # changes number of new words that show up each iteration
set_word_speed = 0.3 # change this to make words appear faster or slower


# import training file here
b_data = pandas.read_csv(train_file)

def ftfy_csv(csv):
    for x in csv['text']:
        x = ftfy.fix_text(x)
    for x in csv['page']:
        x = ftfy.fix_text(x)
    return csv

print("Loading questions...")
b_data = ftfy_csv(b_data)

def clean_text(text):
    text = text.lower()

    text = re.sub(r'[_"“”…\-;%()|+&=*%.,!?:\[\]/]', ' ', text)
    text = re.sub(r"for 10 points", '', text)
    text = re.sub(r"'s", '', text)

    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
    
    text = nltk.WordPunctTokenizer().tokenize(text)

    return text

b_data['cleaned_text'] = list(map(clean_text, b_data['text']))

q_train, q_test = sklearn.model_selection.train_test_split(b_data, train_size = 0.8, random_state=13)

big_train = False

if len(b_data['cleaned_text']) > 15000:
    print("Training quizbot... (this may take a while!)")
    big_train = True
else: print("Training quizbot...")

bow_uni_transform = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
X_tr_bow = bow_uni_transform.fit_transform(q_train['cleaned_text'])
X_te_bow = bow_uni_transform.transform(q_test['cleaned_text'])
y_tr_bow = q_train['page']
y_te_bow = q_test['page']

X_all = bow_uni_transform.transform(b_data['cleaned_text'])
y_all = b_data['page']

def random_forest_for_test(X_tr, y_tr, X_test, y_test, description):
    model = RandomForestClassifier().fit(X_tr, y_tr)
    score = model.score(X_test, y_test)
    print('Test Score with', description, 'features', score)
    return model

def random_forest_for_game(X, y):
    model = RandomForestClassifier().fit(X, y)
    return model

# takes in cleaned list of TUs, returns shortened list of TUs
def fraction_tossup(tu_list, frac):
    new_tu_list = []
    for tu in tu_list:
        new_tu_list.append(tu[:math.ceil(frac*len(tu))])
    return new_tu_list

fracs = [1/3, 1/2, 2/3, 3/4, 4/5, 1]

if test_fracs:
    X_tr_one_third, X_tr_one_half, X_tr_two_thirds, X_tr_three_fourths, X_tr_four_fifths, X_tr_full = [bow_uni_transform.transform(fraction_tossup(q_test['cleaned_text'], x)) for x in fracs]

    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_one_third, y_te_bow, "1/3 tossup length")
    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_one_half, y_te_bow, "1/2 tossup length")
    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_two_thirds, y_te_bow, "2/3 tossup length")
    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_three_fourths, y_te_bow, "3/4 tossup length")
    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_four_fifths, y_te_bow, "4/5 tossup length")
    random_forest_for_test(X_tr_bow, y_tr_bow, X_tr_full, y_te_bow, "full tossup length")

model_rf_game = random_forest_for_game(X_all, y_all)


# plays a game of quizbowl
def game(match_tus):
    # match_tus = pandas.read_csv(questions)
    # certainty = 0
    
    print("\n")
    print("=========================================================")
    print("==                                                     ==")
    print("==                LET THE GAME BEGIN!!!                ==")
    print("==                                                     ==")
    print("=========================================================")
    print("\n")

    input("Press any key to start!\n")
    
    next_tossup = True
    tu_no = 0

    while next_tossup:
        tu = match_tus.iloc[tu_no, 0]
        answer = match_tus.iloc[tu_no, 1]
        tossup(tu, tu_no, answer)

        if(tu_no < len(match_tus)-1):
            response = input("Next tossup? Press Q to quit.\n")
            if response.lower() == "q":
                next_tossup = False
                print("Thanks for playing!")
            else:
                tu_no += 1
        else:
            print("That's the game! Thanks for playing!")
            next_tossup = False

def tossup(tu, tu_no, answer):
    print("Tossup", tu_no+1)
    print("\n")
    time.sleep(1)
    num_words = len(tu.split())
    start_num = 0
    end_num = chunk_size
    stop_tu = False
    bot_guessed = False
    player_guessed = False
    word_speed = set_word_speed
    while (end_num <= num_words) & (not stop_tu) & (not (player_guessed & bot_guessed)): 
        tu_so_far = tu.split()[:end_num]
        stop_tu, bot_guessed = show_words(tu_so_far, answer, start_num, end_num, bot_guessed)
        if end_num == num_words: word_speed = 5 # five seconds after a tossup is finished to buzz in
        i, o, e = select.select( [sys.stdin], [], [], word_speed ) 
        if i:
            input()
            if player_guessed:
                print("You already guessed for this tossup!")
                start_num += chunk_size
                end_num += chunk_size
            else:
                response = input("You buzzed! What is your answer?\n")
                print("You guessed:", response)
                time.sleep(1)
                print("The correct response was:", answer)
                time.sleep(1)
                y_or_n = input("Were you right? Press Y/N\n")
                if (y_or_n.lower() == 'y'):
                    print("Congrats!")
                    stop_tu = True
                else: 
                    print("Sorry :(")
                    player_guessed = True
        else:
            start_num += chunk_size
            end_num += chunk_size

    if not stop_tu: show_words(tu_so_far, answer, end_num, num_words, bot_guessed)
    if ((not player_guessed) & (not bot_guessed)) | (player_guessed & bot_guessed):
        print("\nNo one got it! The answer was:", answer)
        time.sleep(1)

def show_words(tu, answer, start, end, bot_guessed):
    tu_words = ' '.join(tu)
    tu_print = ' '.join(tu[start:end])
    threshold = guess_threshold
    print(tu_print, end = ' ', flush = True)
    stop_tu = False
    tu_array = bow_uni_transform.transform([clean_text(tu_words)])
    guess = model_rf_game.predict(tu_array)
    prob = max(model_rf_game.predict_proba(tu_array)[0])

    # dynamically changing the certainty threshold to avoid silly guesses at the starts of tossups when there's lots of training data
    if big_train:
        if (start < 50):
            threshold = guess_threshold + 0.5 - (start/100)

    if (prob > threshold) & (not bot_guessed) & (start > 10): 
        stop_tu = buzz(guess[0], answer, prob)
        bot_guessed = True
    return stop_tu, bot_guessed

def buzz(guess, answer, certainty):
    is_right = False
    print("\nBUZZ!")
    time.sleep(1)
    print("My guess is:", guess)
    time.sleep(1)
    print("...")
    time.sleep(1)
    if guess == answer:
        print("Hooray! I'm right!")
        time.sleep(1)
        is_right = True
    else: 
        print("Oh no! I'm wrong!")
        time.sleep(1)
    print("My certainty was:", certainty)
    time.sleep(1)
    return is_right

if playgame:
    match_qs = ftfy_csv(pandas.read_csv(game_file))
    game(match_qs)









