# Explorer AI

Explorer AI will be an intelligent chatbot which assists and educates visitors to 
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


## Training data

In addition to information which is specific to the Exploratorium (e.g. exhibit- or gallery-level data), Explorer AI's 
training data must also include plenty of detailed information about the individual entities described or illustrated 
by the exhibits (e.g. vision, fog, magnets). To obtain such training data, we employ a pipeline containing the 
following components:
  - Web-scraping from [exploratorium.edu](https://www.exploratorium.edu/) --  this step provides the required 
institutional-specific data (e.g. exhibit metadata, labeling of exhibits by topic)
  - Processing of institutional data for use with language processing and API calls 
  - API calls to both [Encyclopedia Britannica](https://encyclopaediaapi.com/products/index) and 
[Merriam-Webster](https://dictionaryapi.com/products/index) -- these provide the entity-specific data (i.e. the 
knowledge base) in raw form
  - Processing of knowledge-base data for use with natural language processing and ML modeling purposes

### Web-scraping

Explorer AI's knowledge base should be rooted in each of The Exploratorium's 179 exhibits and the entities that they 
describe or illustrate. Therefore, our data pipeline begins with two webpages on the Exploratorium's website: 
one containing [links to each exhibit's webpage](https://www.exploratorium.edu/exhibits/all), and the other 
containing [links to each gallery's webpage](https://www.exploratorium.edu/visit/galleries). By scraping these pages 
(using Scrapy spiders defined in `project/project/spiders`), we obtain a wealth of information about the exhibits and 
the galleries that contain them:

  - Each item in the file `data/scraped_data/exhibits.json` represents a unique exhibit at the Exploratorium 
(e.g. [Velvet Hands](https://www.exploratorium.edu/exhibits/velvet-hands), 
[Chladni Singing](https://www.exploratorium.edu/exhibits/chladni-singing), or 
[Probably Chelsea](https://www.exploratorium.edu/exhibits/probably-chelsea)). It has the following keys:
  
    - `id` is the (unique) id of the exhibit (taken from the URL slug)
    - `title` is the title of the exhibit
    - `tagline` is a (catchy) short description
    - `description` gives a brief description of the exhibit
    - `location` gives the (current) location of the exhibit (e.g. gallery) inside the museum, or says that it is not 
currently on view
    - `byline` is the information contained in the line beginning "Exhibit developer(s):"
    - `whats_going_on` is one of the more common headings in the exhibit's "about" section; many empty values
    - `going_further` is the other common heading; many empty values
    - `details` stores the text contents of the "about section" whenever it does not contain the previous two features
    - `phenomena` gives a list of phenomena which are illustrated by the exhibit
    - `keywords` gives a list of keywords for the exhibit
    - `collections` gives a list of collections (groupings of exhibits, based on some theme) that the exhibit belongs to
    - `aliases` gives other names that the exhibit might go by; many empty values
    - `collection_id` gives a list of ids for collections to which the exhibit belongs
    - `related_exhibit_id` gives a list of ids for related exhibits
    
  - Each item in the file `data/scraped_data/galleries.json` represents a unique gallery at the Exploratorium 
(e.g. [Gallery 2: Tinkering](https://www.exploratorium.edu/visit/gallery-2) or 
[Gallery 4: Living Systems](https://www.exploratorium.edu/visit/gallery-4)). It has the following keys:
    - `id` is the (unique) id of the gallery (taken from the URL slug)
    - `title` is the title of the exhibit
    - `tagline` is a catchy short description
    - `description` gives a brief description of the exhibit; many empty values
    - `curator_url` gives a link to the curators' statement
    - `curator_statement` gives the curators' names and their statement about the gallery

### Analysis of institutional data

Some data will be needed for API calls, so it is extracted and processed separately. Specifically:
  - The `keywords` and `phenomena` fields in `exhibits.json` will have a lot of affect on how we choose which 
entities our chatbot should have subject matter knowledge over. These fields are processed in `pre_process.ipynb` 
using modules defined in `language_processing.py`. 
  - The long-form fields (from `exhibits.json` these are `description`, `whats_going_on`, `going_further`, and 
`details`; from `galleries.json` they are `description` and `curator_statement`), as well as some others, are 
extracted (for later analysis) in `split_fields.ipynb`. These extracted fields can be found in `data/split_data`. 

In `get_entities.ipynb` we use the 
[analyzeEntities method](https://cloud.google.com/natural-language/docs/analyzing-entities) provided by 
Google's Natural Language API to extract entities from the long-form fields references above. These entities are 
stored in `data/entities/exhibits.json` and `data/entities/galleries.json`. 

Finally, some additional data processing is performed in `data_exploration.ipynb`. 

### Querying knowledge sources
Using the entities obtained from the Natural Language API, as well as keywords and phenomena contained in the scraped 
data, we query the encyclopedia and dictionary APIs to obtain articles about and definitions of topics related to the 
Exploratorium's exhibits.

The files `get_article_lists.ipynb` and `get_articles.ipynb` contain API calls. Not all of the code is currently 
fuctional. 