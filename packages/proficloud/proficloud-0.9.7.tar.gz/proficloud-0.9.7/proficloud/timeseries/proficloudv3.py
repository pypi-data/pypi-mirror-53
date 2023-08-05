from kaa_sdk.config import set_credentials_file, set_config_file
from kaa_sdk.epts.v1.api import get_last_time_series
from datetime import datetime, timedelta
from kaa_sdk.epts.v1.api import get_time_series
import time
from pandas import DataFrame, merge, Series

from streamz.core import Stream
import time
import tornado.ioloop
from tornado import gen
from pandas import DataFrame
import pandas as pd
import numpy

from py_linq import Enumerable

class ProficloudV3Metrics():

    DEBUGTIME = False
    """Debug request response times (print)"""
    DEBUGRESPONSE = False
    """
    Debug http-responses. When set to true, the attribute DEBUGRESPONSECONTENT then contains the last raw response. 
    Does not work when calling API in parallel using the same instance!
    """
    DEBUGRESPONSECONTENT = None
    """
    Contains the last response if DEBUGRESPONSE is set to True.
    """

    _host = 'env.kaa-demo.pc-playground.de'
    _auth_host = 'auth.kaa-demo.pc-playground.de'
    _client_id = 'kaa-frontend'
    _client_secret = None #None for no secret
    _realm = 'kaa'
    _application_name = "demo_application"

    #def __init__(self):   

    @staticmethod
    def authenticate(username, password):
        set_credentials_file(uname=username,
                            password=password,
                            client_id=ProficloudV3Metrics._client_id,
                            client_secret=ProficloudV3Metrics._client_secret)

        set_config_file(host=ProficloudV3Metrics._host,
                        auth_host=ProficloudV3Metrics._auth_host,
                        realm=ProficloudV3Metrics._realm)

    def queryMetrics(self, endpoint_id, metrics, start_time=None, end_time=None, createDf=True, fillNaMethod = None, dropTrailingNa=True, orderDesc=False):
        """
        Query metrics and return the data as pandas DataFrame.
        
        :type metrics: list(str), str
        :param metrics: A list of metric names (or a single metric name) to query. 
        :type start_time: int, datetime, str or None
        :param start_time: Timestamp (ms based), or datetime object (or datetime as string) not used when None. (Default: None)
        :type end_time: int, datetime, str or None
        :param end_time: Timestamp (ms based), or datetime object (or datetime as string). This must be later in time than the start time. If not specified, the end time is assumed to be the current date and time. (Default: None)
        :type orderDesc: boolean
        :param orderDesc: Orders returned data points based on timestamp. Descending order when True, or ascending when False (default) Only in effect when returning DataFrame.
        :type createDF: boolean
        :param createDF: Convert response into a convenient Pandas Dataframe. (Default=True)
        :type fillNaMethod: str
        :param fillNaMethod: {‘backfill’, ‘bfill’, ‘pad’, ‘ffill’, None}, default None. Method to use for filling holes in reindexed Series pad / ffill: propagate last valid observation forward to next valid backfill / bfill: use NEXT valid observation to fill gap
        :type dropTrailingNa: boolean
        :param dropTrailingNa: Drop trailing NaN values when set to true. Especially useful when end neither end param is specified (filters time delay when querying multiple metrics). Default: True
        :rtype: pandas.DataFrame or dict
        :return: Returns pandas.DataFrame 
        """
        
        if ProficloudV3Metrics.DEBUGTIME:
            start_t = datetime.now()

        sort = "ASC"
        if orderDesc:
            sort = "DESC"

        response = get_time_series(ProficloudV3Metrics._application_name, metrics, start_time, end_time, endpoint_id, sort=sort)

        if ProficloudV3Metrics.DEBUGTIME:
            end_t = datetime.now()
            print("Database query took "+str(end_t - start_t))

        if ProficloudV3Metrics.DEBUGRESPONSE:
            ProficloudV3Metrics.DEBUGRESPONSECONTENT = response

        if not createDf:
            return response
        else:
            if ProficloudV3Metrics.DEBUGTIME:
                start_t = datetime.now()
            dfres = ProficloudV3Metrics.convert_response(response, endpoint_id, fillNaMethod=fillNaMethod, dropTrailingNa=dropTrailingNa, convertTimestamp=True)#, orderDesc=orderDesc
            if ProficloudV3Metrics.DEBUGTIME:
                end_t = datetime.now()
                print("Dataframe conversion took "+str(end_t - start_t))
            return dfres


    @staticmethod
    def dateparse(datestring):
        dateformat = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
        res = datestring
        try:
            res = datetime.strptime(datestring, dateformat[0])
        except:
            res = datetime.strptime(datestring, dateformat[1])
        return res

    @staticmethod
    def convert_response(response, endpoint_id, fillNaMethod=None, dropTrailingNa=True, convertTimestamp=False):#, orderDesc=False
        """
        Used existing function from package as base. Description follows.
        """
        result = None

        if response is None:
            raise KeyError("Provided response is invalid. (None)")

        data = Enumerable(response)
        filter_endpoint = data.where(lambda w: endpoint_id in w)
        check_endpoint_id = len(list(filter_endpoint))
        
        if check_endpoint_id <= 0:
            return None
                
        unique_metrics = list(filter_endpoint.select(lambda x: list(x[endpoint_id].keys())[0]).distinct())
        metricCount = len(unique_metrics)

        if metricCount <= 0:
            return None

        for m in range(0, metricCount):
                
            #Get Metric Name
            mname = unique_metrics[m]
            
            try:
                #get metric data:
                all_from_one = data.select(lambda s: s[endpoint_id]).where(lambda w: mname in w)
                items_from_one = all_from_one.select_many(lambda s: s[mname])
            
                valuematrix =list(map(lambda d: [d['timestamp'],d['values'][mname]], items_from_one))
                mdf = DataFrame(valuematrix, columns=["timestamp", mname])
            except:
                raise KeyError("Provided query is invalid (invalid 'values' provided)")

            if result is None:
                result = mdf
            else:
                result = merge(result, mdf, on="timestamp", how="outer")
                #if mname in result:
                #    result = result.append(mdf, ignore_index=True)
                #else:
                #    result = merge(result, mdf, on=["timestamp"], how="outer")
                

        if result.empty:
            return result

        if dropTrailingNa:
            last = min(result.apply(Series.last_valid_index, axis=0))
            result = result.loc[0:last]

        if fillNaMethod is not None:
            result = DataFrame.fillna(result, method=fillNaMethod, axis=0)
            result.dropna(how='all',inplace=True)
            result.dropna(how='all',axis=1,inplace=True)

        if result.empty:
            return result

        #if orderDesc:
        #    result.sort_values(by=["timestamp"], axis=0, ascending=False, inplace=True)
        #else:
        #    result.sort_values(by=["timestamp"], axis=0, ascending=True, inplace=True)

        if result.empty:
            return result

        if convertTimestamp and ("timestamp" in result):
            result["timestamp"] = result["timestamp"].map(ProficloudV3Metrics.dateparse)

        return result


