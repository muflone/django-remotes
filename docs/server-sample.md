# Django Remotes server sample configuration

After you deploy the server and create a new superuser account you can configure
the server path using the Server Administrator page.

In this example the server will be listening on the address
http://192.168.1.5:8001/

---
## Hosts groups

All the registered hosts can belong to one or more **Hosts groups**, which can
be used to organize the hosts in groups but also to assign some commands to some
hosts.

The default group is called `All hosts` and it's automatically set for each new
registered host (see the Settings section).

We'll configure some new hosts groups called:
- `Windows clients`
- `Windows servers`
- `Linux clients`
- `Linux servers`

We cannot still add others hosts to these groups for now as we haven't
registered any. 

---
## Settings

A required step to complete is to set the server URL from the **Settings**
section.

Edit the **server_url** setting by setting its value to the host url
`http://192.168.1.5:8001/`

A useful setting to set up is **hosts_group_auto_add** which defines the
default group to add hosts to. The default group is called `All hosts`.

Please make sure a hosts group with the specified name exists.

---
## Client registration

Please follow the client setup documentation to configure new clients and add
some hosts to the server by using the server URL http://192.168.1.5:8001/

After a host has been registered you can rename it with a more meaningful name
from the **Users** section. Just be aware the user/host name cannot contain
spaces.

All the newly registered hosts will be automatically added to the `All hosts`
group (see the **hosts_group_auto_add** setting in the previous section) but you
can freely add the same host to multiple groups from the **Hosts groups**
section.

To add a host to another group you could simply open the group details from the
**Hosts groups** section and select the host from the hosts list.

---
## Commands configuration

The commands to execute from the clients need to be valid Python code which will
be executed from the Python interpreter installed in the client.

Each command will be executed as a separated script, so the commands will not
share their state or data between them. If you need to pass some data to a
command you should make use of the input **Variables** for each command and save
some data as results.

Commands can also receive system settings and user variables, see the next
sections for some advanced examples.

The **Timeout** argument defines the maximum time allowed for a command to
complete before getting killed.

---
## Commands groups

Commands are grouped into **Commands Groups** and each group has a hosts group
entitled to use it, a time range for execution and a list of commands.

For example, you can define a group for executing something on all the hosts
for a group, until the 1st of the month, after that date, the command group
expires and cannot be used it anymore.

You can also disable an entire commands group to make it unavailable to the
clients.

The order for the group defined the execution priority against all the others
commands groups. The lower order will make the commands group be executed before
the other groups with higher order.


For our example we'll define a new Commands group called
`Common for all the hosts` as follows:

- **Hosts**: set the `All hosts` group defined before in order to make the
  commands available to all the hosts.
- **Name**: set the name `Common for all the hosts`
- **Order**: set the order 1, as the highest execution priority
- **After**: choose a starting date, like 2021-01-01 00:00:00
- **Before**: choose an ending date, like 2099-01-01 23:59:59
- **Active**: be sure to make the commands group active

You can define commands from the commands group configuration, or you can use
the **Commands** section.

---
### A very simple command with no results

A very simple command with no results is the simpler way to start with
Django Remotes. You can create a new command from the **Commands Group**
section itself.

Create a new command for the `Common for all the hosts` group:

- **Name**: set the name `Hello world`
- **Order**: set the priority 1
- **Command**: set as `print('Hello world')`
- **Active**: leave it checked

After saving the command group you can also watch it from the **Commands**
section.

You can execute the command from the client using the `commands_process` action
(see the client documentation).

After the execution you can watch the execution log from the
**Commands outputs** section:

- **Command**: will show the `Hello world` command
- **Host**: will show the host name which executed the command
- **Output**: will show the string `Hello world` as executed from the command
- **Result**: will contain a list with an empty string, which is the default
  empty replies for a command with no results

The command was executed on the client and the printed text was saved back in
the **Output** field for the command.

---
### A simple command with some results

Let's create another command from the **Commands Groups** section for the same
group we created before:

- **Name**: set the name `Counter to 10`
- **Order**: set the priority 2
- **Active**: leave it checked
- **Command**: set the command
```python
import time

__RESULT__ = []
for counter in range(1, 11):
    print(f'Counting: {counter}')
    __RESULT__.append(counter)
    time.sleep(1)
```

This command will count from 1 to 10, awaiting 1 second for each iteration, and
it will save the results in the special variable **\_\_RESULT\_\_** which holds
the returning values from the command.

When the client will process this command it will await 10 seconds before
completing and the server will receive as results a list of 10 numbers.

You can check out the client execution from the **Commands Outputs** section:

- **Command**: will show the `Counter to 10` command
- **Host**: will show the host name which executed the command
- **Output**: will show multiple lines with the string `Counting: 1` and the
  others numbers
- **Result**: will contain a list with the numbers from 1 to 10, returned from
  the client to the server

