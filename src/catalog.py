day_number = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
}

reminder_menu = {
    "sunday": {
        "service": [  ## service reminder
            {"Sunday": "saved_json/sunday.json"}
        ],
        "worship": [  ## worship reminder
            {"Living Hope": "saved_json/living_hope.json"},
            {"Awake": "saved_json/awake.json"}
        ],
    },
    "wednesday": {
        "prayer": [  ## prayer reminder
            {"Wednesday": "saved_json/wednesday.json"}
        ]
    },
}