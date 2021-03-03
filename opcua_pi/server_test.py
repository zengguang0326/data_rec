#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from opcua import ua, Server
from kafka import KafkaConsumer
import json
import random

logging.basicConfig(filename="log.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.WARN)


def readFile(file):
    reader = open(file, "r")
    taglist = []
    for line in reader.readlines():
        if '\xef\xbb\xbf' in line:
            str1 = line.replace('\xef\xbb\xbf', '')
            taglist.append(str(str1.strip().replace(',', '')))
        else:
            taglist.append(str(line.strip().replace(',', '')))
    # print(taglist)
    reader.close
    return taglist


def main():
    # logging.basicConfig(level=logging.ERROR)
    # logger=logging.getLogger("opcua.server.internal_subscription")
    # logger.setLevel(logging.ERROR)
    read = open('config.txt', 'r')
    configs = read.readlines()
    read.close()

    server = Server()
    endpoint = configs[0].split('@')[1].rstrip('\n')
    servername = configs[1].split('@')[1].rstrip('\n')
    kafkaservers = configs[2].split('@')[1].replace("'", "").replace("\"", "").rstrip('\n')
    kafkaserver = kafkaservers[1:-1].split(',')
    kafkatopic = configs[3].split('@')[1].rstrip('\n')
    eventname = configs[4].split('@')[1].rstrip('\n')
    # auto_offset_reset='earlist'
    consumer = KafkaConsumer(kafkatopic, bootstrap_servers=kafkaserver)

    server.set_endpoint(endpoint)
    server.set_server_name(servername)

    print("Program running......")
    print("Please do not close this page")

    # server.load_certificate("certificate-example.der")
    # server.load_private_key("private-key-example.pem")

    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        # ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        # ua.SecurityPolicyType.Basic256Sha256_Sign
    ])

    uri = "http://taiji.com.cn"
    idx = server.register_namespace(uri)

    objs = server.get_objects_node()
    myobj = objs.add_object(idx, "MyObject")

    taglists = readFile("node.csv")
    for taglist in taglists:
        myobj.add_variable(idx, taglist, 6.7).set_writable()
        # myobj.add_variable(idx, taglist, 6.7)

    attrs = readFile("ae_attr.csv")
    custom_etype = server.nodes.base_event_type.add_object_type(idx, eventname)
    for attr in attrs:
        custom_etype.add_property(2, attr, ua.Variant("", ua.VariantType.String))
    myevent = server.get_event_generator(custom_etype, myobj)

    server.start()

    try:
        rootnode = server.get_root_node().get_child(["0:Objects", "{}:MyObject".format(idx)])
        rootnodes = rootnode.get_variables()

        nodeAll = {}
        for i in range(len(rootnodes)):
            nodeId = rootnodes[i]
            nodeName = rootnodes[i].get_browse_name().Name
            nodeAll.update({nodeName: nodeId})

        for message in consumer:
            print("message.value=",message.value)
            recv = message.value.decode("utf8")
            if recv[0] == '{' and recv[-1] == '}':
                nodeKafka = json.loads(recv)
                # print("nodeKafka=", nodeKafka)
                comName = nodeKafka.keys() & nodeAll.keys()
                for row in comName:
                    rootnode.get_child(["2:{}".format(row)]).set_value(nodeKafka[row])

            else:
                datas = recv.split("|")[1:]
                # print("datas=", datas)
                if len(datas)==9:
                    print("ss=",recv)
                    for i in range(len(attrs)):
                        exec("myevent.event.{}='{}'".format(attrs[i], datas[i]))
                    myevent.trigger()
                else:
                    continue

                # print("mysecondevgen=",mysecondevgen)
                # print("mysecondevgen=", myevent.event)


    except Exception as e:
        print(e)

    finally:
        server.stop()


if __name__ == '__main__':
    main()
