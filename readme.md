# Alias
Generate a random name based on the proportion of the population with that forename and surname. The data is USA based, with the surname data from:
https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_North_America#United_States_(American)

The forename is randomly generated based on the proportional popularity of the child names in the decade the person would have been born.  These are the sources:
https://www.ssa.gov/OACT/babynames/decades/names1980s.html
https://www.ssa.gov/OACT/babynames/decades/names1990s.html

This was written for personal amusement and is admittedly of limited value. If you want something quicker/easier than cloning this project, this web service seems well recommended: https://www.fakenamegenerator.com/

If you do find this project to be useful, submit an issue if you would like to see something added or changed.

## Usage
    usage: alias [-h] -a AGE [-f] [-m] [-n NUMBER]

    Generates a random name

    options:
    -h, --help            show this help message and exit
    -a AGE, --age AGE     The person's age
    -f, --female          Choose a female name
    -m, --male            Choose a male name
    -n NUMBER, --number NUMBER
                            Number of identities generated (default is 1)

## Examples
    > python -m alias -ma 25
    Bryce Brooks, a 25-year-old male born on 1997-06-15 (YYYY-MM-DD).
        Mother's maiden name is: Sullivan
    > python -m alias -fa 30
    Anna Jenkins, a 30-year-old female born on 1992-04-29 (YYYY-MM-DD).
        Mother's maiden name is: Turner

## TODO
 * Support more of the data available (more years, names by race).
 * Could use two or three generations earlier for middle name (grandparent or great-grandparent)
 * Could expand to use the forenames WRT state and decade from: https://www.ssa.gov/cgi-bin/namesbystate.cgi
    * The state could either be an input, or randomized based on population distributions
    * It would be easier to scrape this site than copy the tables
