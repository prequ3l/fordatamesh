import requests


def for_get_mesh_id(token: str) -> str:
    try:
        response = requests.get("https://dnevnik.mos.ru/core/api/student_profiles/",
                                headers={"Auth-Token": token})
        return response.json()[0]['id']
    except Exception as e:
        return e.__class__.__name__


class Homeworks:
    def __init__(self, token: str) -> None:
        self.token: str = token
        self.mesh_id: str = for_get_mesh_id(self.token)

    def get_homework(self, date: str) -> str:
        res: str = ''

        headers: {str: str} = {
            'Authorization': self.token,
            'X-mes-subsystem': 'familyweb'
        }

        try:
            response = requests.get(
                f"https://school.mos.ru/api/family/web/v1/homeworks?from={date}&to={date}&student_id={self.mesh_id}",
                headers=headers)

            for i in response.json()['payload']:
                res += f'<b>{i['subject_name']}:</b>\n<i>{i['homework']}</i>\n\n'

            return res
        except Exception as e:
            return e.__class__.__name__
