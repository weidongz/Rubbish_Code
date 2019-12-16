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
 * 此例子用于测试SpectrumWiFiChannel和Phy下的WiFi通信
 * Author: Weidong_Zheng
 */

#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/uinteger.h"
#include "ns3/boolean.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include <array>
#include <iostream>
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/mobility-helper.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/udp-client-server-helper.h"
//#include "ns3/yans-wifi-channel.h"
#include "ns3/spectrum-wifi-helper.h"
#include "ns3/multi-model-spectrum-channel.h"
#include "ns3/propagation-loss-model.h"
#include "ns3/spectrum-wifi-phy.h"
#include "ns3/wifi-net-device.h"
#include "ns3/wifi-mac.h"
#include "ns3/packet-sink-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("WiFiSpectrumCommunication");

static uint32_t wifi_received = 0;
//array<int, 3> wifistates = {};
static uint32_t wifistates[3] = {};

//Ptr<SpectrumWifiPhy>
//GetSpectrumWifiPhyPtr (const NetDeviceContainer &nc)
//{
//  Ptr<WifiNetDevice> wnd = nc.Get (0)->GetObject<WifiNetDevice> ();
//  Ptr<WifiPhy> wp = wnd->GetPhy ();
//  return wp->GetObject<SpectrumWifiPhy> ();
//}

void
PhyStateChanged (Time start, Time duration, WifiPhyState newState)
{
  NS_LOG_FUNCTION ( "" << start << duration << newState);
  if (newState == WifiPhyState::IDLE)
    {
//	  int &idleStateCount = state[0];
	  wifistates[0]++;
//	  std::cout << "Idle state";
    }
  else if (newState == WifiPhyState::RX)
    {
//      rxStateCount++;
//	  std::cout << "Rx state";
    }
  else if (newState == WifiPhyState::CCA_BUSY)
    {
	  wifistates[2]++;
//      ccabusyStateCount++;
//	  std::cout << "Busy state";
    }
  else if (newState == WifiPhyState::TX){
	  newState = WifiPhyState::CCA_BUSY;
	  wifistates[1]++;
  }
}

void ReceivePacket (Ptr<Socket> socket)
{
  while (socket->Recv ())
    {
//      NS_LOG_UNCOND ("Received one packet!");
	  wifi_received++;
    }
}

static void GenerateTraffic (Ptr<Socket> socket, uint32_t pktSize,
                             uint32_t pktCount, Time pktInterval )
{
  if (pktCount > 0)
    {
      socket->Send (Create<Packet> (pktSize));
      Simulator::Schedule (pktInterval, &GenerateTraffic,
                           socket, pktSize, pktCount - 1, pktInterval);
    }
  else
    {
      socket->Close ();
    }
}

int main (int argc, char *argv[])
{
  uint32_t payloadSize = 1472; //bytes
  double simulationTime = 10; //seconds
  std::string wifiType = "ns3::SpectrumWifiPhy";
  Time interPacketInterval = Seconds (0.012);//0.0001
  uint32_t numPackets = 120000;
  double ScheduleTime = 4;

  LogComponentEnable ("WiFiSpectrumCommunication", LOG_LEVEL_DEBUG);

  Ptr<MultiModelSpectrumChannel> spectrumChannel
    = CreateObject<MultiModelSpectrumChannel> ();
  Ptr<LogDistancePropagationLossModel> lossModel
  	= CreateObject<LogDistancePropagationLossModel> ();
  spectrumChannel->AddPropagationLossModel (lossModel);
  Ptr<ConstantSpeedPropagationDelayModel> delayModel
    = CreateObject<ConstantSpeedPropagationDelayModel> ();
  spectrumChannel->SetPropagationDelayModel (delayModel);

  SpectrumWifiPhyHelper spectrumPhy = SpectrumWifiPhyHelper::Default ();
  spectrumPhy.SetChannel (spectrumChannel);
  spectrumPhy.SetErrorRateModel ("ns3::NistErrorRateModel");
  double WifiPow = 16.0206;
  spectrumPhy.Set ("Frequency", UintegerValue (2437));
  spectrumPhy.Set ("ChannelWidth", UintegerValue (20));
  spectrumPhy.Set ("TxPowerStart", DoubleValue (WifiPow)); // dBm
  spectrumPhy.Set ("TxPowerEnd", DoubleValue (WifiPow));
//  spectrumPhy.SetPcapDataLinkType(WifiPhyHelper::DLT_IEEE802_11_RADIO);

  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (1);
  NodeContainer wifiApNode;
  wifiApNode.Create (1);

  WifiHelper wifi;
  wifi.SetStandard (WIFI_PHY_STANDARD_80211n_2_4GHZ);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
		  	  	  	  	  	  	"DataMode", StringValue ("ErpOfdmRate54Mbps"), //ERP: enhanced rate phy
								"ControlMode", StringValue ("ErpOfdmRate24Mbps")); //HtMcs0

  WifiMacHelper mac;
  Ssid ssid = Ssid ("wifiap2sta");
  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid));
  NetDeviceContainer staDevices;
  staDevices = wifi.Install (spectrumPhy, mac, wifiStaNodes);
  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid),
               "EnableBeaconJitter", BooleanValue (false));
  NetDeviceContainer apDevice;
  apDevice = wifi.Install (spectrumPhy, mac, wifiApNode);
