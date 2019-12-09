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
 * Author: Weidong_Zheng
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
//#include "ns3/yans-wifi-channel.h"
#include "ns3/spectrum-wifi-helper.h"
#include "ns3/multi-model-spectrum-channel.h"
#include "ns3/propagation-loss-model.h"
#include "ns3/spectrum-wifi-phy.h"
#include "ns3/wifi-net-device.h"
#include "ns3/wifi-mac.h"
//lr-wpan
#include <ns3/test.h>
#include <ns3/log.h>
#include <ns3/callback.h>
#include <ns3/packet.h>
#include <ns3/simulator.h>
#include <ns3/lr-wpan-error-model.h>
#include <ns3/propagation-loss-model.h>
#include <ns3/lr-wpan-net-device.h>
#include <ns3/spectrum-value.h>
#include <ns3/lr-wpan-spectrum-value-helper.h>
#include <ns3/lr-wpan-mac.h>
#include <ns3/node.h>
#include <ns3/net-device.h>
#include <ns3/single-model-spectrum-channel.h>
#include <ns3/multi-model-spectrum-channel.h>
#include <ns3/mac16-address.h>
#include <ns3/constant-position-mobility-model.h>
#include <ns3/uinteger.h>
#include <ns3/nstime.h>
#include <ns3/abort.h>
#include <ns3/command-line.h>
#include <ns3/lr-wpan-module.h>

//#include <ns3/packet-metadata.h>

// This example considers two hidden stations in an 802.11n network which supports MPDU aggregation.
// The user can specify whether RTS/CTS is used and can set the number of aggregated MPDUs.
//
// Example: ./waf --run "simple-ht-hidden-stations --enableRts=1 --nMpdus=8"
//
// Network topology:
//
//   Wi-Fi 192.168.1.0    lr-wpan(zigbee)
//   AP                   dev1   Mac16Address ("00:02")
//   *     <--- 5m --->   *
//   |5m                  | minDistance
//   |					  |
//   STA                  dev0   Mac16Address ("00:01")
//   (0,0,0)			  (1,1,0)
//
// Packets in this simulation aren't marked with a QosTag so they are considered
// belonging to BestEffort Access Class (AC_BE).

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("WiFiZigBeeInterference");
//ns3::PacketMetadata::Enable ();

static uint32_t g_received = 0;
bool zigbeeTxFlag = false;
static uint32_t zigbee_sent = 0;

Ptr<SpectrumWifiPhy>
GetSpectrumWifiPhyPtr (const NetDeviceContainer &nc)
{
  Ptr<WifiNetDevice> wnd = nc.Get (0)->GetObject<WifiNetDevice> ();
  Ptr<WifiPhy> wp = wnd->GetPhy ();
  return wp->GetObject<SpectrumWifiPhy> ();
}

static void
LrWpanErrorDistanceCallback (McpsDataIndicationParams params, Ptr<Packet> p)
{
  g_received++;
}

static void StateChangeNotification (std::string context, Time now, LrWpanPhyEnumeration oldState, LrWpanPhyEnumeration newState)
{
//  NS_LOG_UNCOND (context << " state change at " << now.GetSeconds ()
//                         << " from " << LrWpanHelper::LrWpanPhyEnumerationPrinter (oldState)
//                         << " to " << LrWpanHelper::LrWpanPhyEnumerationPrinter (newState));
  if (LrWpanHelper::LrWpanPhyEnumerationPrinter (newState) == "BUSY_TX"){
	  zigbeeTxFlag = true;
  	  zigbee_sent ++;
  }
  else
	  zigbeeTxFlag = false;
  if (newState == IEEE_802_15_4_PHY_BUSY_RX)
	  NS_LOG_UNCOND (context << "state change at " << now.GetSeconds() << " to " << LrWpanHelper::LrWpanPhyEnumerationPrinter (newState));
//  NS_LOG_UNCOND (context << "state change at " << now.GetSeconds() << " zigbee flag is " << zigbeeTxFlag);
}

