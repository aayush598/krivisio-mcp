{
  "model_name": "cocomo2",
  "data": {
    "function_points": {
      "fp_items": [
        {"fp_type": "EI", "det": 8, "ftr_or_ret": 1},
        {"fp_type": "EO", "det": 10, "ftr_or_ret": 2},
        {"fp_type": "ILF", "det": 18, "ftr_or_ret": 3}
      ],
      "language": "Java"
    },
    "reuse": {
      "asloc": 3500,
      "dm": 20,
      "cm": 10,
      "im": 10,
      "su_rating": "L",
      "aa_rating": "2",
      "unfm_rating": "CF",
      "at": 15
    },
    "revl": {
      "new_sloc": 8500,
      "adapted_esloc": 2500,
      "revl_percent": 25
    },
    "effort_schedule": {
      "sloc_ksloc": 7.5,
      "sced_rating": "L"
    }
  }
}


{
  "model": "cocomo2",
  "result": {
    "function_point_sizing": {
      "ufp": 15,
      "sloc": 795
    },
    "reuse": {
      "esloc": 4025
    },
    "revl_adjustment": {
      "sloc_total": 11000,
      "sloc_after_revl": 13750
    },
    "estimation": {
      "person_months": 26.96,
      "development_time_months": 8.53,
      "avg_team_size": 3.16
    }
  }
}