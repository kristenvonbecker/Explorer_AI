# Explorer AI

Explorer AI will be a conversational chatbot which assists and educates visitors to 
[The Exploratorium](https://www.exploratorium.edu/about-us), "a public learning laboratory exploring the world through 
science, art, and human perception."

Generally speaking, Explorer AI will be trained to answer the sorts of questions that 
[a human docent at the Exploratorium](https://www.exploratorium.edu/exhibits/human-phenomena-explainer-station) might 
be asked by a patron. In particular, the bot will be trained to respond to the following categories of user intents:
  - Get a definition, e.g. _"What's depth perception?"_ or _"What does chaos mean?"_
  - Get an explanation, e.g. _"How does condensation work?"_ or _"Why does the earth have magnetic poles?"_
  - Get more information about a(n) (related) exhibit, e.g. _"When was \<this exhibit\> created?"_ or _"Suggest an 
exhibit about sound waves."_
  - Locate an exhibit (in its gallery), e.g. _"Which gallery has the 
[big concave mirror](https://www.exploratorium.edu/exhibits/giant-mirror)?"_ 
or _"I can't find [Albert](https://www.exploratorium.edu/exhibits/albert)."_

Explorer AI will be built on [Rasa](https://rasa.com/docs/rasa/), an open-source framework for conversation-driven 
development, and will use a combination of both pre-trained and custom natural language models to predict responses.
Initially, Explorer AI will be deployed through a simple web application. 


## Data

In addition to information which is specific to the Exploratorium (e.g. exhibit- or gallery-level data), Explorer AI's 
training data must also include plenty of data regarding the individual entities described or illustrated by the 
exhibits (e.g. vision, fog, magnets). Thus, our data will originate from the following two sources:
  - Content scraped from [exploratorium.edu](https://www.exploratorium.edu/). This step will yield Explorer AI's 
institutional knowledge, and bit of analysis will extract dozens of search terms which will be used to seed our
second data source. 
  - Encylopedia articles courtesy of [Encyclopedia Britannica](https://encyclopaediaapi.com/products/index) and 
(possibly) dictionary and thesaurus entries courtesty of [Merriam-Webster](https://dictionaryapi.com/products/index). 
This step will provide the training data for Explorer AI's subject matter knowledge, most of which is scientific in 
nature.

### Web-scraping

In order to get the most relevant information about the Exploratorium and its exhibits, we scrape two URLs: one 
containing [links to each exhibit's webpage](https://www.exploratorium.edu/exhibits/all), and the other 
containing [links to each gallery's webpage](https://www.exploratorium.edu/visit/galleries). These pages are crawled
using Scrapy spiders defined in `data/training_data/get_institutional_data/scrapy_project/project/spiders`.

  - Each item in the exhibit-level data (i.e. each exhibit) has the following fields:
    - `id` is the id of the exhibit (taken from the URL slug)
    - `title` is the title of the exhibit
    - `tagline` is a (catchy) short description
    - `description` gives a brief description of the exhibit
    - `location` gives the (current) location of the exhibit (e.g. gallery) inside the museum, or says that it is not 
currently on view
    - `byline` is the information contained in the line beginning "Exhibit developer(s):"
    - `whats_going_on` is one of the more common headings in the exhibit's "about" section
    - `going_further` is the other common heading
    - `details` stores the text contents of the "about section" whenever it does not contain the previous two features
    - `phenomena` gives a list of phenomena which are illustrated by the exhibit
    - `keywords` gives a list of keywords for the exhibit
    - `collections` gives a list of collections (groupings of exhibits, based on some theme) that the exhibit belongs to
    - `aliases` gives other names that the exhibit might go by
    - `collection_id` gives a list of ids for collections to which the exhibit belongs
    - `related_exhibit_id` gives a list of ids for related exhibits 


  - Each item in the gallery-level data (i.e. each gallery) has the following fields:
    - `id` is the id of the gallery (taken from the URL slug)
    - `title` is the title of the exhibit
    - `tagline` is a catchy short description
    - `description` gives a brief description of the exhibit
    - `curator_url` gives a link to the curators' statement
    - `curator_statement` gives the curators' names and their statement about the gallery
    
The `json` files containing this data are located in `data/training_data/get_institutional_data/data/raw`.
  
In addition to using the scraped data obtain knowledge specific to the Exploratorium's exhibits, we also analyze it
for the purpose of extracting the entities and phenomena which are illustrated by each exhibit.

### Analysis of institutional data


In order to perform the second step of data extraction (API calls to Encyclopedia Britannica and Merriam-Webster), we 
must process and analyze the data obtained through web-scraping. This is accomplished in two ways:
  - The long-form fields (from `exhibits.json` these are `description`, `whats_going_on`, `going_further`, and 
`details`; from `galleries.json` they are `description` and `curator_statement`) are extracted and analyzed using the
[analyzeEntities method](https://cloud.google.com/natural-language/docs/analyzing-entities) available through Google's 
Natural Language API. See `data/training_data/analysis/get_entities.ipynb` for details.
  - The `keywords` and `phenomena` fields in `exhibits.json` are cleaned and tagged (at the word level) with part of
speech (using [NLTK's tagger](https://www.nltk.org/api/nltk.tag.html)) and word sense (done manually, using
the script in `data/training_data/analysis/set_word_sense.py`). See `data/training_data/analysis/pre_process.ipynb` for
details.
