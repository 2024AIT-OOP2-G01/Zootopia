from flask import Blueprint
from models import Visitor
from datetime import date
import calendar
import random
import json

# Blueprintの作成
visitor_bp = Blueprint('visitor', __name__, url_prefix='/visitors')


def dummy():
    for y in range(2020,2025):
        for m in range(1,13):
            days =  calendar.monthrange(y, m)[1]
            print("{} {} {}".format(y,m,days))
            for d in range(1,days+1):
                Visitor.create(date=date(y,m,d), male=random.randrange(300,1500,1), female=random.randrange(300,1500,1), boy=random.randrange(300,1500,1), girl=random.randrange(300,1500,1))


@visitor_bp.route('/data')
def list():
    #dummy()
    # データ取得
    visitors = Visitor.select()
    print(type(visitors))
    data = []
    for visitor in visitors:
        #print(visitor.date, visitor.male, visitor.female, visitor.boy, visitor.girl)
        y = visitor.date.year
        m = visitor.date.month
        d = visitor.date.day
        data.append({"{}-{}-{}".format(y, m, d):{"male":visitor.male, "female":visitor.female, "boy":visitor.boy, "girl":visitor.girl}})

    monthly_data = {}
    previous_date = date(1, 1, 1)
    current_date = date(1, 1, 1)
    previous_y_m = date(1, 1, 1)
    current_y_m = date(1, 1, 1)
    data_in_month = {"m":0, "f":0, "b":0, "g":0}
    for dat in data:
        _date = None
        for day in dat.keys():
            y = int(day.split('-')[0])
            m = int(day.split('-')[1])
            d = int(day.split('-')[2])
            _date = date(y,m,d)
        if _date != None:
            current_date = _date
        if current_date.year != previous_date.year:
            current_y_m = date(current_date.year, 1, 1)
            print(f"change year to {current_date.year}")
        if current_date.month != previous_date.month or current_date.year != previous_date.year:
            key = f"{current_y_m.year}-{current_y_m.month}"
            adding_data = {
                "m":data_in_month['m'],
                "f":data_in_month['f'],
                "b":data_in_month['b'],
                "g":data_in_month['g']
                }
            #print(f"sum {key} {adding_data}")
            monthly_data[key]=adding_data
            print("====================================")
            print("------------------------------------")
            print(monthly_data)
            print("------------------------------------")
            print("====================================")
            data_in_month = {"m":0, "f":0, "b":0, "g":0}
            current_y_m = date(current_date.year, current_date.month, 1)
            print(f"change month to {current_date.month}")
            print()
            print()
        #print("D",dat)
        if dat is not None:
            for key in dat.keys():
                #print(dat[key]["male"])
                data_in_month['m'] += dat[key]["male"]
                data_in_month['f'] += dat[key]["female"]
                data_in_month['b'] += dat[key]["boy"]
                data_in_month['g'] += dat[key]["girl"]
        previous_date = current_date
    print("==============")
    print(monthly_data)
    print("==============")
    print(json.dumps(monthly_data))


    return json.dumps(monthly_data)