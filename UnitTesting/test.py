"""
slot_found = []


def scrap_data(vaccine_data=None) -> list:
    v_arr = vaccine_data.strip().split()
    _temp_arr = [v_arr[t * 4: t * 4 + 4] for t in range(int(len(v_arr) / 4))]
    tmp_vac = []
    for _data in _temp_arr:
        if _data[0] != 'Booked':
            _get = {
                'vaccine_name': _data[1],
                'available_quantity': _data[0],
                'age_range': str(_data[3])
            }
            tmp_vac.append(_get)

    if tmp_vac:
        return tmp_vac
    else:
        return []


test_data_array = [
    ['NA', 'CENTER-1', 'ADDRESS-1', '20-May-2021'],
    ['Booked COVISHIELD Age 45+', 'CENTER-2', 'ADDRESS-2', '19-May-2021'],
    ['Booked COVISHIELD Age 18+ 1 COVISHIELD Age 45+', 'CENTER-3', 'ADDRESS-3', '19-May-2021'],
    ['2 COVISHIELD Age 45+ Booked COVISHIELD Age 18+', 'CENTER-4', 'ADDRESS-4', '19-May-2021'],
    ['3 COVISHIELD Age 45+ 4 COVAXIN Age 18+', 'CENTER-5', 'ADDRESS-5', '19-May-2021'],
    ['5 COVISHIELD Age 45+ 6 COVAXIN Age 18+ 7 SPUTNIK-V Age 18+', 'CENTER-6', 'ADDRESS-6', '19-May-2021'],
    ['Booked COVISHIELD Age 45+ Booked COVAXIN Age 45+', 'CENTER-7', 'ADDRESS-7', '19-May-2021'],
]

for x in test_data_array:
    tjj = scrap_data(vaccine_data=x[0])
    print(tjj)
"""

final_data = [
    {
        "center_name": "Apollo Hospital Modern School Paid",
        "center_address": "Modern School Sector 7 Vashi Navi Mumbai Maharashtra India, Thane, Maharashtra, 400703",
        "slot_details": {
            "19-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "50",
                    "age_range": "45+"
                }
            ],
            "20-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "49",
                    "age_range": "45+"
                }
            ]
        }
    },
    {
        "center_name": "Apollo Hospital Navi Mumbai Paid",
        "center_address": "Plot 13 Maharashtra 400614, Thane, Maharashtra, 400614",
        "slot_details": {
            "19-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "8",
                    "age_range": "18+"
                },
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "50",
                    "age_range": "45+"
                }
            ],
            "20-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "50",
                    "age_range": "45+"
                },
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "6",
                    "age_range": "18+"
                }
            ]
        }
    },
    {
        "center_name": "BHAGYANAGAR UPHC (ABOVE 45)",
        "center_address": "NEAR MUNICIPAL SCHOOL NO 75 TADALI ROAD BHAGAYANAGAR BHIWANDI, Thane, Maharashtra, 421302",
        "slot_details": {
            "19-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "20",
                    "age_range": "45+"
                }
            ]
        }
    },
    {
        "center_name": "KHUDABAKSH HALL(BNMC) (45)",
        "center_address": "Bala Compound  Nashik Road  Bhiwandi, Thane, Maharashtra, 421303",
        "slot_details": {
            "19-May-2021": [
                {
                    "vaccine_name": "COVISHIELD",
                    "available_quantity": "20",
                    "age_range": "45+"
                }
            ]
        }
    }
]

start_ = '<html><table border="1" cellspacing="3" cellpadding="3" style="text-align:left;padding:0;"> ' \
         '<tr> <th>No.</th> <th>Center Name</th> <th>Center Address</th> <th>Slot Date</th> ' \
         '<th>Vaccine</th> <th>Quantity</th> <th>Age Range</th> </tr>'
end_ = '</table>'
tel = "<tr> <td>%d</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>"


def prepare_message_body():
    final_body = []
    header_text = 'Following vaccine centers have been found with availability:\n'
    final_body.append(header_text)
    final_body.append(start_)
    for idx, slot_data in enumerate(iterable=final_data, start=1):
        center_name = slot_data['center_name']
        center_address = slot_data['center_address']
        for _date, _arr_1 in slot_data['slot_details'].items():
            for _vacc in _arr_1:
                k = tel % (idx, center_name, center_address, _date, _vacc['vaccine_name'], _vacc['available_quantity'],
                           _vacc['age_range'])
                final_body.append(k)

    final_body.append(end_)
    print('\n'.join(final_body))


prepare_message_body()
