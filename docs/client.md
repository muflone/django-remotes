# Django Remotes client setup

A client to interact with a Django Remotes server must be first
registered and assigned to some hosts groups.

The registration process consists of the following steps:

1. **Server status**: will get the server status and the services
   discovery URL
2. **Services discovery**: will get the available services discovery
   URLS to instruct the client how to interact with the server
3. **Keys generation**: will generate a new keys pair used to encrypt
   data from the server to the client
4. **Host registration**: will register the host to the server using
   the encryption public key. The registered host will not be yet
   verified
5. **Host verification**: will confirm the host registration

There's a command which will execute every previous operation in a
single command, by queuing all the previous steps.

---

## Server status

To request the server status you can use the following command:

```shell
python client.py \
  --action=status \
  --url <SERVER URL> \
  --settings <SETTINGS FILE>
```

The `SERVER URL` will refer to the server root URL. The path
`api/status` will be automatically added to the URL.

The `SETTINGS FILE` is a text file which will store all the client
information.

At the end of the request the client will receive the services
discovery URL in the following way:

```json
{
  "status": "OK",
  "app_name": "Django Remotes",
  "version": "0.3.0",
  "server_url": "http://192.168.1.50/",
  "discover": "/api/v1/discover/"
}
```

---

## Services discovery

The services discovery command will inform the client about the
available services URLs. To request the server services discovery
you can use the following command:

```shell
python client.py \
  --action=discover \
  --settings <SETTINGS FILE>
```

The server will reply with its services URLs which will be saved
into the settings file:

```json
{
  "status": "OK",
  "endpoints": {
    "command_get": "/api/v1/commands/get/",
    "command_post": "/api/v1/commands/post/",
    "commands_list": "/api/v1/commands/list/",
    "host_register": "/api/v1/host/register/",
    "host_status": "/api/v1/host/status/",
    "host_verify": "/api/v1/host/verify/"
  }
}
```

These commands URLs will be used for the host registration and for the  commands
requests.

---

## Keys generation

The server to client communication is based on asymmetric keys: the client will
own the private key used to decrypt the data and the server will receive the
public key used to encrypt the data.

To generate a new keys pair you can use the following command:

```shell
python client.py \
  --action=generate_keys \
  --settings <SETTINGS FILE> \
  --private_key <PRIVATE KEY FILE PATH> \
  --public_key <PUBLIC KEY FILE PATH>

```

This command will create a new private key and a public key to be send to the
server during the host registration. The settings file will have the file paths
for the two keys files.

---

## Host registration

To request the client host registration you can use the following command
using the host registration token got from the server side (see the server
`registration_token` argument).

```shell
python client.py \
  --action=host_register \
  --settings <SETTINGS FILE> \
  --token <HOST REGISTRATION TOKEN>
```

The client will send to the server also the public key needed to encrypt the
data between the server and the client.

---

## Host verification

After a host has been registered it must be verificated to confirm it and enable
it as a confirmed host.

The client host can be verificated using the following command:

```shell
python client.py \
  --action=host_verify \
  --settings <SETTINGS FILE> \
  --token <HOST REGISTRATION TOKEN>
```

---

## Host registration in a single command

All the previous commands can be shortened in a single command that will launch
all the required commands to register and verify the client host.

You can register a new client host using the following command:

```shell
python client.py \
  --action new_host \
  --url <SERVER URL> \
  --settings <SETTINGS FILE> \
  --token <HOST REGISTRATION TOKEN> \
  --private_key <PRIVATE KEY FILE PATH> \
  --public_key <PUBLIC KEY FILE PATH>
```

A new keys pair will be created and the host will be registered and immediately
confirmed to be activated from the server side.

---

## Host status check

After a host was registered you can check its status using the following
command:

```shell
python client.py \
  --action=host_status \
  --settings <SETTINGS FILE>
```

The answer will contain some details about the host and the assigned hosts
groups:

```json
{
  "status": "OK",
  "app_name": "Django Remotes",
  "version": "0.3.1",
  "id": 165,
  "user_id": 147,
  "user_name": "000147",
  "hosts_groups": [
    {
      "id": 3,
      "name": "All hosts"
    },
    {
      "id": 2,
      "name": "Linux hosts"
    }
  ]
}
```

---

## Commands list

A registered host can request the commands to execute with the following command:

```shell
python client.py \
  --action=commands_list \
  --settings <SETTINGS FILE>
```

The reply from the server will contains the commands to execute:

```json
{
  "status": "OK",
  "results": [
    {
      "group": 4,
      "command": 23
    },
    {
      "group": 6,
      "command": 18
    }
  ]
}
```

The client will be informed it needs to execute the previous commands, along
with their command group ID.

---

## Command execution

```shell
python client.py \
  --action=command_get \
  --settings <SETTINGS FILE> \
  --command <COMMAND ID>
```

The client can execute a single command by its ID and transmit to the server
the command reply and results.

---

## Commands processing

The commands processing will list all the commands to execute using
`commands_list` command and then will execute each one of them with the
`command_get` command.

```shell
python client.py \
  --action=commands_process \
  --settings <SETTINGS FILE>
```

This is most frequent command to use, the process any waiting command to be
executed. It will process every item in the commands list, sending back to the
server each command reply.

---

## Commands monitoring

The commands monitoring is used to set the client in a repeating loop which
will await a predefined number of seconds before processing every command in
list and repeat the await again.

```shell
python client.py \
  --action=commands_monitor \
  --settings <SETTINGS FILE>
  --interval=<SECONDS>
```

A client in service mode will typically use this command, putting it in an
awaiting loop and processing every command on each iteration.
