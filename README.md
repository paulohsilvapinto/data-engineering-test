# Venues Validator

### Main Goal

The goal of this project is to check which venues are suitable for a list of users and which are not, based on the preferences of each user. If the venue is not suitable for a user, then it is not suitable for the entire user list.

## Using this project

#### Requirements

The only requirement for this project is Python 3.6. Install Python and add it to the PATH, then run:

```bash
cd PATH\TO\THE\PROJECT\
python setup.py install
```

#### Quick Start

First step is to import the module:

```python
from venues import venues as v
```

The main function is called **get_compatible_venues** and it expects three parameters:

* **user_list:** A list containing the name of the users that will be attending the event.
* **users_url:** The URL of the json file containing the users preferences.
* **venues_url:** The URL of the json file containing the venues details.

If no users_url is provided, then the function will use [this file](https://gist.githubusercontent.com/benjambles/ea36b76bc5d8ff09a51def54f6ebd0cb/raw/ee1d0c16eaf373cccadd3d5604a1e0ea307b2ca0/users.json) as users data. The same will happen if no venues_url is provided, in which case the function will use [this file](https://gist.githubusercontent.com/benjambles/ea36b76bc5d8ff09a51def54f6ebd0cb/raw/ee1d0c16eaf373cccadd3d5604a1e0ea307b2ca0/venues.json) as venues data. **Your custom files must have the same structure as those sample files.**

Therefore, a sample call would be:

```python
v.get_compatible_venues(user_list=['Karol Drewno', 'Wen Li']
```

And the output will be:

```json
{
    "places_to_visit": [
        "Spice of life",
        "The Cambridge",
        "Spirit House"
    ]
    , "places_to_avoid": [
        {
            "name": "El Cantina",
            "reason": ["There is nothing for Karol Drewno to drink."]
        }, {
            "name": "Twin Dynasty",
            "reason": ["There is nothing for Wen Li to eat."]
        }, {
            "name": "Wagamama",
            "reason": ["There is nothing for Karol Drewno to drink."]
        }, {
            "name": "Sultan Sofrasi",
            "reason": ["There is nothing for Karol Drewno to drink."]
        }, {
            "name": "Tally Joe",
            "reason": ["There is nothing for Karol Drewno to drink."]
        }, {
            "name": "Fabrique",
            "reason": [
                "There is nothing for Karol Drewno to drink.",
                "There is nothing for Wen Li to drink."
            ]
        }
    ]
}
```

**I hope you like it! :heart:**
