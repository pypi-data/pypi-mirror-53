## remotecap

A small utility to perform tcpdump packet captures remotely and stream the results back via SSH. It supports capturing from multiple machines at once using asyncio. Additionally, it displays the capture file sizes and growth rates so you know how much data you're getting.

### Installation
remotecap requires Python >= 3.7. remotecap has these hard dependencies: 

* [`aiofiles`](https://github.com/Tinche/aiofiles)
* [`asyncssh`](https://github.com/ronf/asyncssh)
* [`asciimatics`](https://github.com/peterbrittain/asciimatics)
* [`bcrypt`](https://github.com/pyca/bcrypt/) enables SSH private keys (**strongly recommended**)
* [`libnacl`](https://github.com/saltstack/libnacl) to support more cryptographic options
  * `libnacl` requires [`libsodium`](https://github.com/jedisct1/libsodium) which you should install via your distro's package manager
* [`gssapi`](https://github.com/pythongssapi/python-gssapi)
* [`pyOpenSSL`](https://github.com/pyca/pyopenssl)


To install all hard and development dependencies, run this command:

```bash
pip install 'remotecap[dev]'
```

I would strongly recommend that you do this in a `virtualenv`.

From there, you should be able to just run `remotecap`

### Usage
```text
usage: remotecap [-h] -w FILENAME [-f FILTER] [-k KEY] [-i INTERFACE] [-p]
                 [-s PACKET_LENGTH] [-u USER] [-r REFRESH_INTERVAL]
                 [-n KNOWN_HOSTS] [-e] [-c COMMAND_PATH] [-q] [-d]
                 hosts [hosts ...]

positional arguments:
  hosts                 Hosts to perform the capture on. Required.

optional arguments:
  -h, --help            show this help message and exit
  -w FILENAME, --filename FILENAME
                        File to write to if performing the capture on a single
                        host. Folder to put captures in if capturing from
                        multiple hosts. Required. (default: None)
  -f FILTER, --filter FILTER
                        Filter to pass to tcpdump on the remote host(s).
                        (default: not port 22)
  -k KEY, --key KEY     Location of SSH private keys to use. Can be specified
                        multiple times. (default: None)
  -i INTERFACE, --interface INTERFACE
                        Interface to perform the capture with on the remote
                        host(s). (default: any)
  -p, --password-prompt
                        Prompt for password to use for SSH. SSH keys are
                        recommended instead. (default: False)
  -s PACKET_LENGTH, --packet-length PACKET_LENGTH
                        Length of packets to capture. (default: 0)
  -u USER, --user USER  User to SSH as. The user must have sufficient rights.
                        (default: root)
  -r REFRESH_INTERVAL, --refresh-interval REFRESH_INTERVAL
                        Interval to refresh file size and growth rates at.
                        (default: 5)
  -n KNOWN_HOSTS, --known-hosts KNOWN_HOSTS
                        Known hosts file to use. Specify "None" if you want to
                        disable known hosts. (default:
                        /home/USER/.ssh/known_hosts)
  -e, --sudo            Escalate privileges (sudo) and prompt for password
                        (default: False)
  -c COMMAND_PATH, --command-path COMMAND_PATH
                        Path to tcpdump on the system. Needed if tcpdump isn't
                        in your path. (default: tcpdump)
  -q, --quiet           Do not take over the screen. (default: False)
  -d, --debugger
```

### Reasons this exists

1. I got really sick of sshing into a machine, running `tcpdump` with all of the flags needed, scping the cap file over, and then opening it in Wireshark. Packet traces are incredibly useful in many different situations, so this was bad.
2. Quite often, I had to capture from multiple machines at once. Take the steps above and repeat 2-10 times. I know there are things like tmux or various SSH tools to make this easier, but I wanted something simple that I could share.
3. I got tired of fixing shell scripts I wrote to attempt to resolve 1 and 2. Bash is a wonderful, terrible thing, and it didn't really meet my needs in this context.
4. I wanted semi-live viewing of my capture files. Being able to hit `c-R` to get new packets is nice.
5. I wanted to have a live display of how large my capture files were growing and the rate they were growing at.
6. I wanted more practice using `asyncio` and associated libraries. I've messed with Tornado in the past, but `asyncio` was very different and fun to learn.

### Various notes

* If you get tracebacks complaining about key length, you may need to disable known hosts checking. `cryptography` is a very picky library and it's hard to do much of anything about it.

