"""
TODO: add more decades
TODO: middle name based on two or three generations before birth
"""
import csv
import datetime
import math
import os
import random
import string

MIN_USA_FORENAME_DECADE = 1880
MAX_USA_FORENAME_DECADE = 2010


class Identity(object):
    def __init__(self, age, nationality, race, gender):
        self.nationality = nationality.upper()
        if self.nationality != "USA":
            raise ValueError("USA is the only supported nationality so far")
        self.gender = gender.upper()
        if gender not in ("MALE", "FEMALE"):
            raise ValueError(
                "MALE and FEMALE are the only supported gender labels due to reporting data, sorry"
            )
        self.age = int(age)
        self.birthday = None
        self.forename = None
        self.middleName = None
        self.surname = None
        self.mothersMaidenName = None
        self.homeState = None
        self.kindergardenStartDate = None
        self.highschoolGradDate = None
        self.rollIdentity()

    def printInfo(self):
        if self.gender == "MALE":
            subjectivePronoun = "his"
            objectivePronoun = "he"
        else:
            subjectivePronoun = "her"
            objectivePronoun = "she"
        print(
            f"{self.forename} {self.middleName[0]}. {self.surname}, a {self.age}-year-old {self.gender.lower()} born on {self.birthday} (YYYY-MM-DD)."
        )
        print(
            f"\t{self.forename}'s mother's maiden name is {self.mothersMaidenName}, and {objectivePronoun} is from {self.homeState}."
        )
        if self.namesake:
            print(
                f"\t{string.capwords(subjectivePronoun)} middle name is {self.middleName}, named for {subjectivePronoun} {self.namesake}."
            )
        else:
            print(
                f"\t{string.capwords(subjectivePronoun)} middle name is {self.middleName}."
            )
        eduStr = f"\t{string.capwords(objectivePronoun)} started kindergarden in the fall of {self.kindergardenStartDate}"
        eduStr += f" and graduated from high school in the spring of {self.highschoolGradDate}."
        print(eduStr)

    def rollIdentity(self):
        self.birthday = rollBirthDay(self.age)
        self.forename = rollForename(self.birthday.year, self.nationality, self.gender)
        self.middleName, self.namesake = rollMiddleName(
            self.birthday.year, self.nationality, self.gender
        )
        self.surname = rollSurname(self.nationality)
        self.mothersMaidenName = self.surname
        while self.surname == self.mothersMaidenName:
            self.mothersMaidenName = rollSurname(self.nationality)
        self.homeState = rollState(self.nationality)
        self.kindergardenStartDate, self.highschoolGradDate = rollEducation(
            self.birthday, self.nationality, self.homeState
        )


def rollBirthDay(age):
    """Generate a random birthday given an age"""
    date = datetime.datetime.now().date()
    yearStart = date - datetime.timedelta((age + 1) * 365.2425)
    yearEnd = date - datetime.timedelta(age * 365.2425)
    totalDays = (yearEnd - yearStart).days
    return yearStart + datetime.timedelta(days=random.randrange(totalDays))


def rollForename(birthYear, nationality, gender):
    """Generate a random forename based on decade of birth, nationality and gender
    Currently only support MALE and FEMALE genders and a nationality of USA
    Birth decades are also limited, but the data is easy to generate
    """
    if gender not in ("MALE", "FEMALE"):
        raise ValueError(
            "Only rollForename only supports gender values of 'MALE' and 'FEMALE'"
        )
    if nationality not in ("USA"):
        raise ValueError("Only rollForename only supports a nationality value of 'USA'")

    fileName = f"forenames_{10*math.floor(birthYear/10.)}s.csv"
    filePath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"data_{nationality}",
        fileName,
    )
    if not os.path.isfile(filePath):
        raise ValueError(
            f"The forename file: {filePath} does not exist.  Check the age and nationality."
        )

    if gender == "MALE":
        nameIdx = 1
        numberIdx = 2
    else:  # "FEMALE"
        nameIdx = 3
        numberIdx = 4

    names = []
    numbers = []
    total = 0
    with open(filePath) as csv_file:
        data = csv.reader(csv_file, delimiter=",", quotechar='"')
        for line in data:
            if not line[0].isdigit():
                continue  # ignore lines without a number in first column
            else:
                names.append(line[nameIdx])
                number = int(line[numberIdx])
                total += number
                numbers.append(number)

    accum = 0.0
    forename = None
    rollFore = random.random()
    for (name, number) in zip(
        names,
        numbers,
    ):
        accum += number / total
        if not forename and accum > rollFore:
            forename = name

    return forename


