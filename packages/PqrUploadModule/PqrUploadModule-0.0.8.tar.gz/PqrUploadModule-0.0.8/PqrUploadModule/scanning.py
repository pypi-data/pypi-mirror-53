from . import _scan
from . import stasrt_settings

import _scan
from start_settings import return_start_time



class Scan(_scan.HelpScan):
    def __init__(self,account_id):
        self.account_id = account_id

        self.start_time = return_start_time()


        self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
        self.open_td_incidents = self.get_all_non_compl_incidents_from_td()

        self.at_tickets_for_counterparts = self.list_at_ticket_for_counterparts()

        self.td_incidents_for_counterparts = self.list_td_incidents_for_counterparts()