int main (int argc, char *argv[])
{
  uint32_t payloadSize = 1472; //bytes
  double simulationTime = 10; //seconds
  std::string wifiType = "ns3::SpectrumWifiPhy";

//  uint32_t nMpdus = 1;	//Number of aggregated MPDUs
//  uint32_t maxAmpduSize = 0;
//  bool enableRts = 0;

  CommandLine cmd;
  cmd.AddValue ("simulationTime", "Simulation time in seconds", simulationTime);
  cmd.Parse (argc, argv);

  LogComponentEnable ("WiFiZigBeeInterference", LOG_LEVEL_DEBUG);

//  Config::SetDefault ("ns3::WifiRemoteStationManager::RtsCtsThreshold", StringValue ("999999"));

  //Set the maximum size for A-MPDU with regards to the payload size
//  maxAmpduSize = nMpdus * (payloadSize + 200);

  // Set the maximum wireless range to 5 meters in order to reproduce a hidden nodes scenario, i.e. the distance between hidden stations is larger than 5 meters
//  Config::SetDefault ("ns3::RangePropagationLossModel::MaxRange", DoubleValue (5));

  SpectrumWifiPhyHelper spectrumPhy = SpectrumWifiPhyHelper::Default ();

  Ptr<MultiModelSpectrumChannel> spectrumChannel
    = CreateObject<MultiModelSpectrumChannel> ();
//  Ptr<FriisPropagationLossModel> lossModel
//    = CreateObject<FriisPropagationLossModel> ();
  Ptr<LogDistancePropagationLossModel> lossModel
  	= CreateObject<LogDistancePropagationLossModel> ();
  spectrumChannel->AddPropagationLossModel (lossModel);

  Ptr<ConstantSpeedPropagationDelayModel> delayModel
    = CreateObject<ConstantSpeedPropagationDelayModel> ();
  spectrumChannel->SetPropagationDelayModel (delayModel);

  spectrumPhy.SetChannel (spectrumChannel);
  spectrumPhy.SetErrorRateModel ("ns3::NistErrorRateModel");
  spectrumPhy.Set ("Frequency", UintegerValue (2435)); //zigbee channel 17
//  spectrumPhy.Set ("TxPowerStart", DoubleValue (1));
//  spectrumPhy.Set ("TxPowerEnd", DoubleValue (1));
  spectrumPhy.Set ("ChannelWidth",UintegerValue(2));


  // from LrWpanErrorDistancePlot.cc
  Ptr<Node> n0 = CreateObject <Node> ();
  Ptr<Node> n1 = CreateObject <Node> ();
  Ptr<LrWpanNetDevice> dev0 = CreateObject<LrWpanNetDevice> ();
  Ptr<LrWpanNetDevice> dev1 = CreateObject<LrWpanNetDevice> ();
  dev0->SetAddress (Mac16Address ("00:01"));
  dev1->SetAddress (Mac16Address ("00:02"));
  dev0->SetChannel (spectrumChannel);
  dev1->SetChannel (spectrumChannel);
//  std::cout << dev1->GetChannel();
  n0->AddDevice (dev0);
  n1->AddDevice (dev1);
  Ptr<ConstantPositionMobilityModel> mob0 = CreateObject<ConstantPositionMobilityModel> ();
  dev0->GetPhy ()->SetMobility (mob0);
  Ptr<ConstantPositionMobilityModel> mob1 = CreateObject<ConstantPositionMobilityModel> ();
  dev1->GetPhy ()->SetMobility (mob1);

  //waiting to explore
  LrWpanSpectrumValueHelper svh;
  double txPower = 0;
  uint32_t channelNumber = 17;
  Ptr<SpectrumValue> psd = svh.CreateTxPowerSpectralDensity (txPower, channelNumber);
  dev0->GetPhy ()->SetTxPowerSpectralDensity (psd);
//  spectrumChannel->AddRx(dev1->GetPhy ());

  McpsDataIndicationCallback cb0;
  cb0 = MakeCallback (&LrWpanErrorDistanceCallback);
  dev1->GetMac ()->SetMcpsDataIndicationCallback (cb0);

  dev0->GetPhy ()->TraceConnect ("TrxState", std::string ("phy0"), MakeCallback (&StateChangeNotification));

  LrWpanPhyPibAttributes pib;
  pib.phyCurrentChannel = 17;
  pib.phyTransmitPower = 0;
  dev1->GetPhy()->PlmeSetAttributeRequest(phyCurrentChannel, &pib);//phyCurrentChannel = 0x00

  McpsDataRequestParams params;
  params.m_srcAddrMode = SHORT_ADDR;
  params.m_dstAddrMode = SHORT_ADDR;
  params.m_dstPanId = 0;
  params.m_dstAddr = Mac16Address ("00:02");
  params.m_msduHandle = 0;
  params.m_txOptions = 0;

  int minDistance = 5;
//  int maxDistance = 200;  // meters
//  int increment = 1;
  int maxPackets = 1000;
  int packetSize = 20;
  Ptr<Packet> p;
  mob0->SetPosition (Vector (1,1,0));
  mob1->SetPosition (Vector (minDistance,5,0));



  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (1);
//  wifiStaNodes.Create(2);
  NodeContainer wifiApNode;
  wifiApNode.Create (1);

//  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
//  channel.AddPropagationLoss ("ns3::RangePropagationLossModel"); //wireless range limited to 5 meters!

//  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
//  phy.SetPcapDataLinkType (WifiPhyHelper::DLT_IEEE802_11_RADIO);
//  phy.SetChannel (channel.Create ());

  double WifiPow = 16.0206;
  spectrumPhy.Set ("Frequency", UintegerValue (2437));
  spectrumPhy.Set ("ChannelWidth", UintegerValue (20));
  spectrumPhy.Set ("TxPowerStart", DoubleValue (WifiPow)); // dBm
  spectrumPhy.Set ("TxPowerEnd", DoubleValue (WifiPow));


  WifiHelper wifi;
//  wifi.SetStandard(WIFI_PHY_STANDARD_80211b);
  wifi.SetStandard (WIFI_PHY_STANDARD_80211n_2_4GHZ);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
		  	  	  	  	  	  	"DataMode", StringValue ("ErpOfdmRate54Mbps"), //ERP: enhanced rate phy
		  	  	  	  	  	  	"ControlMode", StringValue ("ErpOfdmRate9Mbps")); //HtMcs0
  WifiMacHelper mac;
