# pcap_player

Utility to replay packet captures onto a network interface.


## Install Dependencies

With appropriate permissions:

```sh
pip install pypcapfile
```


## Usage

```sh
./pcap_player.py -h
```

## Caveats

 * Normally only root can use raw sockets.
 * The system may or may not be able to reproduce the timing of the
   packets. The ordering should be ok.
