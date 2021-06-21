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

### InfluxDB

It's a time series database (just like Prometheus) that has nice charts and UI overall.

One of the goals of this project is to avoid constant writing to the SD cards, so you have a few options for the placement of the database:

- **InfluxDB Cloud:** This might be the easiest option. InfluxDB offers a free plan which should be more than enough for a small Pi Cluster running Omni. More information [here](https://www.influxdata.com/influxdb-pricing/).
- **Docker**: You can also run InfluxDB in dockerin a server outside the Pi cluster (this what I'm doing right now). More information [here](https://hub.docker.com/_/influxdb).
- **In the cluster:** If you have better storage in your cluster (like M.2, SSD, etc.) and don't have the SD card limitation, you could also run InfluxDB in the same cluster you are monitoring.

### Libraries

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

⚠️ **NOTE:** These libraries are for the armhf (32-bit version) operative systems. If you are running a 64-bit version, please refer to [this issue](https://github.com/mattogodoy/omni/issues/3) for instructions.

## Installation

Before deploying Omni you'll need an instance if InfluxDB running somewhere.

### Setting up InfluxDB

Once you have your InfluxDB instance running, you'll have to perform some steps to start receiving data:

1. Log into your InfluxDB instance.
2. Click "Data" on the left panel and then click on the "Buckets" tab.
3. Click on "Create Bucket" at the top right.
4. Write a name for your bucket (you can use anything you want here) and click on "Create". This is where you will store the information sent by Omni.
5. Once you have your bucket created you'll need a token. For this, click on the "Tokens" tab.
6. To create a new one click on "Generate" > "Read/Write Token" at the top right.
7. Write a description for your token and select the bucket you just created in both panels (Read and Write). Click on "Save".
8. Now you'll see your new token in the list. Click on its name to see the details.
9. Here you will see your token. Click on the "Copy to clipboard" button. You'll need this token to configure Omni next.

### Setting up Omni

Now you'll need to specify the attributes of your InfluxDB instance in Omni's configuration:

1. Open `omni-install.yaml` and fill the variables in the `ConfigMap` section with your InfluxDB instance information.

    *NOTE: The attribute `OMNI_DATA_RATE_SECONDS` specifies the number of seconds between data reporting events that are sent to the InfluxDB server.*

2. Deploy Omni in your cluster:

``` bash
kubectl apply -f omni-install.yaml
```

3. Check that everything is running as expected:

``` bash
kubectl get all -n omni-system
```

### Creating a dashboard

Once the Omni DaemonSet is up and running in your cluster, it's already sending telemetry to the Influx database.

To create a dashboard, log into your InfluxDB instance and follow these steps:

1. Click on "Boards" at the left panel and then "Create Dashboard" > "New dashboard".
2. Click on "Add Cell". This will open the query page.
3. In the "FROM" box, click on your bucket.
4. In the "Filter" boxe click on "cpu" > "usage_percent"
5. Select all of your nodes and click on "Submit". You will see your data in the graph.
6. At the top you can set a name and a style for this cell. Also you can change fine tune it further by clickong on "Customize".
7. Once you are happy with the results, click the ✅ button at the top right.
8. And there you have it! Your first cell with data from your cluster 🎉

To visualize more information, repeat these steps for disk usage, memory, temperature, etc.

## Contributions

Pull requests with improvements and new features are more than welcome.