class MetricsStreamV3(Stream):
    """
    This class creates a "streamz"-stream from a ProvicloudV3Connector (or one of its child classes such as ProficloudMetrics).

    :type connector: ProficloudV3Metrics (or subclass)
    :param connector: An initialized connector.
    :type metrics: list(str), str
    :param metrics: A list of metric names (or a single metric name) to query. 
    :type intervalMs: int
    :param intervalMs: Polling interval in milliseconds
    :type bufferTime: dict
    :param bufferTime: The buffer time is the current date and time minus the specified value and unit. Possible unit values are “milliseconds”, “seconds”, “minutes”, “hours”, “days”, “weeks”, “months”, and “years”. For example, if the start time is 5 minutes, the query will return all matching data points for the last 5 minutes. Example value: { "value": "10", "unit": "minutes" } 
    :type convertTimestamp: boolean
    :param convertTimestamp: Convert the timestamp to datetime (Default: False)
    """

    def __init__(self, connector, endpoint_id, metrics, intervalMs, bufferTime, **kwargs):
        self.__connector = connector
        self.__metrics = metrics
        self.__intervalMs = intervalMs
        self.__bufferTime = bufferTime
        self.__endpoint_id = endpoint_id
        self.header = DataFrame(columns=["timestamp"] + metrics)
        """The header for DataFrame creation with the streamz package"""
        super().__init__(ensure_io_loop=True, **kwargs)
        self.stopped = True

    @gen.coroutine
    def poll_metrics(self):
        """
        Polling co-routine. This retrieves metrics from the connector.
        """
        previousTs = None
        newSamples = None
        lastEmit = None

        while True:

            #Check interval after successful emit:
            if lastEmit is None:
                lastEmit = datetime.utcnow()
            else:
                diffMs = (datetime.utcnow() - lastEmit).total_seconds()*1000
                if diffMs < self.__intervalMs and diffMs > 0:
                    yield(gen.sleep((self.__intervalMs - diffMs)/1000.0))


            try:
                end_t = datetime.utcnow()
                start_t = end_t - self.__bufferTime
                try:
                    currentFrame = self.__connector.queryMetrics(self.__endpoint_id, self.__metrics, start_time=start_t, end_time=end_t, dropTrailingNa=True, createDf=True)
                except KeyError as err:
                    #Here, this exception might mean that no data was sent in the requested timedelta. Ignoring
                    currentFrame = None
                    #print(err)
            except:
                raise
                
            if currentFrame is not None:
                if ~currentFrame.empty:
                    if previousTs is not None:
                        newSamples = currentFrame[~currentFrame.timestamp.isin(previousTs)]
                    else:
                        newSamples = currentFrame   
                    previousTs = currentFrame["timestamp"]

                    if (~newSamples.empty) and numpy.array_equal(newSamples.columns, self.header.columns):
                        lastEmit = datetime.utcnow()
                        yield self._emit(newSamples)
                    else:
                        yield gen.sleep(self.__intervalMs/1000.0)
                else:
                    yield gen.sleep(self.__intervalMs/1000.0)
            else:
                yield gen.sleep(self.__intervalMs/1000.0)
            if self.stopped:
                break

    def start(self):
        """
        Start the stream.
        """
        if self.stopped:
            self.stopped = False
            self.loop.add_callback(self.poll_metrics)

    def stop(self):
        """
        Stop the stream.
        """
        if not self.stopped:
            self.stopped = True

    def changeInterval(self, intervalMs):
        self.__intervalMs = intervalMs
