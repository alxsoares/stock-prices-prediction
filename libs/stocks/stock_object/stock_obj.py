from libs.stocks.graphs.graphs import Graphs_Obj
from libs.stocks.queues.queue.queue import Queue
from libs.stocks.queues.queue_obj.queue_obj import QueueObejct
import apps.ai.config as config


class StockObj():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, stock_name, mock=None,):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self.sec_counter = 0

        # graphs - scraped
        self.graphs_obj = Graphs_Obj(stock_name=stock_name, mock=mock)
        self.time_scales = {
            # initialize 1s with 1m closing values
            '1s': Queue(init_list=self.graphs_obj.graphs['1m']['close'], maxlen=config.max_window_size['1s']),
            '1m': QueueObejct(init_dict=self.graphs_obj.graphs['1m'], time_scale='1m'),
            '2m': QueueObejct(init_dict=self.graphs_obj.graphs['2m'], time_scale='2m'),
            '5m': QueueObejct(init_dict=self.graphs_obj.graphs['5m'], time_scale='5m'),
            '15m': QueueObejct(init_dict=self.graphs_obj.graphs['15m'], time_scale='15m'),
            '30m': QueueObejct(init_dict=self.graphs_obj.graphs['30m'], time_scale='30m'),
            '1h': QueueObejct(init_dict=self.graphs_obj.graphs['1h'], time_scale='1h'),
            '1d': QueueObejct(init_dict=self.graphs_obj.graphs['1d'], time_scale='1d'),
            '5d': QueueObejct(init_dict=self.graphs_obj.graphs['5d'], time_scale='5d'),
            '1mo': QueueObejct(init_dict=self.graphs_obj.graphs['1mo'], time_scale='1mo'),
            '3mo': QueueObejct(init_dict=self.graphs_obj.graphs['3mo'], time_scale='3mo')
        }

    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''
        self.time_scales['1s'].enqueue(item['value'])
        self.sec_counter = self.sec_counter + 1
        if self.sec_counter % config.time_scale2seconds['1m'] == 0: self.time_scales['1m'].enqueue(
            self.insert(item['volume'],live_by='1s',interval2live_by=config.time_scale2seconds['1m']))
        if self.sec_counter % config.time_scale2seconds['2m'] == 0: self.time_scales['2m'].enqueue(
            self.insert(item['volume'],live_by='1s',interval2live_by=config.time_scale2seconds['2m']))
        if self.sec_counter % config.time_scale2seconds['5m'] == 0: self.time_scales['5m'].enqueue(
            self.insert(item['volume'],live_by='1s',interval2live_by=config.time_scale2seconds['5m']))
        if self.sec_counter % config.time_scale2seconds['15m'] == 0: self.time_scales['15m'].enqueue(
            self.insert(item['volume'],live_by='1s',interval2live_by=config.time_scale2seconds['15m']))
        if self.sec_counter % config.time_scale2seconds['30m'] == 0: self.time_scales['30m'].enqueue(
            self.insert(item['volume'],live_by='15m',interval2live_by=2))
        if self.sec_counter % config.time_scale2seconds['1h'] == 0: self.time_scales['1h'].enqueue(
            self.insert(item['volume'],live_by='30m',interval2live_by=2))
        if self.sec_counter % config.time_scale2seconds['1d'] == 0: self.time_scales['1d'].enqueue(
            self.insert(item['volume'],live_by='1h',interval2live_by=24))
        if self.sec_counter % config.time_scale2seconds['5d'] == 0: self.time_scales['5d'].enqueue(
            self.insert(item['volume'],live_by='1d',interval2live_by=5))
        if self.sec_counter % config.time_scale2seconds['1mo'] == 0: self.time_scales['1mo'].enqueue(
            self.insert(item['volume'],live_by='5d',interval2live_by=4)) # four working weeks
        if self.sec_counter % config.time_scale2seconds['3mo'] == 0: self.time_scales['3mo'].enqueue(
            self.insert(item['volume'],live_by='1mo',interval2live_by=3))

        # initialize sec_counter to zero
        if self.sec_counter >= config.time_scale2seconds['3mo']: self.sec_counter = 0

    def insert(self,volume,live_by,interval2live_by):
        live_by_Queue = self.time_scales[live_by]

        if live_by=='1s':   #Queue instance
            return {'open': list(live_by_Queue._queue)[-interval2live_by],
                    'low': min(list(live_by_Queue._queue)[-interval2live_by:]),
                    'high': max(list(live_by_Queue._queue)[-interval2live_by:]),
                    'close': list(live_by_Queue._queue)[-1],
                    'volume': volume}

        else:               #Queue_obj instance
            return {'open': list(live_by_Queue.open._queue)[-interval2live_by],
                    'low': min(list(live_by_Queue.low._queue)[-interval2live_by:]),
                    'high': max(list(live_by_Queue.high._queue)[-interval2live_by:]),
                    'close': list(live_by_Queue.close._queue)[-1],
                    'volume': volume}