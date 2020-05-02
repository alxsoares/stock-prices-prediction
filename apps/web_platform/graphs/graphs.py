import time
import requests
import graphs.config


class Graphs:
    def __init__(self,stock_name,mock=None):
        self.stock_name=stock_name
        self.graphs={}
        for time_scale in graphs.config.time_scales:
            self.graphs[time_scale]=self.get_quotes(stock_name,time_scale,mock)


    def get_quotes(self,stock_name,time_scale,mock=None):
        TWO_MONTH= graphs.config.TWO_MONTH
        A_WEEK= graphs.config.A_WEEK

        try: # try from begining of time
            json_response=self.get_json_response(0,time_scale)
        except TypeError: # try 2 month ago
            try :
                json_response = self.get_json_response(int(time.time())-TWO_MONTH, time_scale)
            except TypeError: #try a week ago
                try:
                    json_response = self.get_json_response(int(time.time())-A_WEEK, time_scale)
                except TypeError:
                    raise ("This time scale asked for start_time that is shorter than a week")

        return json_response["quote"][0]

    def get_json_response(self,start_time,time_scale,mock=None):
        if mock==None:
            url = graphs.config.url % (self.stock_name, self.stock_name, start_time, int(time.time()), time_scale)
            json_response = requests.get(url).json()['chart']['result'][0]['indicators']
        else:
            return mock

        return json_response







if __name__=="__main__":
    g=Graphs('FB')
    a=1