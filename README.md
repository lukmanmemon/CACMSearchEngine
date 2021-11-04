# CPS842 Final Assignment Readme - Runtime Instructions

## Eval  Program - eval.py
This program requires two (2) command line arguments when running it in the form of either ON/OFF to represent whether to use the smaller list of stopwords or to use the porter stemming algorithm respectively. To successfully run, it requires the python modules ```numpy``` and ```nltk``` to be installed via pip.

This program essentially calls invert.py, and search.py and pipes the necessary input from ```query.txt``` and ```qrels.text``` to arrive at the Average MAP and R-Precision values.

Example: (The following runs the program using the shorter list of stopwords AND also the porter stemming algortithm enabled

```
...\cps842_final_assignment> python3 eval.py ON ON
```

## User Interface Programs

### Django Web Server

The Django web server has the required dependencies under ```web/engine/requirements.txt``` that allows it to run and complete user requests. The API listens by default on port ```8000``` for GET requests with the the parameters of ```query``` representing the search query that will be cleaned and normalized. The optional parameters are ```stopwords``` and ```stemming``` to turn on the smaller list of stopwords and whether or not to use the PS algorithm. By default, these values are set to OFF. The equivalent of ```search.py``` is run through the server code.

The server also requires that ```django-cors-headers``` be installed via pip to allow cross origin access from the same local machine to align with the options in ```settings.py```

**To start/run the server:**

```
cd web/engine
python3 manage.py runserver
```

**Sample Web Request:**
```
http://localhost:8000/search/?query=user&stemming=ON
```
**Sample Web Response:**
```
{"1": {"Rank": "1", "Document": "153", "Score": "1.0", "Title": "Comments from a FORTRAN User", "Author(s)": "Blatt, J. M."}, "2": {"Rank": "2", "Document": "254", "Score": "1.0", "Title": "SMALGOL-61", "Author(s)": "Bachelork, G. A. Dempster, J. R. H. Knuth, D. E. Speroni, J."}, "3": {"Rank": "3", "Document": "300", "Score": "1.0", "Title": "COBOL: A Sample Problem", "Author(s)": "Mackinson, T. N."}, "4": {"Rank": "4", "Document": "322", "Score": "1.0", "Title": "Operational Compatibility of Systems-CONVENTIONS", "Author(s)": "Bright, H. S."}, "5": {"Rank": "5", "Document": "698", "Score": "1.0", "Title": "DATA-DIAL: Two-Way Communication with", "Author(s)": "Marill, T. Edwards, D. Feurzeig, W."}, "6": {"Rank": "6", "Document": "1010", "Score": "1.0", "Title": "A Multiuser Computation Facility for Education and Research", "Author(s)": "Dennis, J. B."}, "7": {"Rank": "7", "Document": "1033", "Score": "1.0", "Title": "Experimental Personalized Array Translator System", "Author(s)": "Hellerman, H."}, "8": {"Rank": "8", "Document": "1043", "Score": "1.0", "Title": "Talk-A High-Level Source Language Debugging", "Author(s)": "verSteeg, R. L."}, "9": {"Rank": "9", "Document": "1071", "Score": "1.0", "Title": "Computer-Usage Accounting for Generalized Time-Sharing Systems", "Author(s)": "Rosenberg, A. M."}, "10": {"Rank": "10", "Document": "1160", "Score": "1.0", "Title": "CAT: A 7090-3600 Computer-Aided Translation", "Author(s)": "Wilson, D. M. Moss, D. J."}, "Time": 244.05893063545227}
```


### React Front-end Client

The React front end client can be build using ```npm run build``` within the ```web/client``` directory. For convenience, we have provided both the source code and the prebuilt build folder so as to minimize toolchain installation/prerequisites.

It can then be served as follows: 

```
The build folder is ready to be deployed.
You may serve it with a static server:

  npm install -g serve
  serve -s build
```

Otherwise, if you'd like to build from scratch, ```npm i``` within ```web/client``` and ```npm start``` following that to run the client.

The interface is fairly intuitive with the search bar allowing for queries which will populate the ```query``` parameter as shown above. The checkboxes turn on the optional flags to send to the API, whether the stemming and stopwords need to be enabled

**Enter Search Query and Set Flags:**
![Alt text](screenshots/input.png?raw=true)

**Searching For Results:**
![Alt text](screenshots/loading.png?raw=true)

**Displayed Results:**
![Alt text](screenshots/results.png?raw=true)




