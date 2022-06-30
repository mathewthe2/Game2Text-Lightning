import sqlite3

class Pitch():
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)

    def get_pitch(self, expression, reading=''):
        cursor = self.db.cursor()
        if reading:
            cursor.execute("SELECT pitch FROM Dict WHERE expression=?", (expression,))
        else:
            cursor.execute("SELECT pitch FROM Dict WHERE expression=? AND reading=?", (expression, reading))
        result = cursor.fetchone()
        return None if result is None else result[0]

if __name__ == '__main__':
    from fbs_runtime.application_context.PyQt5 import ApplicationContext
    appctxt = ApplicationContext()
    pitch = Pitch(appctxt.get_resource('rikaisama/pitch_accents.sqlite'))
    print(pitch.get_pitch('おっとり刀', 'おっとりがたな'))
