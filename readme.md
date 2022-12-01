# Alias
Alias generates a random identity based on the probability of a person of the given age and gender having that forename, of anyone in the USA having that surname, of living in that state, etc.  The philosophy behind this tool is that by using real data and probabilities the resultant identity will be more realistic.

This was written for personal amusement and is admittedly of limited value. If you want something quicker/easier than cloning this project, this web site seems well recommended: https://www.fakenamegenerator.com

Submit an issue if you would like to see something added or changed.

## Data
This is brief synopsis of the data generated and where it came from.

### surname
The surname data is from: https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_North_America#United_States_(American)

### forename
The forename is randomly generated based on the popularity of children's names in the decade the person would have been born.  The source is: https://www.ssa.gov/OACT/babynames/decades These were scraped using Selenium (the code for this is in alias/scripts) for all the decades available (1880-2010).  The scraped data is cached in this repository, so the website is not repeatedly hit.

### middle name and namesake
The middle name is assumed to be a great-grandparent's name, so the name is based on the available name data six decades prior to the data used for the identity.  If that data is not available, then four decades are used and it is assumed that a grandparent is the namesake.  If those data are not available, then the two-decade older are used for the parent's name.  If that is not possible, then the same data source is used, and no namesake is reported.

### mother's maiden name 
The mother's maiden name is generated from the same data as the identity and constrained to be different from the identity's surname.

### home state
The home state probabilities are based on the US population estimates for 2019 from https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population

### birthday
This is a random day that would result in the requested age assuming birthdays are equally distributed   throughout the year. While this is not exactly true, it was deemed sufficient for this exercise. There is a TODO below with reference to data to make results better distributed.

## Usage
    usage: alias [-h] -a AGE [-f] [-m] [-n NUMBER]

    Generates a random identity

    options:
    -h, --help            show this help message and exit
    -a AGE, --age AGE     The person's age
    -f, --female          Choose a female name
    -m, --male            Choose a male name
    -n NUMBER, --number NUMBER
                          Number of identities generated (default is 1)

## Examples
    > python -m alias -ma25
    Lucas T. Scott, a 25-year-old male born on 1997-01-04 (YYYY-MM-DD).
            Lucas's mother's maiden name is Turner, and he is from Texas.
            His middle name is Tommy, named for his great-grandfather.
    > python -m alias -fa30
    Leslie J. Scott, a 30-year-old female born on 1992-02-13 (YYYY-MM-DD).
            Leslie's mother's maiden name is Sullivan, and she is from Nevada.
            Her middle name is Judith, named for her great-grandmother.

## TODO
These are some ideas for the next development tasks in order of likelihood.
 * Could expand to use the forenames WRT state and year from: https://www.ssa.gov/cgi-bin/namesbystate.cgi
    * The state could either be an input, or randomized based on population distributions
    * Would want to scrape the site for the annual data 1960-2021 for each of the 50 states plus DC
    * Use a different file type (JSON or YAML) and store each state's data in one file
    * Could use the state data when possible and then the USA-wide data to extend the range back before 1960
 * Support more of the data available (surnames by race, other nationalities, etc.).
 * The birthday generation assumes an equal probability for each day of the year.  This is a decent assumption, but https://www.panix.com/~murphy/bday.html has data for over 480k birthdays reduced in a way that a better distribution could be implemented here.
