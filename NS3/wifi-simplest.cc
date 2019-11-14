/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2015 Sébastien Deronne
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Sébastien Deronne <sebastien.deronne@gmail.com>
 */
 
#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/uinteger.h"
#include "ns3/boolean.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/mobility-helper.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/udp-client-server-helper.h"
#include "ns3/yans-wifi-channel.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("SimplesSTA2APStations");

int main (int argc, char *argv[])
{
  double simulationTime = 10; //seconds
  
  CommandLine cmd;
  cmd.AddValue ("simulationTime", "Simulation time in seconds", simulationTime);
  cmd.Parse (argc, argv);
  
  NodeContainer WiFiStaNode;
  WiFiStaNode.Create(2);
  NodeContainer WiFiApNode;
  WiFiApNode.Create(2);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();

  YansWifiPhyHelper phy = YansWifiPhyHelper::Default();
  phy.SetPcapDataLinkType(WifiPhyHelper::DLT_IEEE802_11_RADIO);
  phy.SetChannel(channel.Create());

  WifiHelper wifi;
  wifi.SetStandard(WIFI_PHY_STANDARD_80211n_2_4GHZ);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager", "DataMode", StringValue ("HtMcs7"), "ControlMode", StringValue ("HtMcs0"));

  WifiMacHelper mac;
  Ssid ssid = Ssid("SimplesSTA2APStations");
  mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue (ssid));
  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, WiFiStaNode.Get(0));
  mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
  NetDeviceContainer ApDevice;
  ApDevice = wifi.Install(phy, mac, WiFiApNode.Get(0));

  Ssid ssid2 = Ssid("ZigBeeStations");
  mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue (ssid2));
  NetDeviceContainer staDevice2;
  staDevice2 = wifi.Install (phy, mac, WiFiStaNode.Get(1));
  mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid2));
  NetDeviceContainer ApDevice2;
  ApDevice2 = wifi.Install(phy, mac, WiFiApNode.Get(1));

  MobilityHelper mobility;
  mobility.Install(WiFiApNode);
  mobility.Install(WiFiStaNode);

  InternetStackHelper stack;
  stack.Install (WiFiApNode);
  stack.Install (WiFiStaNode);

  Ipv4AddressHelper address;
  address.SetBase ("192.168.1.0", "255.255.255.0");
  Ipv4InterfaceContainer StaInterface;
  StaInterface = address.Assign (staDevices.Get(0));
  Ipv4InterfaceContainer ApInterface;
  ApInterface = address.Assign (ApDevice.Get(0));

  address.SetBase ("192.168.2.0", "255.255.255.0");
  address.Assign (staDevice2.Get(0));
  Ipv4InterfaceContainer ApInterface2 = address.Assign (ApDevice2.Get(0));


  // Setting applications
  uint16_t port = 9;//, port2=5001;
  UdpServerHelper server (port);
  ApplicationContainer serverApp = server.Install (WiFiApNode.Get(0));
  serverApp.Start (Seconds (0.0));
  serverApp.Stop (Seconds (simulationTime + 1));

  UdpClientHelper client (ApInterface.GetAddress (0), port);
  client.SetAttribute ("MaxPackets", UintegerValue (4294967295u));
  client.SetAttribute ("Interval", TimeValue (Time ("0.0001"))); //packets/s
  uint16_t payloadSize = 1472;
  client.SetAttribute ("PacketSize", UintegerValue (payloadSize));

  // Saturated UDP traffic from stations to AP
  ApplicationContainer clientApp1 = client.Install (WiFiStaNode.Get(0));
  clientApp1.Start (Seconds (1.0));
  clientApp1.Stop (Seconds (simulationTime + 1));

  uint16_t port2=5001;
  UdpServerHelper server2 (port2);
  ApplicationContainer serverApp2 = server2.Install (WiFiApNode.Get(1));
  serverApp2.Start (Seconds (0.0));
  serverApp2.Stop (Seconds (simulationTime + 1));

  UdpClientHelper client2 (ApInterface2.GetAddress (0), port2);
  client2.SetAttribute ("MaxPackets", UintegerValue (4294967295u));
  client2.SetAttribute ("Interval", TimeValue (Time ("0.0001"))); //packets/s
  client2.SetAttribute ("PacketSize", UintegerValue (payloadSize));

  // Saturated UDP traffic from stations to AP
  ApplicationContainer clientApp2 = client2.Install (WiFiStaNode.Get(1));
  clientApp2.Start (Seconds (0.9));
  clientApp2.Stop (Seconds (simulationTime + 1));

  //Run Simulation
  Simulator::Stop (Seconds (simulationTime + 1));
  Simulator::Run ();

  uint64_t totalPacketsThrough = DynamicCast<UdpServer> (serverApp.Get (0))->GetReceived ();
  uint64_t totalPacketsThrough2 = DynamicCast<UdpServer> (serverApp2.Get (0))->GetReceived ();

  Simulator::Destroy ();

  double throughput = totalPacketsThrough * payloadSize * 8 / (simulationTime * 1000000.0);
  double throughput2 = totalPacketsThrough2 * payloadSize * 8 / (simulationTime * 1000000.0);
  std::cout << "Throughput: " << throughput << " Mbit/s" << '\n';
  std::cout << "WiFi Throughput: " << throughput2 << " Mbit/s" << '\n';

  return 0;  
}
