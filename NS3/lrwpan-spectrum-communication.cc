/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2011 The Boeing Company
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
 * 此例子用于测试SpectrumWiFiChannel和Phy下的802.15.4通信
 * Author: Weidong_Zheng
 */

/*
 * Try to send data end-to-end through a LrWpanMac <-> LrWpanPhy <->
 * SpectrumChannel <-> LrWpanPhy <-> LrWpanMac chain
 *
 * Trace Phy state changes, and Mac DataIndication and DataConfirm events
 * to stdout
 */
#include <ns3/log.h>
#include <ns3/core-module.h>
#include <ns3/lr-wpan-module.h>
#include <ns3/propagation-loss-model.h>
#include <ns3/propagation-delay-model.h>
#include <ns3/simulator.h>
#include <ns3/single-model-spectrum-channel.h>
#include <ns3/constant-position-mobility-model.h>
#include <ns3/packet.h>

#include "ns3/spectrum-wifi-helper.h"
#include "ns3/multi-model-spectrum-channel.h"

#include <iostream>

using namespace ns3;
NS_LOG_COMPONENT_DEFINE ("ZigbeeSpectrumCommunication");

static uint32_t g_received = 0;
static bool zigbeeTxFlag = false;
static uint32_t zigbee_sent = 0;
static uint32_t zigbeestate[3] = {};

//static void DataIndication (McpsDataIndicationParams params, Ptr<Packet> p)
//{
//  NS_LOG_UNCOND ("Received packet of size " << p->GetSize ());
//}

//static void DataConfirm (McpsDataConfirmParams params)
//{
//  NS_LOG_UNCOND ("LrWpanMcpsDataConfirmStatus = " << params.m_status);
//}

//static void StateChangeNotification (std::string context, Time now, LrWpanPhyEnumeration oldState, LrWpanPhyEnumeration newState)
//{
//  NS_LOG_UNCOND (context << " state change at " << now.GetSeconds ()
//                         << " from " << LrWpanHelper::LrWpanPhyEnumerationPrinter (oldState)
//                         << " to " << LrWpanHelper::LrWpanPhyEnumerationPrinter (newState));
//}

static void
LrWpanErrorDistanceCallback (McpsDataIndicationParams params, Ptr<Packet> p)
{
  g_received++;
}

static void
StateChangeNotification (std::string context, Time now, LrWpanPhyEnumeration oldState, LrWpanPhyEnumeration newState)
{
//  NS_LOG_UNCOND (context << " state change at " << now.GetSeconds ()
//                         << " from " << LrWpanHelper::LrWpanPhyEnumerationPrinter (oldState)
//                         << " to " << LrWpanHelper::LrWpanPhyEnumerationPrinter (newState));
  if (LrWpanHelper::LrWpanPhyEnumerationPrinter (newState) == "BUSY_TX"){
	  zigbeeTxFlag = false;
  	  zigbee_sent ++;
  	  zigbeestate[0] ++;
  }
  else if (newState == IEEE_802_15_4_PHY_RX_ON){
	  zigbeeTxFlag = false;
	  zigbeestate[1]++;
  }
  else
	  zigbeeTxFlag = false;
//  if (newState == IEEE_802_15_4_PHY_BUSY_RX)
//	  NS_LOG_UNCOND (context << "state change at " << now.GetSeconds() << " to " << LrWpanHelper::LrWpanPhyEnumerationPrinter (newState));
//  NS_LOG_UNCOND (context << "state change at " << now.GetSeconds() << " zigbee flag is " << zigbeeTxFlag);
}

void
ReceivePdDataIndication (uint32_t psduLength,
                         Ptr<Packet> p,
                         uint8_t lqi)
{
  NS_LOG_DEBUG ("At: " << Simulator::Now ()
                        << " Received frame size: " << psduLength << " LQI: " <<
                 (uint16_t) lqi);
  g_received++;
}

