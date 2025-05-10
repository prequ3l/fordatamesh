import requests


def for_weight(num: int) -> str:
    dct: {int: str} = {2: '₂',
                       3: '₃'}
    return dct[num]


def for_get_mesh_id(token: str) -> str:
    try:
        response = requests.get("https://dnevnik.mos.ru/core/api/student_profiles/",
                                headers={"Auth-Token": token})
        return response.json()[0]['id']
    except Exception as e:
        return e.__class__.__name__


class Marks:
    def __init__(self, token: str) -> None:
        self.token: str = token
        self.mesh_id: str = for_get_mesh_id(self.token)
        self.subjects: {str: int} = {'<b>Алгебра</b>': 0,
                                     '<b>Биология</b>': 1,
                                     '<b>Теория вероятностей</b>': 2,
                                     '<b>География</b>': 3,
                                     '<b>Геометрия</b>': 4,
                                     '<b>Английский</b>': 5,
                                     '<b>Информатика</b>': 6,
                                     '<b>История</b>': 7,
                                     '<b>Литература</b>': 8,
                                     '<b>Обществознание</b>': 10,
                                     '<b>ОБЗР</b>': 11,
                                     '<b>ОДНКНР</b>': 12,
                                     '<b>Родная литература</b>': 13,
                                     '<b>Родной русский</b>': 14,
                                     '<b>Русский</b>': 15,
                                     '<b>Технология</b>': 16,
                                     '<b>физика</b>': 17,
                                     '<b>Физическая культура</b>': 18,
                                     '<b>Химия</b>': 19}

    def for_get_marks_quarter(self, period: int) -> str:
        res: str = ''

        headers: {str: str} = {
            'Authorization': self.token,
            'X-mes-subsystem': 'familyweb'
        }

        response = requests.get(f'https://school.mos.ru/api/family/web/v1/subject_marks?student_id={self.mesh_id}',
                                headers=headers)
        needed_subjects = [[j for j in response.json()['payload'][i]['periods'] if 'четверть' in j['title']] for i in
                           range(20)]

        for subject, subject_id in self.subjects.items():
            try:
                res += f'{subject}: {", ".join([i['value'] if i['weight'] == 1 else f"<i>{i['value']}{for_weight(i['weight'])}</i>" for i in
                                                needed_subjects[subject_id][period - 1]['marks']])}\n'
            except IndexError:
                pass

        return res

    def for_get_marks_half_year(self, period: int) -> str:
        res: str = ''

        headers: {str: str} = {
            'Authorization': self.token,
            'X-mes-subsystem': 'familyweb'
        }

        response = requests.get(f'https://school.mos.ru/api/family/web/v1/subject_marks?student_id={self.mesh_id}',
                                headers=headers)
        needed_subjects = [[j for j in response.json()['payload'][i]['periods'] if 'пг' in j['title']] for i in
                           range(20)]

        for subject, subject_id in self.subjects.items():
            try:
                res += f'{subject}: {", ".join([i['value'] if i['weight'] == 1 else f"<i>{i['value']}{for_weight(i['weight'])}</i>" for i in
                                                needed_subjects[subject_id][period - 1]['marks']])}\n'
            except IndexError:
                pass

        return res

    def for_get_quarter_and_year(self) -> str:
        res: str = ''

        headers: {str: str} = {
            'Authorization': self.token,
            'X-mes-subsystem': 'familyweb'
        }

        response = requests.get(f'https://school.mos.ru/api/family/web/v1/subject_marks?student_id={self.mesh_id}',
                                headers=headers)

        for subject, subject_id in self.subjects.items():
            try:
                marks: [str] = list()
                for i in range(4):
                    final_q_num: str = response.json()['payload'][subject_id]['periods'][i]['fixed_value']
                    av_q_num: str = response.json()['payload'][subject_id]['periods'][i]['value']

                    if final_q_num:
                        marks.append(final_q_num)
                    elif av_q_num:
                        marks.append(av_q_num)
                    else:
                        marks.append('?')

                final_y_num: str = response.json()['payload'][subject_id]['year_mark']
                av_y_num: str = response.json()['payload'][subject_id]['average_by_all']

                if final_y_num:
                    res += f'{subject}: {", ".join(marks)} --> {final_y_num}\n'
                elif av_y_num:
                    res += f'{subject}: {", ".join(marks)} --> {av_y_num}\n'
                else:
                    res += f'{subject}: {", ".join(marks)} --> ?\n'
            except IndexError:
                marks: [str] = list()
                for i in range(2):
                    final_q_num: str = response.json()['payload'][subject_id]['periods'][i]['fixed_value']
                    av_q_num: str = response.json()['payload'][subject_id]['periods'][i]['value']

                    if final_q_num:
                        marks.append(final_q_num)
                    elif av_q_num:
                        marks.append(av_q_num)
                    else:
                        marks.append('?')

                final_y_num: str = response.json()['payload'][subject_id]['year_mark']
                av_y_num: str = response.json()['payload'][subject_id]['average_by_all']

                if final_y_num:
                    res += f'{subject}: {", ".join(marks)} --> {final_y_num}\n'
                elif av_y_num:
                    res += f'{subject}: {", ".join(marks)} --> {av_y_num}\n'
                else:
                    res += f'{subject}: {", ".join(marks)} --> ?\n'

        return res
