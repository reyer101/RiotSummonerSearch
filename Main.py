from RiotAPI import RiotAPI
import RiotConsts as Consts


def main():
    champDict = map_champs_to_id()  #Iterates through Champions.txt and creates a dictionary mapping champ id's to names

    region_menu() # Prints the regions options menu to the user

    while (True):
        try:
            choice = int(input('Enter the number of your region (1-5): '))
        except NameError:
            print 'Enter a number (1-5)'
            continue

        if (1 <= choice <= 5):
            break
        else:
            print 'ERROR: Invalid Region Choice'

    region = Consts.REGIONS['north_america']

    if (choice == 1):
        region = Consts.REGIONS['north_america']
    elif (choice == 2):
        region = Consts.REGIONS['europe_west']
    elif (choice == 3):
        region = Consts.REGIONS['europe_nordic_and_east']
    elif (choice == 4):
        region = Consts.REGIONS['korea']
    elif (choice == 5):
        region = Consts.REGIONS['brazil']

    api = RiotAPI(Consts.KEY, False, region)  # Creates an API to access regional data
    staticAPI = RiotAPI(Consts.KEY, True, region)  # Creates an API to access static data

    summoner = raw_input("Enter your summoner name: ")
    summoner = summoner.replace(" ", "")  #Summoner names are stored without spaces so spaces are deleted
    print

    r = api.get_summoner_by_name(summoner) #r will be a dictionary of dictionaries containing basic summoner information

    try:
        sumID = r[summoner.lower()]['id']  #User enters a summoner name but the information we want is gathered
    except KeyError:                       #by making an API call with a summoner ID.
        print 'Summoner does not exist'
        quit()
    # print sumID

    if(r[summoner.lower()]['summonerLevel']==30): #Only level 30 summoners will have league information
        league = api.get_league_by_id(sumID)
    else:
        name = r[summoner.lower()]['name']
        level = r[summoner.lower()]['summonerLevel']

        print 'Name: {name} \n' \
              'Level: {level} \n'.format(name=name, level=level) #If the summoner is not level 30 then only their
        quit()                                                   #name and level are output

    # print league[str(sumID)][0]['entries'][0]
    wins = league[str(sumID)][0]['entries'][0]['wins']
    losses = league[str(sumID)][0]['entries'][0]['losses']       #Retrieves win and loss information from the league dictionary
    games = wins + losses                                        # and calculates a win percentage

    winRate = float(wins) / games
    winRate = round(winRate, 2) * 100

    name = league[str(sumID)][0]['entries'][0]['playerOrTeamName']
    leaguePoints = league[str(sumID)][0]['entries'][0]['leaguePoints'] #Retrieves summoner rank information
    division = league[str(sumID)][0]['entries'][0]['division']
    tier = league[str(sumID)][0]['tier']

    print "Name: {name} \n" \
          "Rank: {tier} {division} {leaguePoints} LP\n" \
          "Win Rate: %{winRate}\n".format(name=name, tier=tier, division=division,    #Outputs formatted summoner ranked information
                                          winRate=winRate, leaguePoints=leaguePoints)

    champStats = api.get_stats_by_id(sumID)['champions']  #Get's individual champion stats for the summoner

    gamesPlayed = [] #This list will be a list of lists with each inner list containing
                     # a champion id, number of games, and a win rate

    for champs in champStats:
        gamesPlayed.append([champs['id'], champs['stats']['totalSessionsPlayed'],
                            (float(champs['stats']['totalSessionsWon'])/float(champs['stats']['totalSessionsPlayed']))])

    sortedGamesPlayed = sorted(gamesPlayed, key=lambda champ: champ[1], reverse=True) #sorts the lists by games played

    idx = 1
    for champ in sortedGamesPlayed:
        if(champ[0]!=0):                         #Uses the dictionary of champions created at the beginning of the program to
            champ[0] = champDict[str(champ[0])]  #retrieve the champion name corresponding to the id in the sortedGamesPlayed list

    sortedWinPercent = sorted(gamesPlayed, key=lambda champ: champ[2], reverse=True) #Makes another sorted list this time by
                                                                                     #win rate


    #update_champs(staticAPI)  # Only needs to be called if ids change


    print 'Top 3 Most Played Champions:'

    idx = 1
    while idx < 4:
        print '{idx}. {champ}  {games} played'.format(idx=idx, champ=sortedGamesPlayed[idx][0],
                                                  games=sortedGamesPlayed[idx][1])
        idx += 1
                                                          #Outputs the top 3 most played champions with the number of games played
    print
    print 'Top 3 Highest Win Rate: '
    idx = 1
    rank = 1
    while(idx < 50 and rank < 4):
        if(sortedWinPercent[idx][1]>=10):
            print '{idx}. {champ}  %{rate} '.format(idx=rank, champ=sortedWinPercent[idx][0],
                                                  rate=(round(100* sortedWinPercent[idx][2])))
            idx += 1
            rank += 1                                     #Outputs the top 3 highest win rate champions with 10 or more games played
        else:
            idx += 1

def region_menu():
    print '1. North America \n' \
          '2. European West \n' \
          '3. European and Nordic East \n' \
          '4. Korea \n' \
          '5. Brazil \n'
                                             #Matching champion id's to names required making calls to the Riot static data API.
def update_champs(staticAPI):                #Since making calls to the Riot static API took about 20 seconds per call, it didn't
    champFile = open("Champions.txt", 'w')   #make sense to refer to the API every time it was necessary to retrieve a name from an id.
    idx = 1                                  #This function makes one call and populates a file Champions.txt with each line containing
    while (idx < 500):                       #a champion id and name separated by a comma. Now if the id's change or a new champion is
        try:                                 #added simply call this function to update the text file.
            champFile.write(str(idx) + ',' + staticAPI.get_champ_by_id(idx)['name'] + '\n')
            idx += 1
        except KeyError:
            idx += 1
    # Above lines are used to get an update up the champions and their ids
    champFile.close()

def map_champs_to_id(): #Reads from the text file created by update_champs and maps champ id's to names in a dictionary for instant
    champDict = {}      #access throughout the program.
    champFile = open("Champions.txt", 'r')
    for line in champFile:
        line = line.replace('\n','')
        line = line.split(',')
        champDict[line[0]] = line[1]

    return champDict

    champFile.close()



if __name__ == "__main__":
    main()
