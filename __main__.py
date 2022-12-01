import argparse
from alias.identity import Identity

parser = argparse.ArgumentParser(
    prog="alias", description="Generates a random identity"
)
parser.add_argument("-a", "--age", type=int, required=True, help="The person's age")
parser.add_argument("-f", "--female", action="store_true", help="Choose a female name")
parser.add_argument("-m", "--male", action="store_true", help="Choose a male name")
parser.add_argument(
    "-n",
    "--number",
    type=int,
    default=1,
    help="Number of identies generated (default is 1)",
)
args = parser.parse_args()

# error handle the arguments
if args.male == args.female:
    print("The male and female options are mutually exclusive and one is required.")
    parser.print_help()
    exit(1)
if args.number < 1:
    print("The number of identies should be one or greater.")
    parser.print_help()
    exit(1)

# only handling this data so far MALE|FEMALE, USA, WHITE
if args.male:
    gender = "MALE"
else:
    gender = "FEMALE"
nationality = "USA"
race = "WHITE"

identity = Identity(args.age, nationality, race, gender)
for _ in range(args.number):
    identity.rollIdentity()
    identity.printInfo()