**WARNING**: If you had set the previous command timeout to 10 or lower seconds
the command will fail for a timeout, as it cannot be completed in the maximum
allowed time. As a result, the command will not be completed, and it will be
tried again during the next check. Always avoid to set commands that cannot be
completed in the allowed time as the process may continue to try to process the
same command forever, until it will be completed.

---
### A command with results and variables

You can also configure some variables to hold some result for a command with
results, like the previous command.

Before creating a new command we have to define some variable from the
**Variables** section:

- **Category**: you can categorize the variables like you prefer, for this
  example set the category to `Python`
- **Name**: set the variable name like `version`
- **Description**: add a description like `Running Python version`

Create also another variable in the same way:

- **Category**: you can categorize the variables like you prefer, for this
  example set the category to `System`
- **Name**: set the variable name like `platform`
- **Description**: add a description like `System platform in use`

Now we'll create a command which will get some information from the client and
save the result in the two variables set before.

Create a new command like before with the following information:

- **Name**: set the name `Get system information`
- **Order**: set the priority 3
- **Active**: leave it checked
- **Command**: set the following command
```python
import sys

__RESULT__ = [
    sys.platform,
    sys.version
]
print(__RESULT__)
```

This command will get the platform information and the Python version, and it
will return both to the server.

Now we want to capture those values into the two variables set before. Let's
open the **Commands variables** section and assign two variables:

- **Command**: choose the `Get system information` command
- **Variable**: choose the `platform` variable
- **Order**: set the order 0, to point to the first result in the `__RESULT__`
  variable

Create another assignment to the comand variable:

- **Command**: choose the `Get system information` command
- **Variable**: choose the `version` variable
- **Order**: set the order 1, to point to the second result in the `__RESULT__`
  variable

**NOTE**: The `order` attribute refers to the item in the `__RESULT__` list, so
the command results must return enough values to be saved in the variables.

Executing the command from a Microsoft Windows host you can see the following
results in the **Commands outputs** section:

**Command**: will show the `Get system information` command
- **Host**: will show the host name which executed the command
- **Output**: will show the results as a printed list
- **Result**: will contain a list with two values: `win32` for the platform and
  `3.9.9 ...` for the Python version

If you access to the **Variable values** section you'll find two variables set
for the host that executed the command with the value `win32` for the platform
variable and `3.9.9 ...` for the version variable.

In this way we saved the data in a customized variable for each host running
the command. You can define as many variables you need.

---
### A command with input settings and input variables

A configured command can also receive input values from the server in two forms:
- **Input Settings**: refer to global settings, common to every hosts
- **Input Variables**: refer to per-host values, specific only to the requesting
  host. The input variables can be set from the superuser administrator or be
  automatically set from another command like in the previous section.

To test these features we'll create a new setting and we'll use the variables
set from the previous example plus a new added variable.

From the **Settings** section create a new setting like the following:
- **Name**: set the name as `global message`
- **Description**: set the description as `Welcome message`
- **Value**: set as the setting value `Hello everyone`
- **Active**: leave it as checked

In the **Variables** section create a new variable called `name`, the category
is not relevant at all.

In the **Variable values** add a new variable like the following:

- **Host**: select the host running the command
- **Variable**: select the `name` variable
- **Value**: set the variable value as `Muflone VM`

Now we'll create a new command which will use both the setting and the new
variable as input.

These commands have to be set from the **Commands** section:

- **Name**: set the command name as `Pass some settings and variables`
- **Group**: choose the `Common for all the hosts` group
- **Description**: put a descriptive text as `The settings and variables will
  be passed as input for the command`
- **Input settings**: choose the `global message` setting
- **Input variables**: choose the `name` variablee
- **Command**: set the following command:
```python
greet = __SETTINGS__['global message']
host_name = __VARIABLES__['name'] or 'unnamed host'

print(f'{greet} from {host_name}')
```
- **Timeout**: leave the default 15 seconds timeout
- **Order**: set the order to 4
- **Active**: leave it as checked

If you run the command from the same host used in the previous commands you'll
have the following output: `Hello everyone from Muflone VM`; if you run the same
command from another host, whose variable `name` wasn't set you'll receive
instead `Hello everyone from unnamed host` as the variable `name` was passed as
None.

---
## API logs and filtering

The setting called `apilog_enable_logging` allow you to enable logging for the
API calls. If you set its value to 1 all the calls to the API will be logged in
the **Api logs** section.

There's another setting called `apilog_include_arguments` which enables logging
even for the arguments passed to the API call. You can find the arguments in a
field in the **Api logs** section.

The `apilog_filter_users` can be set with a comma separated list of user names
to exclude from the API calls log. For example setting it with `00004,00005`
the hosts with name `00004` and `00005` will not be logged in the Api logs
section.

All the API logs are saved into another database different from the default
database used for configuration and commands.
