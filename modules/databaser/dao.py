# from prettytable import PrettyTable
from sqlalchemy import select, update

# from modules.databaser import vendors_base
from modules.databaser.db import comments, engine, hardware
from modules.pinger.pinger import pinger
from modules.pinger.pinger_all_network_with_threading import net_scanner


# pattern class
class DAO:
    def create_hardware_unit_with_comment(self, hard_type, hard_name, hard_ip, hard_place, comment):
        conn = engine.connect()
        with conn.begin():
            insert_query = hardware.insert().values(
                hard_type=hard_type,
                hard_name=hard_name,
                hard_ip=hard_ip,
                hard_place=hard_place,
            )
            result = conn.execute(insert_query)
            new_hardware_id = result.inserted_primary_key[0]

            insert_query = comments.insert().values(hardware_id=new_hardware_id, comment=comment)
            conn.execute(insert_query)
        return new_hardware_id

    def read_hardware_with_comment(self, input_id):
        conn = engine.connect()
        query = (
            select(
                [
                    hardware.c.id,
                    hardware.c.hard_type,
                    hardware.c.hard_name,
                    hardware.c.hard_ip,
                    hardware.c.hard_place,
                    comments.c.comment,
                ]
            )
            .select_from(hardware.join(comments, comments.c.hardware_id == hardware.c.id))
            .where(hardware.c.id == input_id)
        )

        result = conn.execute(query).first()
        return dict(result)

    def pinger_for_page(self, id):
        conn = engine.connect()
        query = select([hardware.c.hard_ip]).where(hardware.c.id == id)
        result = conn.execute(query).first().values()
        #        print(result[0])
        result_of_ping = pinger(result[0])
        return result_of_ping

    def update_the_comment(self, id_for_upd, newcomment):
        conn = engine.connect()
        query = (
            update(comments).where(comments.c.hardware_id == id_for_upd).values(comment=newcomment)
        )
        conn.execute(query)
        return newcomment

    def read_hardware_with_param(self, type_hardware, locate):
        conn = engine.connect()
        query = select([hardware, comments.c.comment]).where(
            hardware.c.id == comments.c.hardware_id
        )

        where_stmt = []

        if type_hardware != "0":
            where_stmt.append(hardware.c.hard_type == type_hardware)
        if locate != "0":
            where_stmt.append(hardware.c.hard_place == locate)
        if where_stmt:
            query = query.where(*where_stmt)

        list_with_param = []
        exec = conn.execute(query)

        for row in exec:
            list_with_param.append(row)

        #        print(list_with_param)

        results_table = PrettyTable()
        results_table.field_names = ["Row in db", "Type", "Name", "IP", "Locate", "Comment"]
        for row in list_with_param:
            results_table.add_row(row)

        result_for_html = results_table.get_html_string(format=True)

        return result_for_html

    # def scan_network(self):
    #     scan_table = PrettyTable()
    #     scan_table.field_names = ["IP", "Net name", "MAC", "Vendor"]
    #     scanned_dict = sorted(net_scanner().items())
    #     #        print(net_scanner())
    #     #        print(scanned_dict)
    #     for row in scanned_dict:
    #         len_in_table = []
    #         len_in_table.append(row[0])
    #         len_in_table.append(row[1][0])
    #         len_in_table.append(row[1][1])
    #         len_in_table.append(vendors_base.vendors_names(str(row[1][1])))
    #         #            print(len_in_table)
    #         scan_table.add_row(len_in_table)
    #
    #     result_for_html = scan_table.get_html_string(format=True)
    #
    #     return result_for_html
