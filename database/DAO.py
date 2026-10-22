
from database.DB_connect import DBConnect
from model.arco import Arco
from model.regista import Regista


class DAO:
    @staticmethod
    def getAllMovies():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from movie m """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(date1, date2):
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select distinct dm.name_id, n.name
                    from director_mapping dm, movie m, names n 
                    where dm.movie_id = m.id and dm.name_id = n.id
                    and m.date_published BETWEEN %s and %s
                    order by n.name asc """

        cursor.execute(query, (date1, date2))

        for row in cursor:
            result.append(Regista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapR, date1, date2):
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select r1.name_id as r1, r2.name_id as r2, count(distinct r1.genre) as peso
                    from (select distinct dm.name_id, g.genre
                            from director_mapping dm, movie m, genre g 
                            where dm.movie_id = m.id and m.id = g.movie_id 
                            and m.date_published BETWEEN %s and %s) r1, 
                            (select distinct dm.name_id, g.genre
                                from director_mapping dm, movie m, genre g 
                                where dm.movie_id = m.id and m.id = g.movie_id 
                                and m.date_published BETWEEN %s and %s) r2
                    where r1.name_id  < r2.name_id  
                    and r1.genre = r2.genre 
                    group by r1.name_id, r2.name_id
                    order by peso desc"""

        cursor.execute(query, (date1, date2, date1, date2))

        for row in cursor:
            result.append(Arco(idMapR[row["r1"]], idMapR[row["r2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result
