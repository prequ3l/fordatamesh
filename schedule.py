import requests


def for_get_mesh_id(token: str) -> str:
    try:
        response = requests.get("https://dnevnik.mos.ru/core/api/student_profiles/",
                                headers={"Auth-Token": token})
        return response.json()[0]['id']
    except Exception as e:
        return e.__class__.__name__


class Schedule:
    def __init__(self, token: str) -> None:
        self.token: str = token
        self.mesh_id: str = for_get_mesh_id(self.token)

    def get_schedule(self, date: str) -> str:
        res: str = ''

        headers: {str: str} = {
            'Authorization': self.token,
            'X-mes-subsystem': 'familyweb'
        }

        try:
            response = requests.get(
                f'https://school.mos.ru/api/family/web/v1/schedule/short?student_id={self.mesh_id}&dates={date}',
                headers=headers)

            for num, subject in enumerate(response.json()['payload'][0]['lessons'], 1):
                if subject['subject_name'] is None:
                    res += f"<b>{num}.</b> <i>{subject['group_name']}</i>\n"
                else:
                    res += f"<b>{num}.</b> <i>{subject['subject_name']}</i>\n"

            return res
        except Exception as e:
            return e.__class__.__name__
