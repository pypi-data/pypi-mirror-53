import numpy as np


_GROUP_BY = object()


class _TableMeta(type):
    def __repr__(cls):
        return cls.__name__


class _Table(metaclass=_TableMeta):
    __table_name__ = None  #: Override if subclass name not equal to DB table name

    def __transform__(self, df):
        """
        Override. Apply any post-receive transformation on the DataFrame,
        such as decoding categorical ints into human-readable values.
        """
        return df

    def __repr__(self):
        return str(self.__class__)

    def __iter__(self):
        return iter((attr, getattr(self, attr))
                    for attr in dir(self)
                    if not attr.startswith('_'))

    def _select_agg(self):
        return ', '.join('{0}({1}) as {1}'.format(aggfunc, col)
                         for col, aggfunc in self
                         if aggfunc is not _GROUP_BY)

    def _groupby(self):
        return ', '.join(col
                         for col, aggfunc in self
                         if aggfunc is _GROUP_BY)

    def _columns(self):
        return [col for col, _ in self]

    def __contains__(self, column):
        return (isinstance(column, str) and
                not column.startswith('_') and
                hasattr(self, column))


class ping(_Table):
    NodeId = Iccid = _GROUP_BY
    RTT = 'mean'
    Error = 'sum'
    Operator = Host = 'mode'
    _default_field = 'RTT'


class gps(_Table):
    NodeId = _GROUP_BY
    Latitude = 'mean'
    Longitude = Altitude = Speed = SatelliteCount = 'mean'
    _default_field = 'Latitude'


class sensor(_Table):
    NodeId = _GROUP_BY
    CPU_User = CPU_Apps = FreeRAM = Swap = Temperature = 'mean'
    BootCounter = Uptime = CumUptime = IOWait = 'max'
    _default_field = 'Uptime'


class event(_Table):
    NodeId = _GROUP_BY
    EventType = Message = ExperimentId = 'mode'
    _default_field = 'EventType'


class modem(_Table):
    NodeId = Iccid = _GROUP_BY
    Interface = CID = ENODEBID = PCI = DeviceMode = DeviceState = DeviceSubmode = Frequency = MCC_MNC = Operator = IP_Address = LAC = Band = 'mode'
    RSCP = RSRP = ECIO = RSRQ = RSSI = 'mean'
    _default_field = 'DeviceMode'

    def __transform__(self, df):
        # from https://github.com/MONROE-PROJECT/data-exporter
        if 'DeviceMode' in df:
            df.DeviceMode.replace(
                dict(enumerate(('unknown', 'disconnected', 'no_service', '2G', '3G', 'LTE'))),
                inplace=True)
        if 'DeviceState' in df:
            df.DeviceState.replace(
                dict(enumerate(('unknown', 'registered', 'unregistered', 'connected', 'disconnected'))),
                inplace=True)
        if 'DeviceSubmode' in df:
            df.DeviceSubmode.replace(
                dict(enumerate(('unknown', 'UMTS', 'WCDMA', 'EVDO', 'HSPA', 'HSPA+', 'DC HSPA', 'DC HSPA+', 'HSDPA', 'HSUPA', 'HSDPA+HSUPA', 'HSDPA+', 'HSDPA+HSUPA', 'DC HSDPA+', 'DC HSDPA + HSUPA'))),
                inplace=True)
        return df
    
class nettest(_Table):
    NodeId = Iccid = _GROUP_BY
    Operator = 'mode'
    Download = Upload = RTTClient = RTTServer = 'mean'
    _default_field = 'Download'
    
class tcpcomplete(_Table):
    NodeId = Iccid = _GROUP_BY
    TCPFQDN = 'mode'
    TCPCbytesAll = TCPSbytesAll = TCPDuration = TCPCRTTAVG = TCPCRTTSTD = TCPCPktsRetx = TCPCPktsOOO =  TCPSPktsRetx = TCPSPktsOOO = 'mean'
    _default_field = 'TCPFQDN'
    
    def __transform__(self, df):
        if 'TCPCbytesAll' in df and 'TCPDuration' in df:
            df['TCPGoodPutUpload'] = df['TCPCbytesAll']*8/df['TCPDuration']
        
        if 'TCPSbytesAll' in df and 'TCPDuration' in df:
            df['TCPGoodPutDownload'] = df['TCPSbytesAll']*8/df['TCPDuration']
        return df

        
    
class udpcomplete(_Table):
    NodeId = Iccid = _GROUP_BY
    UDPFQDN = 'mode'
    UDPCbytesAll = UDPSbytesAll = UDPCDurat = UDPSDurat = 'mean'
    _default_field = 'UDPFQDN'
    
    def __transform__(self, df):
        if 'UDPCbytesAll' in df and 'UDPCDurat' in df:
            df['UDPGoodPutUpload'] = df['UDPCbytesAll']*8/df['UDPCDurat']
        
        if 'UDPSbytesAll' in df and 'UDPSDurat' in df:
            df['UDPGoodPutDownload'] = df['UDPSbytesAll']*8/df['UDPSDurat']
        return df


# Hide .mro() member by exposing instances instead of types
ping = ping()
gps = gps()
sensor = sensor()
event = event()
modem = modem()
nettest = nettest()
tcpcomplete = tcpcomplete()
udpcomplete = udpcomplete()


for name, table_type in list(globals().items()):
    if not name.startswith('_') and isinstance(table_type, type) and issubclass(table_type, _Table):
        globals()[name] = table_type()


def _all_tables():
    for name, T in globals().items():
        if isinstance(T, _Table) and not name.startswith('_'):
            yield T


def _check_table(table):
    if isinstance(table, _Table):
        return table
    try:
        return next(T for T in _all_tables()
                    if (T is table or
                        T.__class__.__name__ == table))
    except StopIteration:
        raise ValueError('Unknown MONROE table: {}'.format(table))

class _ModeReducer:
    def __call__(self, series):
        if series.empty:
            return np.nan
        modes = series.mode().values
        return modes[0] if modes.size else np.nan

    def __repr__(self):
        return 'mode'

MODE = _ModeReducer()

# Map columns to their respective sensible aggregation functions
AGGREGATE = {field: (MODE if func in ('mode', _GROUP_BY) else func)
             for table in _all_tables()
             for field, func in table}

_CATEGORICAL_COLUMNS = tuple(field
                             for field, func in AGGREGATE.items()
                             if func is MODE)

# Unit tests

assert str(ping) == 'ping'
assert str(ping.__class__) == 'ping'
assert len(list(iter(ping))) == 6
assert len(ping._columns()) == 6
assert ping._select_agg().count(',') == 3
assert ping._groupby() == 'Iccid, NodeId'

assert ping in _all_tables() and gps in _all_tables()

assert _check_table(ping) is ping
assert _check_table('ping') is ping

try: _check_table('INVALID')
except ValueError: pass
else: assert False
