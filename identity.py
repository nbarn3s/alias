"""
TODO: add more decades
TODO: middle name based on two or three generations before birth
"""
import csv
import datetime
import math
import os
import random


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
        self.forname = None
        self.surname = None
        self.mothersMaidenName = None
        self.rollIdentity()

    def printInfo(self):
        print(
            f"{self.forname} {self.surname}, a {self.age}-year-old {self.gender.lower()} born on {self.birthday} (YYYY-MM-DD)."
        )
        print(f"\tMother's maiden name is: {self.mothersMaidenName}")

    def rollIdentity(self):
        self.birthday = rollBirthDay(self.age)
        self.forname = rollForename(self.birthday.year, self.nationality, self.gender)
        self.surname = rollSurname(self.nationality)
        self.mothersMaidenName = self.surname
        while self.surname == self.mothersMaidenName:
            self.mothersMaidenName = rollSurname(self.nationality)


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
    forname = None
    rollFore = random.random()
    for (name, number) in zip(
        names,
        numbers,
    ):
        accum += number / total
        if not forname and accum > rollFore:
            forname = name

    return forname


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