//#include "ns3/wifi-phy.h"
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

//   Ptr<WifiMac> macSta = mac.Create(staDevices.Get(0));
//   macSta->SetMaxPropagationDelay(MilliSeconds(2));

  Ptr<SpectrumWifiPhy> phySta = GetSpectrumWifiPhyPtr (staDevices);
//  // We expect channel 6, width 20, frequency 2437
//  NS_ASSERT (phySta->GetChannelNumber () == 6);
//  NS_ASSERT (phySta->GetChannelWidth () == 20);
//  NS_ASSERT (phySta->GetFrequency () == 2437);
//  // change the channel to 17, and the cf to 2437
//  phySta->SetAttribute ("Frequency", UintegerValue (2437));
//  phySta->SetAttribute ("ChannelNumber", UintegerValue (6));

//  Config::Set ("/NodeList/*/DeviceList/*/$ns3::WifiNetDevice/Mac/BE_MaxAmpduSize", UintegerValue (maxAmpduSize));

  // Setting mobility model
  MobilityHelper mobility;
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();

  // AP is between the two stations, each station being located at 5 meters from the AP.
  // The distance between the two stations is thus equal to 10 meters.
  // Since the wireless range is limited to 5 meters, the two stations are hidden from each other.
  positionAlloc->Add (Vector (5.0, 0.0, 0.0));
  positionAlloc->Add (Vector (0.0, 0.0, 0.0));
//  positionAlloc->Add (Vector (10.0, 0.0, 0.0));
  mobility.SetPositionAllocator (positionAlloc);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiApNode);
  mobility.Install (wifiStaNodes);

  // Internet stack
  InternetStackHelper stack;
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);

  Ipv4AddressHelper address;
  address.SetBase ("192.168.1.0", "255.255.255.0");
  Ipv4InterfaceContainer StaInterface;
  StaInterface = address.Assign (staDevices);
  Ipv4InterfaceContainer ApInterface;
  ApInterface = address.Assign (apDevice);

  // Setting applications
  uint16_t port = 9;
  UdpServerHelper server (port);
  ApplicationContainer serverApp = server.Install (wifiApNode);
  serverApp.Start (Seconds (0.0));
  serverApp.Stop (Seconds (simulationTime + 1));

  UdpClientHelper client (ApInterface.GetAddress (0), port);
  client.SetAttribute ("MaxPackets", UintegerValue (4294967295u));
  client.SetAttribute ("Interval", TimeValue (Time ("0.0001"))); //packets/s
  client.SetAttribute ("PacketSize", UintegerValue (payloadSize));

  // Saturated UDP traffic from stations to AP
  ApplicationContainer clientApp1 = client.Install (wifiStaNodes);
  clientApp1.Start (Seconds (0.0));
  clientApp1.Stop (Seconds (simulationTime));

  spectrumPhy.EnablePcap ("SimpleWiFiInterference_Ap", apDevice.Get (0));
  spectrumPhy.EnablePcap ("SimpleWiFiInterference_Sta1", staDevices.Get (0));
//  phy.EnablePcap ("SimpleHtHiddenStations_Sta2", staDevices.Get (1));

//  AsciiTraceHelper ascii;
//  spectrumPhy.EnableAsciiAll (ascii.CreateFileStream ("SimpleHtHiddenStations.tr"));

  Simulator::Stop (Seconds (simulationTime + 1));

//  for (int j = minDistance; j < maxDistance;  )
//    {
      for (int i = 0; i < maxPackets; i++)
        {
          p = Create<Packet> (packetSize);
          Simulator::Schedule (MilliSeconds (i), //MicroSeconds: US
                               &LrWpanMac::McpsDataRequest,
                               dev0->GetMac (), params, p);

        }
//      Simulator::Run ();

//      g_received = 0;
//      j += increment;
//      mob1->SetPosition (Vector (j,0,0));
//    }

  Simulator::Run ();

//  std::cout << Simulator::GetContext() << std::endl;
  NS_LOG_DEBUG ("Received " << g_received << " packets for distance " << minDistance);

  uint64_t totalPacketsThrough = DynamicCast<UdpServer> (serverApp.Get (0))->GetReceived ();

  Simulator::Destroy ();

  double throughput = totalPacketsThrough * payloadSize * 8 / (simulationTime * 1000000.0);
  std::cout << "Throughput: " << throughput << " Mbit/s" << '\n';
//  if (throughput < minExpectedThroughput || (maxExpectedThroughput > 0 && throughput > maxExpectedThroughput))
//    {
//      NS_LOG_ERROR ("Obtained throughput " << throughput << " is not in the expected boundaries!");
//      exit (1);
//    }
  return 0;
}
