# OMNI

A very lightweight monitoring system for Raspberry Pi clusters running Kubernetes.

![omni](img/omni_board.png?raw=true "InfluxDB dashboard with Omni data")

## Why?

When I finished my Kubernetes cluster using a few Raspberry Pis, the first thing I wanted to do is install Prometheus + Grafana for monitoring, and so I did. But when I had all of it working I found a few drawbacks:

- The Prometheus exporter pods use a lot of RAM
- The Prometheus exporter pods use a considerable amount of CPU
- Prometheus gathers way too much data that I don't really need.
- The node where the main Prometheus pod is installed gets all of the information and saves it in its own database, constantly performing a lot of writes to the SD card. SD cards under lots of constant writing operations tend to die.

Last but not least, I like to learn how these things work.

## Advantages

Omni has (what I consider) some advantages over the regular Prometheus + Grafana combo:

- It uses almost no RAM (13 Mb)
- It uses almost no CPU
- It gathers only the information I need
- All of the information is sent to an InfluxDB instance that could be outside of the cluster. This means that no information is persisted in the Pis, extending their SD card's lifetime.
- InfluxDB acts as the database and the graph dashboard at the same time, so there is no need to also install Grafana (although you could if you wanted to).

## Prerequisites

For Omni to work, you'll need to have a couple of things running first.

#### InfluxDB

It's a time series database (just like Prometheus) that has nice charts and UI overall.

One of the goals of this project is to avoid constant writing to the SD cards, so you have a few options for the placement of the database:

1. Use InfluxDB's online service (there is even a free tier https://www.influxdata.com/influxdb-pricing/)
2. Run an InfluxDB instance in a server outside the Pi cluster (this what I'm doing right now)
3. If you have better storage in your cluster (like M.2, SSD, etc.) and don't have the SD card limitation, run InfluxDB in the same cluster.

#### Libraries

You'll need to have the `libseccomp2.deb` library installed in each of your nodes to avoid a Python error:

`Fatal Python Error: pyinit_main: can't initialize time`

(more info [here](https://github.com/linuxserver/docker-papermerge/issues/4#issuecomment-735236388))

To install it you can do it in two ways (**only one is needed**):

- **Ansible:** *all nodes at the same time*

    Edit the file `ansible-playbook-libs.yaml` in this repo, add your hosts and run:

    ``` bash
    ansible-playbook install-libs.yaml
    ```

- **SSH:** *one by one*

    Connect into each of your nodes and run:

    ``` bash
    wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.1-1_armhf.deb
    sudo dpkg -i libseccomp2_2.5.1-1_armhf.deb
    ```

Once you have it, everything should work ok.

## Installation

Before deploying Omni you'll have to specify the attributes of your InfluxDB instance.

1. Open `omni-install.yaml` and fill the variables with your InfluxDB instance information.

    *NOTE: The attribute `OMNI_DATA_RATE_SECONDS` specifies the number of seconds between data reporting events that are sent to the InfluxDB server.*

2. Check that everything is running as expected:

``` bash
kubectl get all -n omni-system
```

And you are done! 🎉

## Contributions

Pull requests with improvements and new features are more than welcome.
