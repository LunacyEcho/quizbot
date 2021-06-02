# QUIZBOT

### TL;DR

To install dependencies: `pip install ntlk sklearn pandas re ftfy time sys math`
Also download: `nltk.download('stopwords')`
To watch Quizbot play tossups: `python3 quizbot.py [training file] [game file]`
To play against Quizbot: `python3 quizbot-interactive.py [training file] [game file]`

Sample interactive game (3 minutes to train) | `python3 quizbot-interactive.py tossups-for-train/all-tossups.csv tossups-for-game/all-game.csv`
Sample interactive game (1 minute to train) | `python3 quizbot-interactive.py tossups-for-train/all-tossups-small.csv tossups-for-game/all-game-small.csv`

### What's this?

Say hello to Quizbot, the latest program to join the question-answering ranks of WATSON, QANTA, and more! At its core, Quizbot is a program that uses a classifier to answer quizbowl questions. Each "question" contains multiple sentences containing clues going from more to less obscure, all in order to describe a particular thing that a player of the game is trying to guess. IRL quizbowl players use buzzers to "buzz in" when they want to have a guess at the answer, usually interrupting the reader before they finish. Quizbot plays quizbowl similarly to human players, "hearing" questions one word at a time, and "buzzing in" with a guess once it feels certain enough that it knows the answer.

Quizbot was coded in Python and runs a Random Forest Classifier on a file of training questions to learn how to new questions. 

### Before Running Quizbot

Before running Quizbot, make sure to install the following libraries: nltk, sklearn, pandas, ftfy, time, sys, math. Each can be installed by running `pip install [libraryname]` from the command line. 

### quizbot.py

This is a program that demonstrates Quizbot's ability to answer questions, but without the functionality for a user to play along. To run quizbot.py, run `quizbot.py [training file] [game file]`, with the both the training file and the game file being .csv files with two columns—one labeled `text` where each row contains the full text of a tossup, and the other labeled `page` with each row containing the text of title of the Wikipedia page associated with the correct answer (e.g. "Alexander_the_Great" or "Ulysses_(novel)").

Near the top of the actual code file are a number of adjustable settings that you can change to adjust the way quizbot.py runs.
1. `test_fracs` - When true, Quizbot displays, based on the training data, how accurate it is when only operating of fractions of a tossup. This is meant to simulate how accurate Quizbot would be if it were to "buzz in" at, in order, 1/3, 1/2, 2/3, 3/4, 4/5, and all of a tossup. The default value is `False`. 
2. `remove_stopwords` - When true, Quizbot removes common English words from the training text based on the nltk list of stopwords. It is recommended to keep this at the default value, which is `True`. 
3. `playgame` - When true, Quizbot plays a game of quizbowl based on the game file. This option can be toggled off when one just wants to test its accuracy without playing a game. The default value is `True`. 
4. `guess_threshold` - This is the accuracy threshold that, when playing a game, Quizbot has to reach before guessing an answer. Adjusting this value makes Quizbot more or less willing to take risks. This must be a value between 0 and 1, and the default value (which assumes a training data set of at least 2,000 tossups) is `0.1`.  
5. `chunk_size` - This is the number of words that a game tossup advances by for every iteration. The default value is `5`. 
6. `set_word_speed` - This is the number of seconds that pass by between iterations of chunks of words during game tossups. The default value is `1.2`. 

### quizbot-interactive.py

This is a program that allows the user to play a game of quizbowl against Quizbot. The way to run the game is the same as for `quizbot.py` (you run `quizbot.py [training file] [game file]`). To play along, you start the game as usual. To buzz, you press `Enter`, and you type out your answer. The console reveals to you what the actual answer is (without telling Quizbot!), and you confirm whether you're right or wrong (honor system here, essentially). Both you and Quizbot only get one guess, as per regular quizbowl rules. 

Sample game files are in the `tossups-for-game` folder; you can also make your own game files by formatting a .csv file as described above (having two columns, one for `text` and one for `page`). 

Near the top of the code file are a number of adjustable settings that are similar to those in `quizbot.py`. The only differences are that `chunk_size` defaults to `1` (only displaying one word at a time), and that `set_word_speed` defaults to `0.5`. 

### Details for Game Playing

In the `tossups-for-train` folder, there are a number of different .csv files each containing a large number of tossups that can be used to train Quizbot. There are subject-specific training files, including the "Big Three" subjects of Literature (`lit-tossups.csv`), History (`hist-tossups.csv`), and Science (`sci-tossups.csv`), as well as files for the subjects of Fine Arts (`arts-tossups.csv`), Geography (`geo.tossups.csv`), Mythology (`myth-tossups.csv`), Religion (`rel-tossups.csv`), and Social Science (`socsci-tossups.csv`). `tossups-for-train` also contains larger training files for all-subject games. `all-lhs-tossups.csv` contains all of the tossups in the Big Three training files (30k tossups, takes about 2.5 minutes to train), while `all-tossups.csv` contains tossups from all of the other training files (many were further filtered because otherwise the file would be too big; as it stands, `all-tossups.csv` contains 33k tossups and takes about 3 minutes to train). 

In the `tossups-for-game` folder, there are a number of small game files consisting of ~5-10 tossups each. There is one game file for each of the subjects, as well as a longer game file (63 tossups) combining all the tossups from the smaller game files. If you were to create your own game file, this is the folder where it should go.
If you're just starting your exploration into Quizbot, training on `tossups-for-train/all-tossups.csv` and having a game file of `tossups-for-game/all-game.csv` would be a good place to start! (Although if you're short on time, training/running on a single subject would be faster.)