int main (int argc, char *argv[])
{
  bool verbose = false;
  bool extended = false;

  CommandLine cmd;

  cmd.AddValue ("verbose", "turn on all log components", verbose);
  cmd.AddValue ("extended", "use extended addressing", extended);

  cmd.Parse (argc, argv);

  LrWpanHelper lrWpanHelper;
  if (verbose)
    {
      lrWpanHelper.EnableLogComponents ();
    }

  // Enable calculation of FCS in the trailers. Only necessary when interacting with real devices or wireshark.
  // GlobalValue::Bind ("ChecksumEnabled", BooleanValue (true));

  // Create 2 nodes, and a NetDevice for each one
  Ptr<Node> n0 = CreateObject <Node> ();
  Ptr<Node> n1 = CreateObject <Node> ();

  Ptr<LrWpanNetDevice> dev0 = CreateObject<LrWpanNetDevice> ();
  Ptr<LrWpanNetDevice> dev1 = CreateObject<LrWpanNetDevice> ();

  if (!extended)
    {
      dev0->SetAddress (Mac16Address ("00:01"));
      dev1->SetAddress (Mac16Address ("00:02"));
    }
  else
    {
      Ptr<LrWpanMac> mac0 = dev0->GetMac();
      Ptr<LrWpanMac> mac1 = dev1->GetMac();
      mac0->SetExtendedAddress (Mac64Address ("00:00:00:00:00:00:00:01"));
      mac1->SetExtendedAddress (Mac64Address ("00:00:00:00:00:00:00:02"));
    }

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

//  // Each device must be attached to the same channel
//  Ptr<SingleModelSpectrumChannel> channel = CreateObject<SingleModelSpectrumChannel> ();
//  Ptr<LogDistancePropagationLossModel> propModel = CreateObject<LogDistancePropagationLossModel> ();
//  Ptr<ConstantSpeedPropagationDelayModel> delayModel = CreateObject<ConstantSpeedPropagationDelayModel> ();
//  channel->AddPropagationLossModel (propModel);
//  channel->SetPropagationDelayModel (delayModel);

  dev0->SetChannel (spectrumChannel);
  dev1->SetChannel (spectrumChannel);

  // To complete configuration, a LrWpanNetDevice must be added to a node
  n0->AddDevice (dev0);
  n1->AddDevice (dev1);

  // Trace state changes in the phy
  dev0->GetPhy ()->TraceConnect ("TrxState", std::string ("phy0"), MakeCallback (&StateChangeNotification));
  dev1->GetPhy ()->TraceConnect ("TrxState", std::string ("phy1"), MakeCallback (&StateChangeNotification));

  Ptr<ConstantPositionMobilityModel> mob0 = CreateObject<ConstantPositionMobilityModel> ();
  dev0->GetPhy ()->SetMobility (mob0);
  Ptr<ConstantPositionMobilityModel> mob1 = CreateObject<ConstantPositionMobilityModel> ();
  dev1->GetPhy ()->SetMobility (mob1);
  mob0->SetPosition (Vector (1,1,0));
  mob1->SetPosition (Vector (1,5,0));
//  Ptr<ConstantPositionMobilityModel> sender0Mobility = CreateObject<ConstantPositionMobilityModel> ();
//  sender0Mobility->SetPosition (Vector (0,0,0));
//  dev0->GetPhy ()->SetMobility (sender0Mobility);
//  Ptr<ConstantPositionMobilityModel> sender1Mobility = CreateObject<ConstantPositionMobilityModel> ();
//  // Configure position 10 m distance
//  sender1Mobility->SetPosition (Vector (0,10,0));
//  dev1->GetPhy ()->SetMobility (sender1Mobility);

//  McpsDataConfirmCallback cb0;
//  cb0 = MakeCallback (&DataConfirm);
//  dev0->GetMac ()->SetMcpsDataConfirmCallback (cb0);
  McpsDataIndicationCallback cb0;
  cb0 = MakeCallback (&LrWpanErrorDistanceCallback);
  dev1->GetMac ()->SetMcpsDataIndicationCallback (cb0);

//  McpsDataIndicationCallback cb1;
//  cb1 = MakeCallback (&DataIndication);
//  dev0->GetMac ()->SetMcpsDataIndicationCallback (cb1);

//  McpsDataConfirmCallback cb2;
//  cb2 = MakeCallback (&DataConfirm);
//  dev1->GetMac ()->SetMcpsDataConfirmCallback (cb2);

//  McpsDataIndicationCallback cb3;
//  cb3 = MakeCallback (&DataIndication);
//  dev1->GetMac ()->SetMcpsDataIndicationCallback (cb3);

//  // Tracing
//  lrWpanHelper.EnablePcapAll (std::string ("lr-wpan-data"), true);
//  AsciiTraceHelper ascii;
//  Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream ("lr-wpan-data.tr");
//  lrWpanHelper.EnableAsciiAll (stream);

  dev0->GetPhy ()->TraceConnect ("TrxState", std::string ("phy0"), MakeCallback (&StateChangeNotification));

//  LrWpanPhyPibAttributes pib;
//  pib.phyCurrentChannel = 17;
//  pib.phyTransmitPower = 0;
//  dev1->GetPhy()->PlmeSetAttributeRequest(phyCurrentChannel, &pib);//phyCurrentChannel = 0x00

  // The below should trigger two callbacks when end-to-end data is working
  // 1) DataConfirm callback is called
  // 2) DataIndication callback is called with value of 50
  Ptr<Packet> p0 = Create<Packet> (20);  // 50 bytes of dummy data
  McpsDataRequestParams params;
  params.m_dstPanId = 0;
  if (!extended)
    {
      params.m_srcAddrMode = SHORT_ADDR;
      params.m_dstAddrMode = SHORT_ADDR;
      params.m_dstAddr = Mac16Address ("00:02");
    }
  else
    {
      params.m_srcAddrMode = EXT_ADDR;
      params.m_dstAddrMode = EXT_ADDR;
      params.m_dstExtAddr = Mac64Address ("00:00:00:00:00:00:00:02");
    }
  params.m_msduHandle = 0;
  params.m_txOptions = 0;//TX_OPTION_ACK;

//  dev0->GetMac ()->McpsDataRequest (params, p0);
//  Simulator::ScheduleWithContext (1, Seconds (0.0),
//                                  &LrWpanMac::McpsDataRequest,
//                                  dev0->GetMac (), params, p0);
  for (int i = 0; i < 1000; i++)
    {
      p0 = Create<Packet> (20);
      Simulator::Schedule (MilliSeconds (i), //MicroSeconds: US
                           &LrWpanMac::McpsDataRequest,
                           dev0->GetMac (), params, p0);
      //SChedule()函数每隔delay时间执行一次Event函数
    }
//  // Send a packet back at time 2 seconds
//  Ptr<Packet> p2 = Create<Packet> (60);  // 60 bytes of dummy data
//  if (!extended)
//    {
//      params.m_dstAddr = Mac16Address ("00:01");
//    }
//  else
//    {
//      params.m_dstExtAddr = Mac64Address ("00:00:00:00:00:00:00:01");
//    }
//  Simulator::ScheduleWithContext (2, Seconds (2.0),
//                                  &LrWpanMac::McpsDataRequest,
//                                  dev1->GetMac (), params, p2);

  Simulator::Run ();

  std::cout << "Received zigbee packets num: " << g_received << " times" << '\n';

  Simulator::Destroy ();
  return 0;
}
