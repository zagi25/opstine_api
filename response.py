from data.sql import sql_execute

class Response:
    def __init__(self, sql_string, get):
        self.sql_string = sql_string
        self.get = get

    def _format_podaci(self, data):
        formated_data = list()
        keys = ['naziv_opstine', 'naziv_okruga']
        names = list()
        for d in data:
            names.append(d[keys[0]])

        names = list(set(names))
        names.sort()
        for name in names:
            single = dict()
            godina = dict()
            to_remove = ['opstina_id', 'naziv_opstine', 'naziv_okruga', 'naziv_opstine_clean', 'naziv_okruga_clean', 'godina']
            for d in data:
                if d['naziv_opstine'] == name:
                    single['naziv_opstine'] = d['naziv_opstine']
                    single['naziv_okruga'] = d['naziv_okruga']
                    godina[d['godina']] = {}
                    keys1 = [key for key in d.keys()]
                    for r in to_remove:
                        try:
                            keys1.remove(r)
                        except:
                            pass
                    for key in keys1:
                        godina[d['godina']][key] = d[key]

            single['godina'] = godina
            formated_data.append(single)

        return formated_data

    def _format_distinct_values(self, data, value):
        formated_data = list()
        for d in data:
            formated_data.append(d[value])

        formated_data.sort()
        return formated_data

    def _format_labels(self, data):
        formated_data = list()
        for d in data:
            if d['name'] not in formated_data:
                formated_data.append(d['name'])
        # formated_data = list(set(formated_data))
        # formated_data.sort()

        return formated_data[3:]

    def getResponse(self):
        res = dict()
        formated = list()
        data = sql_execute(self.sql_string, 'get')
        if self.get == 'podaci':
            formated = self._format_podaci(data)
        elif self.get == 'godine':
            formated = self._format_distinct_values(data, 'godina')
        elif self.get == 'opstine':
            formated = self._format_distinct_values(data , 'naziv_opstine')
        elif self.get == 'okruzi':
            formated = self._format_distinct_values(data, 'naziv_okruga')
        elif self.get == 'tipovi_podataka':
            formated = self._format_labels(data)

        if data:
            res['status'] = 'Success'
            res['result'] = formated
        else:
            res['status'] = 'Failure'
            res['result'] = 'No data found'

        return res
