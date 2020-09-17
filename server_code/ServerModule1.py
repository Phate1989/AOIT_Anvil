#!/usr/bin/python
# -*- coding: utf-8 -*-

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

# with open('AOIT_Internship_Excel.csv', 'r') as file:
#    SKUList = csv.DictReader(file)
#    line_count = 0
#    SKUs = []
#    # creating SKU List
#    for sku in SKUList:
#        SKUs.append(sku)

@anvil.server.callable
def say_hello(n):
    answer = n * 8
    return [answer]


@anvil.server.callable
def say_media():
 
  # row = tables.app_tables.csv_table.get(file=sku)
  return (4)

def Get_SA_Match(SA_Matches):
  SA_Matched_Dict =[]
  SA_MATCH = []
  for SA_Matched in SA_Matches:
    SA_SKU_MATCH = app_tables.skutable.search(Name=SA_Matched)
    for row in SA_SKU_MATCH:
        SA_MATCH.append({'Sub': SA_Matched, 'Price': row['MSRP']})
  return(SA_MATCH)

def Get_SA_Match_Price(SA_Matches):
  SA_Total = 0
  SA_Matched_Dict =[]
  SA_MATCH = []
  for SA_Matched in SA_Matches:
       SA_Total += float(SA_Matched['Price'])
  return(SA_Total)
  
@anvil.server.callable    
def GetBundle():
  
  SubsToRemove = []
  SubsRemoved = []
  List = []
  SA_Prices = []
  SA_Total = 0
  BundlePrice = 0

  for row in app_tables.bundletable.search():

  # print(list(row))

    line_count = 0

  # creating SKU List

    List.append(dict(row))

    # print(sku)
    

  Requirements = [r['option'] for r in app_tables.options.search()]
  OpenReqs = Requirements
  while len(OpenReqs) != 0:
    print(len(OpenReqs))

    BundleMatches = []
    NoMatch = True

    for Req in OpenReqs:
        for row in List:
            for (k, BundleSKU) in row.items():
                if Req == BundleSKU:
                    NoMatch = False
                    BundleMatches.append({'Sub': Req, 'Bundle': k})

                # print(BundleMatches)

    # Testing finding matches and display
    # YourMatches = "Your Features can be found in "
    # for match in BundleMatches:

    # YourMatches += match['Bundle'] + " "

    track = {}

    for FoundMatch in BundleMatches:
        for (key, value) in FoundMatch.items():
            if key == 'Bundle':
                if value not in track:
                    track[value] = 0
                else:
                    track[value] += 1
    if len(track) != 0:
        MostCommonBundle = max(track, key=track.get)

        
    # print(MostCommonBundle)

    # Get StandAlone leftover apps

    if NoMatch == True:
        for ReqsLeft in OpenReqs:
            OpenReqs.remove(ReqsLeft)
            ReqLeftMatch = app_tables.skutable.search(Name=ReqsLeft)
            for row in ReqLeftMatch:
                SA_Prices.append({'Sub': ReqsLeft, 'Price': row['MSRP']})

    # find subs in most common Bundle

    for lines in List:
        SubsToRemove.append(lines[MostCommonBundle])

    # print(SubsToRemove)

    # remove from open Reqs

    for SubToRemove in SubsToRemove:
        for OpenReq in Requirements:
            if OpenReq == SubToRemove:
                SubsRemoved.append(OpenReq)
                OpenReqs.remove(SubToRemove)
    #for Matched_Subs in SubsRemoved:
    
    SA_Matched_Subs = Get_SA_Match(SubsRemoved)
    SA_Matched_Price = Get_SA_Match_Price(SA_Matched_Subs)
  
  BundleSKUMatch = Get_SA_Match(MostCommonBundle.split(","))
  BundlePrice = Get_SA_Match_Price(BundleSKUMatch)
  
  
  txt_out = "The following Features are available in the bundle " + MostCommonBundle + "\n"
  for sub in SA_Matched_Subs:
    txt_out += sub['Sub'] + " with the price of " + str(sub['Price'])+ "\n"
  txt_out += "Standalone License Total: " +str(SA_Matched_Price) + "\n"
  txt_out += "Bundle License Total: " + str(BundlePrice) + "\n"
  
  
  
  print(SA_Matched_Price)
  print (SA_Matched_Subs)             
  print (OpenReqs)
  print (SA_Prices)

  # Get Stand Alone Price

  # for subs in SA_Prices:
    #   SA_Total += float(subs['Price'])
  # print(SA_Total)
  
  
  return [txt_out]

		