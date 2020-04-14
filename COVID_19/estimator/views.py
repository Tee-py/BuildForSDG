from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Log

def estimator(data):
    #calculations for the currentlyInfected property
    impact_ci = data['reportedCases']*10
    severe_ci = data['reportedCases']*50

    #calculations for the inFectedByRequestTime
    if data['periodType'] == 'days':
        impact_ibrt = int(impact_ci*(2**int((data['timeToElapse']/3))))
        severe_ibrt = int(severe_ci*(2**int((data['timeToElapse']/3))))

    elif data['periodType'] == 'weeks':
        factor = int((data['timeToElapse']*7)/3)
        impact_ibrt = int(impact_ci*(2**factor))
        severe_ibrt = int(severe_ci*(2**factor))

    elif data['periodType'] == 'months':
        factor = int((data['timeToElapse']*30)/3)
        impact_ibrt = int(impact_ci*(2**factor))
        severe_ibrt = int(severe_ci*(2**factor))

    impact_scbrt = int(0.15*impact_ibrt)
    severe_scbrt = int(0.15*severe_ibrt)
    impact_hbbrt = int(0.35*data['totalHospitalBeds']-impact_scbrt)
    severe_hbbrt = int(0.35*data['totalHospitalBeds']-severe_scbrt)
    impact_icu = int(0.05*impact_ibrt)
    severe_icu = int(0.05*severe_ibrt)
    impact_venti = int(0.02*impact_ibrt)
    severe_venti = int(0.02*severe_ibrt)

    if data['periodType'] == 'days':
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']\
        ['avgDailyIncomePopulation'])/data['timeToElapse'])
        severe_dnflight = ((severe_ibrt*data['region']['avgDailyIncomeInUSD']*data['region'][\
        'avgDailyIncomePopulation'])/data['timeToElapse'])

    elif data['periodType'] == 'weeks':
        denum_var = data['timeToElapse']*7
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']\
        ['avgDailyIncomePopulation'])/denum_var)
        severe_dnflight = ((severe_ibrt* data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)

    elif data['periodType'] == 'months':
        denum_var = data['timeToElapse']*30
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)
        severe_dnflight = ((severe_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)

    #The returned data
    python_return_data = {
        "data": {
            "region": {
                "name": data['region']['name'],
                "avgAge": data['region']['avgAge'],
                "avgDailyIncomeInUSD": data['region']['avgDailyIncomeInUSD'],
                "avgDailyIncomePopulation": data['region']['avgDailyIncomePopulation']
            },
            "periodType": data['periodType'],
            "timeToElapse": data['timeToElapse'],
            "reportedCases": data['reportedCases'],
            "population": data['population'],
            "totalHospitalBeds": data['totalHospitalBeds']
        },
        "impact": {
          "currentlyInfected": impact_ci,
          "infectionsByRequestedTime": impact_ibrt,
          "severeCasesByRequestedTime": impact_scbrt,
          "hospitalBedsByRequestedTime": impact_hbbrt,
          "casesForICUByRequestedTime": impact_icu,
          "casesForVentilatorsByRequestedTime": impact_venti,
          "dollarsInFlight": int(impact_dnflight),

        },
        "severeImpact": {
          "currentlyInfected": severe_ci,
          "infectionsByRequestedTime": severe_ibrt,
          "severeCasesByRequestedTime": severe_scbrt,
          "hospitalBedsByRequestedTime": severe_hbbrt,
          "casesForICUByRequestedTime": severe_icu,
          "casesForVentilatorsByRequestedTime": severe_venti,
          "dollarsInFlight": int(severe_dnflight),
        }
    }
    #return the json format of the input data and python return data
    return python_return_data


# Create your views here.

def home(request):
    import json
    response = json.dumps({})
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def endpoint(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        response = json.dumps(estimator(data))
    else:
        response = json.dumps({})
    import random
    new_log = Log(request_method=request.method, status_code=200, path='/api/v1/on-covid-19', response_time= \
        random.randint(10, 30), time_unit='ms')
    new_log.save()
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def xml(request):
    if request.method == 'POST':
        import dicttoxml
        import json
        data = json.loads(request.body)
        response = dicttoxml.dicttoxml(estimator(data))
    else:
        import dicttoxml
        response = dicttoxml.dicttoxml({})
    import random
    new_log = Log(request_method=request.method, status_code=200, path='/api/v1/on-covid-19/xml', response_time= \
        random.randint(10, 15), time_unit='ms')
    new_log.save()
    return HttpResponse(response, content_type='application/xml')

@csrf_exempt
def json(request):
    import random
    import json
    if request.method == 'POST':
        covid = json.loads(request.body)
        response = json.dumps(estimator(covid))
    else:
        response = json.dumps({})
    new_log = Log(request_method=request.method, status_code=200, path='/api/v1/on-covid-19/json', response_time= \
        random.randint(10, 15), time_unit='ms')
    new_log.save()
    return HttpResponse(response, content_type='text/json')


def logs(request):
    all_logs = Log.objects.all()
    out = """"""
    for log in all_logs:
        out += f'{log.request_method}\t{log.path:}\t{log.status_code:>15}\t{log.response_time:>15}{log.time_unit}\n'
    return HttpResponse(out, content_type='text/plain')
