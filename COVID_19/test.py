import requests
data = json_str =  {"region": {"name": "Africa", "avgAge": 19.7, "avgDailyIncomeInUSD": 4, "avgDailyIncomePopulation": 0.73},\
            "periodType": "days", "timeToElapse": 38, "reportedCases": 2747, "population": 92931687, "totalHospitalBeds"\
            : 678874 }
response = requests.post('http://127.0.0.1:8000/api/v1/on-covid-19/', params=data)