//  Ptr<WifiMac> macSta = mac.Create(staDevices.Get(0));
//  macSta->SetMaxPropagationDelay(MilliSeconds(2));

  Ptr<WifiNetDevice> wnd = staDevices.Get (0)->GetObject<WifiNetDevice> ();
  Ptr<WifiPhy> wp = wnd->GetPhy ();
  Ptr<SpectrumWifiPhy> phySta = wp->GetObject<SpectrumWifiPhy> ();
  Ptr<WifiPhyStateHelper> phystatePtr = phySta->GetState ();
  phystatePtr->TraceConnectWithoutContext("State", MakeCallback (&PhyStateChanged));

  Ptr<NetDevice> dev = wifiApNode.Get (0)->GetDevice (0);
  Ptr<WifiNetDevice> wifi_dev = DynamicCast<WifiNetDevice> (dev);
  Ptr<WifiMac> wifi_mac = wifi_dev->GetMac ();
  wifi_mac->SetAttribute("Slot", TimeValue(Time("0.00001")));
  dev = wifiStaNodes.Get(0)->GetDevice(0);
  wifi_dev = DynamicCast<WifiNetDevice> (dev);
  wifi_mac = wifi_dev->GetMac ();
  wifi_mac->SetSlot(MicroSeconds(10)); //change sender slot to 10us

  // Setting mobility model
  MobilityHelper mobility;
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
  positionAlloc->Add (Vector (5.0, 0.0, 0.0));
  positionAlloc->Add (Vector (0.0, 0.0, 0.0));
  mobility.SetPositionAllocator (positionAlloc);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiApNode);
  mobility.Install (wifiStaNodes);

  InternetStackHelper stack;
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);
  Ipv4AddressHelper address;
  address.SetBase ("192.168.1.0", "255.255.255.0");
  Ipv4InterfaceContainer StaInterface;
  StaInterface = address.Assign (staDevices);
  Ipv4InterfaceContainer ApInterface;
  ApInterface = address.Assign (apDevice);

//  //sending via schedule
//  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
//  Ptr<Socket> recvSink = Socket::CreateSocket (wifiApNode.Get (0), tid);
//  InetSocketAddress local = InetSocketAddress (Ipv4Address::GetAny (), 80);
//  recvSink->Bind (local);
//  recvSink->SetRecvCallback (MakeCallback (&ReceivePacket));//calculate wifi packets
//
//  Ptr<Socket> source = Socket::CreateSocket (wifiStaNodes.Get (0), tid);
//  InetSocketAddress remote = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
//  source->SetAllowBroadcast (true);
//  source->Connect (remote);
//
//  Simulator::ScheduleWithContext (source->GetNode ()->GetId (),
//                                  Seconds(ScheduleTime), &GenerateTraffic,
//                                  source, payloadSize, numPackets, interPacketInterval); //schdule:每一秒调用一次

  // Setting applications
  uint16_t port = 9;
  UdpServerHelper server (port);
  ApplicationContainer serverApp = server.Install (wifiApNode);
  serverApp.Start (Seconds (0.0));
  serverApp.Stop (Seconds (simulationTime));

  UdpClientHelper client (ApInterface.GetAddress (0), port);
  client.SetAttribute ("MaxPackets", UintegerValue (numPackets));//4294967295u
  client.SetAttribute ("Interval", TimeValue (Time ("0.00015"))); //packets/s
  client.SetAttribute ("PacketSize", UintegerValue (payloadSize));
  // Saturated UDP traffic from stations to AP
  ApplicationContainer clientApp1 = client.Install (wifiStaNodes);
  clientApp1.Start (Seconds (ScheduleTime));
  clientApp1.Stop (Seconds (simulationTime));

//  spectrumPhy.EnablePcap ("WiFiSpectrumCommunication_Ap", apDevice.Get (0));
//  spectrumPhy.EnablePcap ("WiFiSpectrumCommunication_Sta1", staDevices.Get (0));
////  phy.EnablePcap ("WiFiSpectrumCommunication_Sta2", staDevices.Get (1));
//  AsciiTraceHelper ascii;
//  spectrumPhy.EnableAsciiAll (ascii.CreateFileStream ("WiFiSpectrumCommunication.tr"));

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();
  uint64_t totalPacketsThrough = DynamicCast<UdpServer> (serverApp.Get (0))->GetReceived ();
//  uint64_t totalPacketsThrough = wifi_received;
  Simulator::Destroy();

  double throughput = totalPacketsThrough * payloadSize * 8 / ((simulationTime-ScheduleTime) * 1000000.0);
  std::cout << "Received " << totalPacketsThrough << " wifi packets in " << simulationTime-ScheduleTime << " Seconds\n";
  std::cout << "Throughput: " << throughput << " Mbit/s" << '\n';

  return 0;
}
