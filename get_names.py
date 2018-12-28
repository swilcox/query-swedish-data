import copy
import sys
import pandas as pd
import requests
from io import StringIO

FIRST_NAME_URL = "http://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0001/BE0001G/BE0001FNamn10"
LAST_NAME_URL = "http://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0001/BE0001G/BE0001ENamn10"

YEAR = 1999
MAX_NAMES = 200

FNAME_QUERY = {
  "query": [
    {
      "code": "Fornamn",
      "selection": {
        "filter": "all",
        "values": [
          "*"
        ]
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "{}".format(YEAR)
        ]
      }
    }
  ],
  "response": {
    "format": "csv"
  }    
}

FEMALE_FNAME_QUERY = copy.deepcopy(FNAME_QUERY)
FEMALE_FNAME_QUERY["query"][0]["selection"]["values"][0] = "*K"

MALE_FNAME_QUERY = FNAME_QUERY.copy()
MALE_FNAME_QUERY["query"][0]["selection"]["values"][0] = "*M"

LNAME_QUERY = {
    "query": [
    {
      "code": "Efternamn",
      "selection": {
        "filter": "all",
        "values": [
          "*"
        ]
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "{}".format(YEAR)
        ]
      }
    }
  ],
  "response": {
    "format": "csv"
  }
}

# NOTE: splitting the last name into 2 queries is apparently necessary becauset the API
# errors out on the "correct" full query due to the high number of records. Splitting it
# into 2 queries seems to work.

LNAME_QUERY_1 = copy.deepcopy(LNAME_QUERY)
LNAME_QUERY_1["query"][0]["selection"]["values"] = [
    "A*", "B*", "C*", "D*", "E*", "F*", "G*", "H*", "I*", "J*", "K*", "L*", "M*", "N*", "O*"
]

LNAME_QUERY_2 = copy.deepcopy(LNAME_QUERY)
LNAME_QUERY_2["query"][0]["selection"]["values"] = [
    "P*", "Q*", "R*", "S*", "T*", "U*", "V*", "W*", "X*", "Y*", "Z*", "Å*", "Ä*", "Ö*"
]

FEMALE_FNAME = {'queries': [FEMALE_FNAME_QUERY], 'url': FIRST_NAME_URL, 'count_field': 'First namnes {}'.format(YEAR), 'name_field': 'first names', 'label': 'Female'}
MALE_FNAME = {'queries': [MALE_FNAME_QUERY], 'url': FIRST_NAME_URL, 'count_field': 'First namnes {}'.format(YEAR), 'name_field': 'first names', 'label': 'Male'}
LNAME = {'queries': [LNAME_QUERY_1, LNAME_QUERY_2], 'url': LAST_NAME_URL, 'count_field': 'Last names {}'.format(YEAR), 'name_field': 'last names'}

NAME_MAP = {'female': FEMALE_FNAME, 'male': MALE_FNAME, 'last': LNAME}

NAME_TYPES = [FEMALE_FNAME, MALE_FNAME, LNAME]

CODE = "('{}', {}),"

OUTPUT_TYPE = [CODE]


def _get_name_data(name_type):
    """
    request data from the API and return a pandas dataframe object with the right data
    """
    print('BEGIN: get name data')
    output_texts = []
    for q in name_type['queries']:
        print('executing API query...')
        r = requests.post(name_type['url'], json=q)
        output_texts.append(r.text)
    print('analyzing data')
    df = pd.read_csv(StringIO(''.join(output_texts)))
    df[['count']] = df[[name_type['count_field']]].apply(pd.to_numeric, errors='coerce')
    df.rename(columns={name_type['name_field']: 'name_value'}, inplace=True)
    df.sort_values(['count'], ascending=[False], inplace=True)
    total = df['count'].sum()
    df = df[0:MAX_NAMES]
    df['percent'] = df['count'] / total
    df.sort_values(['name_value'], inplace=True)
    return df


def _output_data(df, output_type, filename):
    """
    output the dataframe data in the specified format to a file
    """
    print('outputing data')
    with open(filename, 'wt') as output_file:
        for row in df.itertuples():
            output_file.write("('{}', {:.6f}),\n".format(row.name_value.strip(), row.percent))

    print(df)


def main(name_type, filename):
    """
    main function.
    Get the data from Sweden and filter it.
    Output the data.
    """
    df = _get_name_data(name_type)
    _output_data(df, CODE, filename)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        if NAME_MAP.get(sys.argv[1], None):
            main(NAME_MAP.get(sys.argv[1]), sys.argv[2])
        else:
            print("choose name type of: {}".format(NAME_MAP.keys()))
    else:
        print("{} NAME_TYPE <filename>".format(sys.argv[0]))
