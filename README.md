# Docent AI

Docent AI will be an intelligent virtual museum guide which assists, educates, and entertains visitors to 
[The Exploratorium](https://www.exploratorium.edu/), a science museum in San Francisco.

## Data sources

### Web-scraping
The data for Docent AI's knowledge base will be rooted in each of The Exploratorium's 179 exhibits. To seed the 
knowledge base, two pages of the Exploratorium's website were scraped using the Scrapy framework: 
one with [links to each exhibit's page](https://www.exploratorium.edu/exhibits/all), and the other with 
[links to each gallery's page](https://www.exploratorium.edu/visit/galleries). Viewing a gallery as a collection of 
exhibits, it is hoped that the resulting data structure will reflect a more holistic view of the museum's exhibits.

Each item in `data/scraped_data/exhibits.json` represents a unique exhibit. 
  - `id` is the (unique) id of the exhibit
  - `title` is the title of the exhibit
  - `tagline` is a (catchy) short description
  - `description` gives a brief description of the exhibit
  - `location` gives the (current) location of the exhibit (e.g. gallery) inside the museum, or says that it is not currently on view
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

Each item in  `data/scraped_data/galleries.json` represents a unique gallery.
  - `id` is the (unique) id of the gallery
  - `title` is the title of the exhibit
  - `tagline` is a catchy short description
  - `description` gives a brief description of the exhibit; many empty values
  - `curator_url` gives a link to the curators' statement
  - `curator_statement` gives the curators' names and their statement about the gallery

### Entity-analysis of scraped data
Using the [analyzeEntities method](https://cloud.google.com/natural-language/docs/analyzing-entities) provided by 
Google's Natural Language API, selected text fields of the exhibits and galleries data (contained in the fileds 
described above) are analyzed. From the exhibit-level data, we analyze `tagline`, `description`, `byline`, 
`whats_going_on`, `going_further`, and `details`. From the gallery-level data, we analyze `tagline`, `description`, 
and `curator_statement`. 

In order to structure the API calls, we must parse the relevant data into separate text files. The directory 
`data/split_data/` contains these text files. The file names of these files correspond to the `id` field of the 
relevant exhibit or gallery.

Each item in `data/entities/exhibits.json` represents the entities corresponding to one field of one exhibit. 
Each item in `data/entities/galleries.json` represents the entities corresponding to one field of one gallery. 

### Querying knowledge sources
Using the entities obtained from the Natural Language API, as well as keywords and phenomena contained in the 
scraped data, we can query the [Encyclopedia Britannica API](https://encyclopaediaapi.com/products/index) to obtain 
articles about topics related to the Exploratorium's exhibits.