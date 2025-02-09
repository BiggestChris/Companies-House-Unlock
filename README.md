# Companies House Unlock
 
## Summary:

This Tool works by calling the Companies House API to search Director Records and then grouping the results (and their companies) by Date of Birth (DoB). This has been deployed at https://companies-house-unlock.onrender.com/ - albeit this is using a free-tier hosting service via Render, and so may take up to 60 seconds to spin up when activated, and may strain under high volumes of traffic.


## Background:

### Problem:

Companies House has a deficiency in that it isn't using immutable unique IDs to track individuals as Directors. In many cases, when a Director is registered, if the details aren't exactly the same (First name/ Middle names / Last names/ Address) then it will just create a new record, rather than append the existing Director record. This makes it easy for bad actors to intentionally obfuscate their directorshop of multiple companies. In essence, if I want to find out _all_ the directorships a person holds, I need to search for that person, and look up all possible records individually, creating manual work and creating high risk of missing a directorship.

### Solution:

Companies House Unlock calls the Companies House API to retrieve the same search results as if searching for a Director, but it groups all of those records together by Date of Birth, so if an individual has multiple director records with slightly different names/addresses, it will group all of those together. It also pulls together all the companies results in one place - this means that you can see all of the Directorships held by an individual at once, thus removing the manual work of finding them and mitigating the risk of missing a directorship.

### Limitations:

1. This is entirely dependent on the Companies House API and its own search function.
2. If a Director has managed to avoid submitting DoB for some records and not others, then they will not be grouped together.
3. This will group together different people who share the same DoB and appear in the same Companies House search results (i.e. two John Smiths with the same DoB).
4. It is always advisable to manually check results directly on Companies House and this app should not be solely relied upon. No responsibility is taken for incorrect information given by the app.

## How to use:
1. Go to the homepage and type in the name of the Director to search - please enter in the format *'First name'* *(Optional)'Middle name/s'* *'Last name'*.
2. (It has been found that the search function works for legal entities as well as individuals, but it has been designed for individuals in mind). 
3. Click _Search_.
4. Wait for results to load (whilst the app calls the Companies House API, this can take up to 60-120 seconds depending upon the size of the results).
5. The page will automatically refresh when results appear, scroll down to look at all the Director groupings.
6. Each Director grouping will show the Director record search results with the same Date of Birth, listing the Director name, Address, Birth Month and Officer ID.
7. Underneath it will show all the companies with directorships of the above records together, for each company it will state the Name, Company number, Status and Incorporation date.
8. Clicking on a Director name will you to its page on Companies House, similarly clicking on a Company name will take you to its page on Companies House.
9. All of those results without a Date of Birth will be grouped together at the bottom of the search results.


## Codebase:

The Codebase for this app uses the Flask framework with Python and Bootstrap CSS.

**/static/** - Thise houses the CSS used for the Site


**/templates/** - This houses the HTML templates used for the application:
* _index.html_ - This is the search page for the app - with a form to submit text to search.
* _layout.html_ - This is the general template for the Flask app, includes the Navbar.
* _results.html_ - This is the results page for the app - it retrieves the sorted search results from the API and loads in via blocks based upon the grouped results.

**/app.py** - This houses the main Flask framework calling and routing. It also calls the functions defined in _functions.py_ to perform the search and stores the results via Flask session (to accomodate multiple users). The grouping together of results happens here as well.

**/functions.py** - This houses the functions that call the Companies House API for searching and retrieving details.

**/requirements.txt** - This houses the necessary Python libraries needed to run the app.

**/test_apy.py** - A separate test script that was used for testing the Companies House API is working via the search function.



## Further notes:
* The first version of this app was originally created as an entry to the [Inversity](https://inversity.co/) challenge on Open-Source Investigation sponsored by [Bellingcat](https://www.bellingcat.com/).

* Original [submission video for the challenge](https://youtu.be/CZkafTg99mQ) to Inversity 

* [Companies House Officer Summary API Page](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/officersummary?v=latest)