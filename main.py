import argparse
import os
import shutil
import pandas as pd
from pandas import Series
from typing import Any
from numpy import ndarray
from numpy.random import default_rng


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description='Koppelt leden van een klas met andere leden in een '
                    'willekeurige volgorde op basis van een CSV bestand met alle gegevens.')
    # Add the arguments positional and optional
    parser.add_argument('-f', '--filepath', metavar='', help='Pad naar het CSV bestand', required=True)
    parser.add_argument('-o', '--outputfolder', metavar='', help='Pad naar de uitvoer map', required=True)
    # Parse the arguments
    args = parser.parse_args()
    # Initialize the random number generator
    rng = default_rng()
    bit_generator = rng.bit_generator
    # Initialize the output folder and input file variables
    output_folder = args.outputfolder + "\\vriendjesweek_uitvoer"
    name_folder = output_folder + "\\namen"
    email_folder = output_folder + "\\emailadressen"
    csv_file_path = args.filepath
    # set up the directory structure
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    os.mkdir(name_folder)
    os.mkdir(email_folder)
    # welcome the user
    print("Dit script koppelt klasgenoten met elkaar in een willekeurige volgorde "
          "op basis van een CSV bestand met de klassen, namen en emailadressen.")
    print("\nZorg er voor dat het CSV bestand 3 kolommen heeft met de volgende namen in deze exacte volgorde: "
          "\'class\', \'name\' en \'email\'.")
    # run some checks on the csv file
    if csv_file_path[-4:] != ".csv":
        csv_file_path += ".csv"
    if not os.path.exists(csv_file_path):
        print("\nHet bestand bestaat niet. Probeer het opnieuw.")
        input()
        exit()

    input("\nHet bestand is gevonden! Klik op enter om door te gaan.")

    def process_csv_data():
        # read the csv file into a pandas dataframe
        df = pd.read_csv(csv_file_path)

        # sort the dataframe by the class column
        df.sort_values(by=["class"], inplace=True)

        # make an empty list to store the class names
        class_names = []
        # loop through the dataframe and add the class names to the list
        for index, row in df.iterrows():
            class_names.append(row["class"])
        # remove duplicates from the list
        class_names = list(set(class_names))
        # sort the list alphabetically
        class_names.sort()

        # set the index to the class
        df.set_index("class", inplace=True)

        # make a list to store the dataframes for all the classes
        class_data_frames = []
        # loop through the dataframe and add the dataframes to the list
        for classes in class_names:
            class_data_frames.append(df.loc[classes])

        # store the dataframes in a dictionary with the class names as keys
        class_dict = dict(zip(class_names, class_data_frames))

        shuffled_rows: dict[Series | None | ndarray | Any, Any] = {}
        # loop through the dictionary and shuffle the rows
        for key, value in class_dict.items():
            # shuffle the rows
            shuffled_rows[key] = value.sample(frac=1, random_state=bit_generator)

        # print the shuffled rows for each class
        for key, value in shuffled_rows.items():
            print("\n" + key + ":")
            print(value)

        # make a separate dictionary to store the names in the shuffled rows
        shuffled_names = {}
        # loop through the dictionary and add the names to the dictionary
        for key, value in shuffled_rows.items():
            # make a list to store the names
            names = []
            # loop through the rows and add the names to the list
            for index, row in value.iterrows():
                names.append(row["name"])
            # add the list to the dictionary
            shuffled_names[key] = names

        # make a separate dictionary to store the emails in the shuffled rows
        shuffled_emails = {}
        # loop through the dictionary and add the emails to the dictionary
        for key, value in shuffled_rows.items():
            # make a list to store the emails
            emails = []
            # loop through the rows and add the emails to the list
            for index, row in value.iterrows():
                emails.append(row["email"])
            # add the list to the dictionary
            shuffled_emails[key] = emails

        # take the first name + " -> " + the next name in the dictionary and add it to a dictionary named assigned_names
        # the last name should be assigned to the first name of that class
        assigned_names = {}
        # loop through the dictionary and add the names to the dictionary
        for key, value in shuffled_names.items():
            # make a list to store the names
            names = []
            # loop through the names and add the names to the list
            for index, name in enumerate(value):
                # check if the index is the last index
                if index == len(value) - 1:
                    # add the name to the list
                    names.append(name + " -> " + value[0])
                else:
                    # add the name to the list
                    names.append(name + " -> " + value[index + 1])
            # add the list to the dictionary
            assigned_names[key] = names

        # take the first email + " -> " + the next email in the dictionary and add it to a dictionary named
        # assigned_emails the last email should be assigned to the first email of that class
        assigned_emails = {}
        # loop through the dictionary and add the emails to the dictionary
        for key, value in shuffled_emails.items():
            # make a list to store the emails
            emails = []
            # loop through the emails and add the emails to the list
            for index, email in enumerate(value):
                # check if the index is the last index
                if index == len(value) - 1:
                    # add the email to the list
                    emails.append(email + " -> " + value[0])
                else:
                    # add the email to the list
                    emails.append(email + " -> " + value[index + 1])
            # add the list to the dictionary
            assigned_emails[key] = emails

        # save the assigned names for each class to a txt file named after the class and "toegewezen_namen.txt"
        # in the output folder

        for key, value in assigned_names.items():
            # create the filepath
            filepath = name_folder + "\\" + key + " toegewezen_namen.txt"
            # open the file
            with open(filepath, "w") as file:
                # loop through the names and write them to the file
                for name in value:
                    file.write(name + "\n")
                # close the file
                file.close()

        # save the assigned emails for each class to a txt file named after the class and "toegewezen_emailadressen.txt"
        # in the output folder

        for key, value in assigned_emails.items():
            # create the filepath
            filepath = email_folder + "\\" + key + " toegewezen_emailadressen.txt"
            # open the file
            with open(filepath, "w") as file:
                # loop through the emails and write them to the file
                for email in value:
                    file.write(email + "\n")
                # close the file
                file.close()

    process_csv_data()

    # tell the user that the program is done and the files are saved
    print("\nHet programma is klaar. De namen zijn opgeslagen in "
          + name_folder
          + " en de emailadressen in "
          + email_folder
          )
    # wait for the user to press enter to exit the program
    input("\nDruk op enter om het programma te sluiten.")
    exit()


# run the program
if __name__ == "__main__":
    main()
