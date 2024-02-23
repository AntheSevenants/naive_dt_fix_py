import pandas as pd

# Ported from my R code


def fix_participle_dt(df: pd.DataFrame, column: str, ignore_list: list[str] = ["geplant", "gepland", "ingeplant", "ingepland", "gebaad", "gebaat", "geniest", "geniesd"], correct_list: list[str] = ["geracet", "gefaket", "opgenoemd", "getwitterd", "gecrasht", "geliket", "gepiercet", "nagepluisd"]):
    """Correct participle endings based on relative frequencies

    Args:
        df (pandas.DataFrame): the dataframe to apply the corrections to
        column (str): the name of the column to correct
        ignore_list (list[str], optional): a list of participles to never correct. Defaults to ["geplant", "gepland", "ingeplant", "ingepland", "gebaad", "gebaat", "geniest", "geniesd"].
        correct_list (list[str], optional): a list of definitely correct participles, which overrules the relative frequencies. Defaults to ["geracet", "gefaket", "opgenoemd", "getwitterd", "gecrasht", "geliket", "gepiercet", "nagepluisd"].
    """

    # First, we check what participles are in the dataset
    all_participles = df[column].unique()

    # Then, create a frequency table so we can compare forms against each other
    participle_counts = df[column].value_counts()

    # List of all replacements to make
    replacements = {}

    # We go over each participle in the dataset one by one
    for participle in all_participles:
        # Some forms are ambiguous, so they have to be ignored
        # Other forms most language users just don't spell right...
        if participle in ignore_list or participle in correct_list:
            continue

        # Get the last character of this participle
        last_char = participle[-1]

        # Get a version of this participle without the last character
        participle_bare = participle[:-1]

        # If the last character of the participle is 'd', consider a form
        # where the last character is 't'
        if last_char == "d":
            alternative_form = participle_bare + "t"
        # The inverse for 't' (alternative form with 'd')
        elif last_char == "t":
            alternative_form = participle_bare + "d"
        # Not eligible, skip
        else:
            continue

        # Get the frequencies of both the original and the alternative
        participle_frequency = participle_counts.get(participle, 0)
        participle_alternative_frequency = participle_counts.get(
            alternative_form, 0)

        # If the alternative is not found in the dataset,
        # definitely don't consider it
        if participle_alternative_frequency == 0 and alternative_form not in correct_list:
            continue

        # If the alternative form is more popular, assume it is correct
        # We add it to the list of replacements
        if participle_alternative_frequency > participle_frequency or alternative_form in correct_list:
            replacements[participle] = alternative_form
            print(f"[naive-dt-fix] Will replace '{participle}' with '{alternative_form}'")

    print("[naive-dt-fix] Replacing participles")

    # Finally, do the replacement
    df[column] = df[column].replace(replacements)

    print("[naive-dt-fix] Replacements made")

    return df