def rollMiddleName(birthYear, nationality, gender):
    birthDecade = 10 * math.floor(birthYear / 10.0)
    pDecade = birthDecade - 20  # parent decade
    gpDecade = pDecade - 20  # grandparent decade
    ggpDecade = gpDecade - 20  # great-grandparent decade
    if gender == "MALE":
        root = "father"
    else:
        root = "mother"
    if ggpDecade >= MIN_USA_FORENAME_DECADE:
        namesake = f"great-grand{root}"
        middleName = rollForename(ggpDecade, nationality, gender)
    elif gpDecade >= MIN_USA_FORENAME_DECADE:
        namesake = f"grand{root}"
        middleName = rollForename(gpDecade, nationality, gender)
    elif pDecade >= MIN_USA_FORENAME_DECADE:
        namesake = root
        middleName = rollForename(pDecade, nationality, gender)
    else:
        namesake = None
        middleName = rollForename(birthDecade, nationality, gender)
    return middleName, namesake


def rollSurname(nationality):
    """Generate a random surname given a nationality
    Currently the only nationality supported is USA
    """
    if nationality not in ("USA"):
        raise ValueError("Only rollSurname only supports a nationality value of 'USA'")
    filePath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"data_{nationality}",
        "surnames.csv",
    )
    if not os.path.isfile(filePath):
        raise ValueError(f"The surname file: {filePath} does not exist.")
    with open(filePath) as csv_file:
        surnames = []
        whiteNumbers = []
        whiteTotal = 0
        data = csv.reader(csv_file, delimiter=",", quotechar='"')
        for line in data:
            if len(line) < 2:
                continue
            try:
                whiteNumber = float(line[1])
            except ValueError:
                continue
            surnames.append(line[0])
            whiteTotal += whiteNumber
            whiteNumbers.append(whiteNumber)

    wAccum = 0.0
    surname = None
    rollSur = random.random()
    for (sName, whiteNumber) in zip(surnames, whiteNumbers):
        wAccum += whiteNumber / whiteTotal
        if wAccum > rollSur:
            surname = sName
            break
    return surname


def rollState(nationality):
    """Generate a random state given a nationality
    Currently the only nationality supported is USA
    """
    if nationality not in ("USA"):
        raise ValueError("Only rollState only supports a nationality value of 'USA'")
    filePath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"data_{nationality}",
        "states.csv",
    )
    if not os.path.isfile(filePath):
        raise ValueError(f"The file: {filePath} does not exist.")
    with open(filePath) as csv_file:
        states = []
        numbers = []
        total = 0
        data = csv.reader(csv_file, delimiter=",", quotechar='"')
        for line in data:
            if len(line) < 3:
                continue
            try:
                number = float(line[2])
            except ValueError:
                continue
            states.append(line[1])
            total += number
            numbers.append(number)

    accum = 0.0
    homeState = None
    rollState = random.random()
    for (state, number) in zip(states, numbers):
        accum += number / total
        if accum > rollState:
            homeState = state
            break
    return homeState


def rollEducation(birthday, nationality, state):
    if nationality not in ("USA"):
        raise ValueError("Only rollState only supports a nationality value of 'USA'")

    filePath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"data_{nationality}",
        "kindergarden.csv",
    )
    if not os.path.isfile(filePath):
        raise ValueError(f"The file: {filePath} does not exist.")

    condition = None
    conditionalDateStr = None
    with open(filePath) as csv_file:
        data = csv.reader(csv_file, delimiter=",", quotechar='"')
        for line in data:
            if len(line) < 3:
                continue
            if line[0] == state:
                condition = line[1]
                conditionalDateStr = line[2]
                break

    if condition in ("LEA", "N/A"):
        # use most strict condition and date since it is more likely to be held back than to start early
        # LEA stands for Local Educational Authority
        condition = "5_before"
        conditionalDateStr = "7/31"
    elif condition in ("5"):
        # only Vermont
        # this reference suggests that New England schools typically start between Aug 26 and Aug 30
        # https://www.pewresearch.org/fact-tank/2019/08/14/back-to-school-dates-u-s/
        # use still most the strict condition and date since it is more likely to be held back than to start early
        condition = "5_before"
        conditionalDateStr = "7/31"

    birthyearPlus5 = birthday.year + 5
    conditionalMonth, conditionalDay = conditionalDateStr.split("/")
    conditionalDate = datetime.date(
        birthyearPlus5, int(conditionalMonth), int(conditionalDay)
    )

    kgCheck = datetime.date(birthyearPlus5, birthday.month, birthday.day)
    if condition in ("5_on_or_before", "5_on"):
        if conditionalDate >= kgCheck:
            kindergardenStartYear = birthyearPlus5
        else:
            kindergardenStartYear = birthyearPlus5 + 1
    elif condition in ("5_by", "5_prior_to", "5_before"):
        if conditionalDate > kgCheck:
            kindergardenStartYear = birthyearPlus5
        else:
            kindergardenStartYear = birthyearPlus5 + 1
    else:
        raise Exception("Unknown conditions for kindergarden start")
    highSchoolGradYear = kindergardenStartYear + 13

    return kindergardenStartYear, highSchoolGradYear
