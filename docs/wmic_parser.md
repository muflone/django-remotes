# WMIC Parser

## Description

A class named **WmicParser** in the client package allows to ease getting system
information on the Microsoft Windows host through the `wmic` tool, available in
almost any Windows versions.

Its usage requires knowing the alias node to use via WMI, some fields to query
and some condition used to filter the results.

When you create a WmicParser object you have to set the maximum **timeout**
value in seconds the wmic command line will await before failing for timeout.

## Get single information from WMI

The method `get` returns a single value from a single WMI object using an alias,
a field name and a string condition to filter the objects.

A very simple usage can be the following:

```python
from remotes.client.wmic_parser import WmicParser

wmic = WmicParser(timeout=10)
interface = wmic.get(alias='nic',
                     field='NetConnectionID',
                     condition='(PhysicalAdapter = TRUE and NetEnabled = TRUE)')
```

The previous example will query the `nic` alias, will filter the results finding
only the NIC cards with `PhysicalAdapter = TRUE and NetEnabled = TRUE` and
returns the field named `NetConnectionID`.

## Get a list of fields from WMI

The method `get_list` returns a list of items from a single WMI object using an
alias, a field name a string condition to filter the objects.

The `separator` argument is used to specify the items' separator, typically a
comma.

The `strip` argument is used to specify what surrounds a value, for example a
pair of quotes to remove from the values.

The difference with the method `get` is the returned type: `get` will return a
simple string while `get_list` will return a list of strings.

A simple usage can be the following:

```python
from remotes.client.wmic_parser import WmicParser

wmic = WmicParser(timeout=10)
servers = wmic.get_list(alias='nicconfig',
                        field='DNSServerSearchOrder',
                        condition=f'(SettingID=\'{interface_id}\')',
                        separator=',',
                        strip='"')
```

The previous example will query the `nicconfig` alias, will filter the results
finding only the NIC card with `SettingID` equal to interface_id variable and
returns the field named `DNSServerSearchOrder`.

## Get a list of items from WMI

The method `get_values` returns a list of items for any WMI objects using
an alias, a list of field names, a string condition to filter the objects.

The difference with the method `get_list` is the number of items returned:
`get_list` will return a single item while `get_values` will return a list of
dictionaries.

A simple usage can be the following:

```python
from remotes.client.wmic_parser import WmicParser

wmic = WmicParser(timeout=10)
interfaces = wmic.get_values(alias='nic',
                             fields=('NetConnectionID', 'GUID'),
                             condition='PhysicalAdapter = TRUE')
```

The previous example will query the `nic` alias, will filter the results finding
only the NIC cards with `PhysicalAdapter = TRUE` and returns the fields named
`NetConnectionID` and `GUID`.

## Call a method from WMI

The method `call` will call a method for a WMI object using an alias, a string
condition to filter the objects, a method name and a list of string arguments
to pass to the called method.

A simple usage can be the following:

```python
from remotes.client.wmic_parser import WmicParser

wmic = WmicParser(timeout=10)
values = wmic.call(alias='nicconfig',
                   condition=f'(SettingID=\'{interface_id}\')',
                   method='SetDNSServerSearchOrder',
                   parameters=None)
```

The previous example will query the `nicconfig` alias, will filter the results
finding only the NIC card with `SettingID` equal to interface_id variable,
calls the method `SetDNSServerSearchOrder` passing it no arguments.
