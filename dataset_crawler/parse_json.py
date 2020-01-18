import json

with open("climate_report.json") as f:
    data = json.loads(f.read())

rows = []
for url, days in data.items():
    month, year = url.split("climate/")[1].split("-")[0], url.split("climate/")[1].split("-")[1].split("/")[0]

    for Day in days.items():
        day = Day[1]['Day'] if 'Day' in Day[1].keys() else None

        if day:
            Day[1]['Year'] = str(year)
            Day[1]['Month'] = str(month)
            Day = Day[1]
            Day['FG'] = '1' if Day['FG'] == 'o' else Day['FG']
            col = list(Day.values())
            if len(rows) == 0:
                rows.append(list(Day.keys()))

            rows.append(col)

with open("climate_report_dataset.csv", "w") as f:
    for i, data in enumerate(rows):
        data = data[1:]+[data[0]]
        lines = ""
        for line in data:
            lines+= line.strip()+","
        lines = lines[:-1]+"\n"

        f.write(lines)