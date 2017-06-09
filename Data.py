import urllib
import urllib.request
from bs4 import BeautifulSoup
from Sentiment import TwitterClient
import mysql.connector

conn = mysql.connector.connect(user='root',password ="password5",host='localhost',database='performance') #connect to SQL database

def make_soup(url): #Creating a method to open URLs using urllib and Beautifulsoup4 library
    page = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(page, "lxml") #LXML parser used as opposed to html.parser as it scrapes data more quickly
    return soupdata

i = 1

keepersoup = make_soup("http://www.foxsports.com/soccer/stats?competition=1&season=20160&category=GOALKEEPING") #Opening FoxSports Goalkeeper stats URL

keeperbody = keepersoup.find('tbody') #Locating the table of statistics within the url

for record in keeperbody.find_all('tr', class_=False): #Finding each row within the HTML table

    string = '' #The string will represent the row currently being looked at and stats relating to the player will be appended to it

    for element in record.find_all('a', class_='wisbb_fullPlayer'): #Scraping player's full name
        linkExtension = (element['href']) #another link related to the player with more details including playing position

        for value in element.find_next('span'):

            full_name = value.split(',')
            if full_name[0] is not None:
                last_name = full_name[0]
            if len(full_name) > 1:
                first_name = full_name[1]
            else:
                first_name = ''             #Full name will be split into forename and surname, if player has no forename then forename is blank

    string = string + last_name + ', ' + first_name #names are appended to string seperated by comma

    for team in record.find_all('span', class_='wisbb_tableAbbrevLink'): #Scraping the team abbreviation and converting it into the full team name for future use
        team_name = ''
        if team.a is not None:
            team_name = team.a.get_text()
            if team.a.get_text()=="ARS":
                team_name="Arsenal"
            if team.a.get_text()=="BOU":
                team_name="Bournemouth"
            if team.a.get_text()=="BUR":
                team_name="Burnley"
            if team.a.get_text()=="CHE":
                team_name="Chelsea"
            if team.a.get_text()=="CRY":
                team_name="Crystal Palace"
            if team.a.get_text()=="EVE":
                team_name="Everton"
            if team.a.get_text()=="HUL":
                team_name="Hull City"
            if team.a.get_text()=="LEI":
                team_name="Leicester City"
            if team.a.get_text()=="LIV":
                team_name="Liverpool"
            if team.a.get_text()=="MCI":
                team_name="Manchester City"
            if team.a.get_text()=="MID":
                team_name="Middlesbrough"
            if team.a.get_text()=="MUN":
                team_name="Manchester United"
            if team.a.get_text()=="SOU":
                team_name="Southampton"
            if team.a.get_text()=="STK":
                team_name="Stoke City"
            if team.a.get_text()=="SUN":
                team_name="Sunderland"
            if team.a.get_text()=="SWA":
                team_name="Swansea City"
            if team.a.get_text()=="TOT":
                team_name="Tottenham Hotspur"
            if team.a.get_text()=="WAT":
                team_name="Watford"
            if team.a.get_text()=="WBA":
                team_name="West Bromwich Albion"
            if team.a.get_text()=="WHU":
                team_name="West Ham United"
        else:
            team_name = '' #The table can contain players that do not have teams (due to transferring to teams in another league or tech fault so I gave these players a blank team)

        string = string + ', ' + team_name #appending team name to string

    for values in record.find_all('td')[1:]: #Every column after the name and team is fetched and added onto string seperated by comma
        string = string + ', ' + values.get_text()

    string = string + '\n'
    surname, rawForename, team, games_played, games_started, mins_played, wins, draws, losses, goalsConceded, shotsFacedOnTarget, shotsFaced, saves, cleanSheets, yellows, reds  = string.split(',')
    forename = rawForename.replace(" ","") #string is split into key performance stats. Forename was scraped with a space infront so it was stripped here

    positionString = '' #get players position string
    newsoup = make_soup("http://www.foxsports.com/"+linkExtension) #opening related player page to fetch his playing position (goalkeeper in this case)
    positionfind = newsoup.find('span', class_='wisfb_bioLargeSubInfo')
    positionString = positionString + positionfind.get_text()
    position, team_duplicate, heightweight = positionString.split('|') #We only needed position but other bits if info were attached. So I split string.

    if (team_name != ''):
        standingsSoup = make_soup("http://www.foxsports.com/soccer/standings?competition=1") #opening standard Premier League table for general stats

        standingsTable = standingsSoup.find('tbody') #Locating table
        for standingsRecord in standingsTable.find_all('tr', class_=False):

            string = ''

            for team in standingsRecord.find_all('a', class_='wisbb_fullTeam'):

                for team_id in team.find_next('span', class_=False):
                    if team_id == team_name:  #From the table we get the goals conceded and goals scored for the players team
                        string = string + team_name
                        for values in standingsRecord.find_all('td')[1:]:
                            string = string + ', ' + values.get_text()
                        a, b, c, d, e, f, g, h, i, j, k = string.split(",")
                        teamGoalsScored = g.replace(" ", "")
                        teamGoalsConceded = h.replace(" ", "")

#We need to fetch the player's team's next fixture via another url. We will prepare the url extension based on the player's team.
        if team_name == 'Arsenal':
            teamScheduleExtension = 'arsenal'
        if team_name == 'Bournemouth':
            teamScheduleExtension = 'bournemouth'
        if team_name == 'Burnley':
            teamScheduleExtension = 'burnley'
        if team_name == 'Chelsea':
            teamScheduleExtension = 'chelsea'
        if team_name == 'Crystal Palace':
            teamScheduleExtension = 'crystal-palace'
        if team_name == 'Everton':
            teamScheduleExtension = 'everton'
        if team_name == 'Hull City':
            teamScheduleExtension = 'hull-city'
        if team_name == 'Leicester City':
            teamScheduleExtension = 'leicester-city'
        if team_name == 'Liverpool':
            teamScheduleExtension = 'liverpool'
        if team_name == 'Manchester City':
            teamScheduleExtension = 'manchester-city'
        if team_name == 'Manchester United':
            teamScheduleExtension = 'manchester-united'
        if team_name == 'Middlesbrough':
            teamScheduleExtension = 'middlesbrough'
        if team_name == 'Stoke City':
            teamScheduleExtension = 'stoke-city'
        if team_name == 'Southampton':
            teamScheduleExtension = 'southampton'
        if team_name == 'Sunderland':
            teamScheduleExtension = 'sunderland'
        if team_name == 'Swansea City':
            teamScheduleExtension = 'swansea-city'
        if team_name == 'Tottenham Hotspur':
            teamScheduleExtension = 'tottenham-hotspur'
        if team_name == 'Watford':
            teamScheduleExtension = 'watford'
        if team_name == 'West Bromwich Albion':
            teamScheduleExtension = 'west-bromwich-albion'
        if team_name == 'West Ham United':
            teamScheduleExtension = 'west-ham-united'

        nextFixtureSoup = make_soup("http://www.foxsports.com/soccer/" + teamScheduleExtension + "-team-schedule") #open team's fixure page

        fixtureBody = nextFixtureSoup.find('tbody') #Locate table
        string = ''
        winnings = ''
        winCounter = 0
        winPercent = 0
        nextFixtureString = ''

        for fixture in fixtureBody.find_all('span', class_="wisbb_status"):
            for row in fixtureBody.find_all('tr', class_='wisbb_teamScheduleRow')[3:]: #First 3 rows are ignored as these are usually old fixtures

                for element in row.find_all('div', class_='wisbb_fullTeamStacked'): #Get next opposition team's name from span element in second column
                    for value in element.find_all('span')[1]:
                        string = string + value

                for td in row.find_all('td', class_='wisbb_scheduleTextElement'): #Get competion name. We only need EPL (English Premier League) so we'll filter the rest later
                    for div in td.find_all('div', class_='wisbb_textElement'):
                        for href in div.find_all('a'):
                            for span in href.find_all('span', class_='wisbb_main'):
                                string = string + "," + span.get_text()

                for datebox in row.find_all('td', class_='wisbb_scheduleTitleElement '): #Getting the next fixture date from table
                    for date in datebox.find_all('div', class_='wisbb_titleElement'):
                        for span in date.find_all('span'):
                            string = string + "," + span.get_text()

                for upcomingOnly in row.find_all('td', class_='wisbb_gameInfo'): #Get all possible future fixtures
                    for a in upcomingOnly.find_all('a'):
                        for span in a.find_all('span'):
                            string = string + "," + span.get_text()

                string = string + "\n"

        for upcomingFixtures in string.split("\n"):
            if ('EPL') in upcomingFixtures:
                nextEPLFixtures = nextFixtureString + upcomingFixtures + "\n" #Getting only EPL fixtures
                if ('ET') in nextEPLFixtures:
                    nextFixtureString = nextFixtureString + upcomingFixtures + "\n" #From EPL fixtures result, we get only future fixtures, none in the past

        nextFixtureString = nextFixtureString.split('\n')[0]
        nextGameOpposition = nextFixtureString.split(",")[0]
        nextGameDate = nextFixtureString.split(",")[2] #From string, we split it into individual values for future use and database insertion

        j = '' #Using the next game opposition variable we just created, we will fetch some opposition stats
        if nextGameOpposition == "Arsenal":
            j = 1
        if nextGameOpposition == "Bournemouth":
            j = 127
        if nextGameOpposition == "Burnley":
            j = 43
        if nextGameOpposition == "Chelsea":
            j = 4
        if nextGameOpposition == "Crystal Palace":
            j = 6
        if nextGameOpposition == "Everton":
            j = 7
        if nextGameOpposition == "Hull City":
            j = 41
        if nextGameOpposition == "Leicester City":
            j = 26
        if nextGameOpposition == "Liverpool":
            j = 10
        if nextGameOpposition == "Manchester City":
            j = 11
        if nextGameOpposition == "Manchester United":
            j = 12
        if nextGameOpposition == "Middlesbrough":
            j = 13
        if nextGameOpposition == "Southampton":
            j = 20
        if nextGameOpposition == "Stoke City":
            j = 42
        if nextGameOpposition == "Sunderland":
            j = 29
        if nextGameOpposition == "Swansea City":
            j = 45
        if nextGameOpposition == "Tottenham Hotspur":
            j = 21
        if nextGameOpposition == "Watford":
            j = 33
        if nextGameOpposition == "West Bromwich Albion":
            j = 36
        if nextGameOpposition == "West Ham United":
            j = 25

        formSoup = make_soup("https://www.premierleague.com/clubs/" + str(j) + "/club/overview") #Using offial EPL website, we'll retrieve opposition stats by going to their relevant page

        oppLast5Games = '' #We will fetch their last 5 results (W for win, D for draw, L for Loss) for user website. e.g. WWWDL
        oppWinCounter = 0 # Using the previous variable we will calculate the number of wins ('W') in the string
        oppWinPercentage = 0 # Using the previous variable we will calculate the percentage of wins ('W') for prediction algorithm purposes later on

        for oppFormContainer in formSoup.find_all('span', class_="teamForm"):
            oppLast5Games = oppLast5Games + oppFormContainer.get_text() #appending the recent form to string
            if "W" in oppFormContainer:
                oppWinCounter = oppWinCounter + 1 #Counting the number of Wins ('W') in the recent form string

        if (oppWinCounter) == 0: #Calculate the % of wins in the string
            oppWinPercentage = 0
        if (oppWinCounter) == 1:
            oppWinPercentage = 20
        if (oppWinCounter) == 2:
            oppWinPercentage = 40
        if (oppWinCounter) == 3:
            oppWinPercentage = 60
        if (oppWinCounter) == 4:
            oppWinPercentage = 80
        if (oppWinCounter) == 5:
            oppWinPercentage = 100

        j = '' #Now we will fetch exactly the same data as above, but for the player's own team this time
        if team_name == "Arsenal":
            j = 1
        if team_name == "Bournemouth":
            j = 127
        if team_name == "Burnley":
            j = 43
        if team_name == "Chelsea":
            j = 4
        if team_name == "Crystal Palace":
            j = 6
        if team_name == "Everton":
            j = 7
        if team_name == "Hull City":
            j = 41
        if team_name == "Leicester City":
            j = 26
        if team_name == "Liverpool":
            j = 10
        if team_name == "Manchester City":
            j = 11
        if team_name == "Manchester United":
            j = 12
        if team_name == "Middlesbrough":
            j = 13
        if team_name == "Southampton":
            j = 20
        if team_name == "Stoke City":
            j = 42
        if team_name == "Sunderland":
            j = 29
        if team_name == "Swansea City":
            j = 45
        if team_name == "Tottenham Hotspur":
            j = 21
        if team_name == "Watford":
            j = 33
        if team_name == "West Bromwich Albion":
            j = 36
        if team_name == "West Ham United":
            j = 25

        formSoup = make_soup("https://www.premierleague.com/clubs/" + str(j) + "/club/overview")

        teamLast5Games = ''
        teamWinCounter = 0
        teamWinPercentage = 0

        for teamFormContainer in formSoup.find_all('span', class_="teamForm"):
            teamLast5Games = teamLast5Games + teamFormContainer.get_text()
            if "W" in teamFormContainer:
                teamWinCounter = teamWinCounter + 1

        if (teamWinCounter) == 0:
            teamWinPercentage = 0
        if (teamWinCounter) == 1:
            teamWinPercentage = 20
        if (teamWinCounter) == 2:
            teamWinPercentage = 40
        if (teamWinCounter) == 3:
            teamWinPercentage = 60
        if (teamWinCounter) == 4:
            teamWinPercentage = 80
        if (teamWinCounter) == 5:
            teamWinPercentage = 100

        # creating object of TwitterClient Class: based on library from http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
        api = TwitterClient()
        # calling function to get tweets
        tweets = api.get_tweets(query= forename + " " + surname, count=200)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        positiveTweetsPercentage = format(100 * len(ptweets) / len(tweets))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        negativeTweetsPercentage = format(100 * len(ntweets) / len(tweets))
        # percentage of neutral tweets
        #print("Neutral tweets percentage: {} % \ ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

        posNegDifference = float(positiveTweetsPercentage) - float(negativeTweetsPercentage) #Difference in % between positive and negative tweets
        socialMediaScore = 0 #initialising social media score variable

        if (posNegDifference >= 50): #Setting social media score based on pos/neg difference
            socialMediaScore = 10
        if (posNegDifference >= 45 and posNegDifference < 50):
            socialMediaScore = 9
        if (posNegDifference >= 40 and posNegDifference < 45):
            socialMediaScore = 8
        if (posNegDifference >= 35 and posNegDifference < 40):
            socialMediaScore = 7
        if (posNegDifference >= 30 and posNegDifference < 35):
            socialMediaScore = 6
        if (posNegDifference >= 25 and posNegDifference < 30):
            socialMediaScore = 5
        if (posNegDifference >= 20 and posNegDifference < 25):
            socialMediaScore = 4
        if (posNegDifference >= 15 and posNegDifference < 20):
            socialMediaScore = 3
        if (posNegDifference >= 10 and posNegDifference < 15):
            socialMediaScore = 2
        if (posNegDifference >= 5 and posNegDifference < 10):
            socialMediaScore = 1
        if (posNegDifference >= 0 and posNegDifference < 5):
            socialMediaScore = 0
        if (posNegDifference >= -5 and posNegDifference < 0):
            socialMediaScore = -1
        if (posNegDifference >= -10 and posNegDifference < -5):
            socialMediaScore = -2
        if (posNegDifference >= -15 and posNegDifference < -10):
            socialMediaScore = -3
        if (posNegDifference >= -20 and posNegDifference < -15):
            socialMediaScore = -4
        if (posNegDifference >= -25 and posNegDifference < -20):
            socialMediaScore = -5
        if (posNegDifference >= -30 and posNegDifference < -25):
            socialMediaScore = -6
        if (posNegDifference >= -35 and posNegDifference < -30):
            socialMediaScore = -7
        if (posNegDifference >= -40 and posNegDifference < -35):
            socialMediaScore = -8
        if (posNegDifference >= -45 and posNegDifference < -40):
            socialMediaScore = -9
        if (posNegDifference < -45):
            socialMediaScore = -10

        concedingRatio = 0 #Initialising variable for goals conceded per game
        cleansheetChance = 0 #Initialising variable for goalkeeper clean sheet prediction
        shotsToGoalsConcededRatio = 0 #Initialising variable for number of shots on goal per goal
        # Cleansheet prediction
        if (int(games_played) >= 3):
            concedingRatio = int(goalsConceded) / int(games_played)
            if (concedingRatio < 1):
                cleansheetChance = 60
            if (concedingRatio >= 1 and concedingRatio < 2):
                cleansheetChance = 50
            if (concedingRatio >= 2 and concedingRatio < 3):
                cleansheetChance = 40
            if (concedingRatio >= 3):
                cleansheetChance = 30
        else:
            cleansheetChance = 30
        # Cleansheet prediction


        if(shotsFacedOnTarget or goalsConceded ==0): #if shots faced on target or goals conceded is 0, then do nothing
            cleansheetChance = cleansheetChance
        else:
            shotsToGoalsConcededRatio = int(shotsFacedOnTarget) / int(goalsConceded)
            if (shotsToGoalsConcededRatio <= 3):
                cleansheetChance = cleansheetChance - 10 #If keeper concedes a goal within every 3 shots faced then reduce clean sheet chance

    #Alter clean sheet prediction based on social media score
        if (socialMediaScore == -10):
            cleansheetChance = cleansheetChance - 10
        if (socialMediaScore == -9):
            cleansheetChance = cleansheetChance - 9
        if (socialMediaScore == -8):
            cleansheetChance = cleansheetChance - 8
        if (socialMediaScore == -7):
            cleansheetChance = cleansheetChance - 7
        if (socialMediaScore == -6):
            cleansheetChance = cleansheetChance - 6
        if (socialMediaScore == -5):
            cleansheetChance = cleansheetChance - 5
        if (socialMediaScore == -4):
            cleansheetChance = cleansheetChance - 4
        if (socialMediaScore == -3):
            cleansheetChance = cleansheetChance - 3
        if (socialMediaScore == -2):
            cleansheetChance = cleansheetChance - 2
        if (socialMediaScore == -1):
            cleansheetChance = cleansheetChance - 1
        if (socialMediaScore == 0):
            cleansheetChance = cleansheetChance
        if (socialMediaScore == 1):
            cleansheetChance = cleansheetChance + 1
        if (socialMediaScore == 2):
            cleansheetChance = cleansheetChance + 2
        if (socialMediaScore == 3):
            cleansheetChance = cleansheetChance + 3
        if (socialMediaScore == 4):
            cleansheetChance = cleansheetChance + 4
        if (socialMediaScore == 5):
            cleansheetChance = cleansheetChance + 5
        if (socialMediaScore == 6):
            cleansheetChance = cleansheetChance + 6
        if (socialMediaScore == 7):
            cleansheetChance = cleansheetChance + 7
        if (socialMediaScore == 8):
            cleansheetChance = cleansheetChance + 8
        if (socialMediaScore == 9):
            cleansheetChance = cleansheetChance + 9
        if (socialMediaScore == 10):
            cleansheetChance = cleansheetChance + 10

        if (winPercent >= 60):
            cleansheetChance = cleansheetChance + 5
        if (oppWinPercentage < 60):
            cleansheetChance = cleansheetChance + 5
        if (winPercent < 60):
            cleansheetChance = cleansheetChance - 5
        if (oppWinPercentage >= 60):
            cleansheetChance = cleansheetChance - 5


        cursor = conn.cursor() #Insert data fetched into database, goalkeeper table
        cursor.execute(
        "INSERT INTO goalkeeper (`Forename`, `Surname`, `Team`, `Position`, `Games Played`, `Games Started`, `Minutes Played`, `Wins`, `Draws`, `Losses`, `Goals Conceded`, `Shots on target faced`, `Shots faced`, `Saves`, `Clean Sheet`, `Yellow Cards`, `Red Cards`, `Social Media Score`, `Team goals scored`, `Team goals conceded`, `Next opposition`, `Next fixture date`, `Team last 5 matches`, `Team last 5 win percent`, `Opposition last 5 matches`, `Opposition last 5 win percent`, `Chance of clean sheet`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (forename, surname, team_name, position, games_played, games_started, mins_played, wins, draws, losses, goalsConceded, shotsFacedOnTarget, shotsFaced, saves, cleanSheets, yellows, reds, socialMediaScore, teamGoalsScored, teamGoalsConceded, nextGameOpposition, nextGameDate, teamLast5Games, teamWinPercentage, oppLast5Games,oppWinPercentage,cleansheetChance))
        conn.commit()
        print(forename + " " + surname + ", " + team_name) #print what player has been analysed for debugging purposes

    else:
        pass #if player has no team (due to not being in the premier league anymore or simply a technical issue) ignore them and move on to next player
print("All goalkeepers fetched")


for i in range(1, 12): #Now we fetch outfield (defender, midfielder, forward) player data. There are more pages as there are alot more outfield players than goalkeepers so we increment the page once all data has been fetched
    #Now we follow almost exactly the same process as the goalkeeper fetch
    soup = make_soup( "http://www.foxsports.com/soccer/stats? competition=1&season=20160&category=STANDARD&pos=0&team=0&isOpp=0&sort=3&sortOrder=0&page="+str(i))

    body = soup.find('tbody')

    for record in body.find_all('tr', class_=False):

        string = ''

        for element in record.find_all('a', class_='wisbb_fullPlayer'):
            positionLinkExtension = (element['href']) #intialise variable for finding players playing position e.g. midfielder
            teamScheduleExtension = '' #intialise variable for finding players next opposition details

            for value in element.find_next('span'):

                full_name = value.split(',')
                if full_name[0] is not None:
                    last_name = full_name[0]
                if len(full_name) > 1:
                    first_name = full_name[1]
                else:
                    first_name = ''

        string = string + last_name + ',' + first_name #Retrieving name from first column in table and splitting it into forename and surname

        for team in record.find_all('span', class_='wisbb_tableAbbrevLink'): #Changing players team abbreviation to full team name
            team_name = ''
            if team.a is not None:
                team_name = team.a.get_text()
                if team.a.get_text()=="ARS":
                    team_name="Arsenal"
                if team.a.get_text()=="BOU":
                    team_name="Bournemouth"
                if team.a.get_text()=="BUR":
                    team_name="Burnley"
                if team.a.get_text()=="CHE":
                    team_name="Chelsea"
                if team.a.get_text()=="CRY":
                    team_name="Crystal Palace"
                if team.a.get_text()=="EVE":
                    team_name="Everton"
                if team.a.get_text()=="HUL":
                    team_name="Hull City"
                if team.a.get_text()=="LEI":
                    team_name="Leicester City"
                if team.a.get_text()=="LIV":
                    team_name="Liverpool"
                if team.a.get_text()=="MCI":
                    team_name="Manchester City"
                if team.a.get_text()=="MID":
                    team_name="Middlesbrough"
                if team.a.get_text()=="MUN":
                    team_name="Manchester United"
                if team.a.get_text()=="SOU":
                    team_name="Southampton"
                if team.a.get_text()=="STK":
                    team_name="Stoke City"
                if team.a.get_text()=="SUN":
                    team_name="Sunderland"
                if team.a.get_text()=="SWA":
                    team_name="Swansea City"
                if team.a.get_text()=="TOT":
                    team_name="Tottenham Hotspur"
                if team.a.get_text()=="WAT":
                    team_name="Watford"
                if team.a.get_text()=="WBA":
                    team_name="West Bromwich Albion"
                if team.a.get_text()=="WHU":
                    team_name="West Ham United"
            else:
                team_name = ''

            string = string + ', ' + team_name

        for values in record.find_all('td')[1:]:
            string = string + ', ' + values.get_text()
        string = string + '\n'
        surname, forenameRaw, team, games_played, games_started, mins_played, goals, assists, shots, shots_on_goal, yellows, reds = string.split(',')
        forename = forenameRaw.replace(" ", "") #Split string with appended table data. Forename has a space at beginning so we need to strip this space.

        positionString = ''
        newsoup = make_soup("http://www.foxsports.com/"+positionLinkExtension) #open url with players general info including position
        positionfind = newsoup.find('span', class_='wisfb_bioLargeSubInfo')
        positionString = positionString + positionfind.get_text()
        position, team_duplicate, heightweight = positionString.split('|') #Get players details as a string and split. We only need his position

        if(team_name!=''): #If the player has a team assigned to him, do the following. The else statement (if player has no team) is at the end of this scraper
            standingsSoup = make_soup("http://www.foxsports.com/soccer/standings?competition=1")
            # Just like in goalkeeper fetch, we now need to find goals conceded and scored by player's team
            standingsTable = standingsSoup.find('tbody')
            for standingsRecord in standingsTable.find_all('tr', class_=False):

                string = ''

                for team in standingsRecord.find_all('a', class_='wisbb_fullTeam'):

                    for team_id in team.find_next('span', class_=False):
                        if team_id == team_name:
                            string = string + team_name
                            for values in standingsRecord.find_all('td')[1:]:
                                string = string + ', ' + values.get_text()
                            a, b, c, d, e, f, g, h, i, j, k = string.split(",")
                            teamGoalsScored = g.replace(" ", "")
                            teamGoalsConceded = h.replace(" ", "") #These variables have a space at the beginning which we don't need so we strip it

#Get player's/player's team's next opposition team and date, along with team's recent form and win percentage
            if team_name=='Arsenal':
                teamScheduleExtension = 'arsenal'
            if team_name=='Bournemouth':
                teamScheduleExtension = 'bournemouth'
            if team_name=='Burnley':
                teamScheduleExtension = 'burnley'
            if team_name=='Chelsea':
                teamScheduleExtension = 'chelsea'
            if team_name=='Crystal Palace':
                teamScheduleExtension = 'crystal-palace'
            if team_name=='Everton':
                teamScheduleExtension = 'everton'
            if team_name=='Hull City':
                teamScheduleExtension = 'hull-city'
            if team_name=='Leicester City':
                teamScheduleExtension = 'leicester-city'
            if team_name=='Liverpool':
                teamScheduleExtension = 'liverpool'
            if team_name=='Manchester City':
                teamScheduleExtension = 'manchester-city'
            if team_name=='Manchester United':
                teamScheduleExtension = 'manchester-united'
            if team_name=='Middlesbrough':
                teamScheduleExtension = 'middlesbrough'
            if team_name=='Stoke City':
                teamScheduleExtension = 'stoke-city'
            if team_name=='Southampton':
                teamScheduleExtension = 'southampton'
            if team_name=='Sunderland':
                teamScheduleExtension = 'sunderland'
            if team_name=='Swansea City':
                teamScheduleExtension = 'swansea-city'
            if team_name=='Tottenham Hotspur':
                teamScheduleExtension = 'tottenham-hotspur'
            if team_name=='Watford':
                teamScheduleExtension = 'watford'
            if team_name=='West Bromwich Albion':
                teamScheduleExtension = 'west-bromwich-albion'
            if team_name=='West Ham United':
                teamScheduleExtension = 'west-ham-united'

            nextFixtureSoup = make_soup("http://www.foxsports.com/soccer/"+teamScheduleExtension+"-team-schedule")

            fixtureBody = nextFixtureSoup.find('tbody')
            string = ''
            winnings = ''
            winCounter = 0
            winPercent = 0
            nextFixtureString = ''

            for fixture in fixtureBody.find_all('span', class_="wisbb_status"):
                for row in fixtureBody.find_all('tr', class_='wisbb_teamScheduleRow')[3:]:

                    for element in row.find_all('div', class_='wisbb_fullTeamStacked'):
                        for value in element.find_all('span')[1]:
                            string = string + value

                    for td in row.find_all('td', class_='wisbb_scheduleTextElement'):
                        for div in td.find_all('div', class_='wisbb_textElement'):
                            for href in div.find_all('a'):
                                for span in href.find_all('span', class_='wisbb_main'):
                                    string = string + "," + span.get_text()

                    for datebox in row.find_all('td', class_='wisbb_scheduleTitleElement '):
                        for date in datebox.find_all('div', class_='wisbb_titleElement'):
                            for span in date.find_all('span'):
                                string = string + "," + span.get_text()

                    for upcomingOnly in row.find_all('td', class_='wisbb_gameInfo'):
                        for a in upcomingOnly.find_all('a'):
                            for span in a.find_all('span'):
                                string = string + "," + span.get_text()

                    string = string + "\n"

            for upcomingFixtures in string.split("\n"):
                if ('EPL') in upcomingFixtures:
                    nextEPLFixtures = nextFixtureString + upcomingFixtures + "\n"
                    if ('ET') in nextEPLFixtures:
                        nextFixtureString = nextFixtureString + upcomingFixtures + "\n"

            nextFixtureString = nextFixtureString.split('\n')[0]
            nextGameOpposition= nextFixtureString.split(",")[0]
            nextGameDate= nextFixtureString.split(",")[2]

            j = ''
            if nextGameOpposition == "Arsenal":
                j = 1
            if nextGameOpposition == "Bournemouth":
                j = 127
            if nextGameOpposition == "Burnley":
                j = 43
            if nextGameOpposition == "Chelsea":
                j = 4
            if nextGameOpposition == "Crystal Palace":
                j = 6
            if nextGameOpposition == "Everton":
                j = 7
            if nextGameOpposition == "Hull City":
                j = 41
            if nextGameOpposition == "Leicester City":
                j = 26
            if nextGameOpposition == "Liverpool":
                j = 10
            if nextGameOpposition == "Manchester City":
                j = 11
            if nextGameOpposition == "Manchester United":
                j = 12
            if nextGameOpposition == "Middlesbrough":
                j = 13
            if nextGameOpposition == "Southampton":
                j = 20
            if nextGameOpposition == "Stoke City":
                j = 42
            if nextGameOpposition == "Sunderland":
                j = 29
            if nextGameOpposition == "Swansea City":
                j = 45
            if nextGameOpposition == "Tottenham Hotspur":
                j = 21
            if nextGameOpposition == "Watford":
                j = 33
            if nextGameOpposition == "West Bromwich Albion":
                j = 36
            if nextGameOpposition == "West Ham United":
                j = 25

            formSoup = make_soup("https://www.premierleague.com/clubs/" + str(j) + "/club/overview") #We need to get oppositions recent form via the official EPL website

            oppLast5Games = ''
            oppWinCounter = 0
            oppWinPercentage = 0

            for oppFormContainer in formSoup.find_all('span', class_="teamForm"):
                oppLast5Games = oppLast5Games + oppFormContainer.get_text()
                if "W" in oppFormContainer:
                    oppWinCounter = oppWinCounter + 1

            if (oppWinCounter) == 0:
                oppWinPercentage = 0
            if (oppWinCounter) == 1:
                oppWinPercentage = 20
            if (oppWinCounter) == 2:
                oppWinPercentage = 40
            if (oppWinCounter) == 3:
                oppWinPercentage = 60
            if (oppWinCounter) == 4:
                oppWinPercentage = 80
            if (oppWinCounter) == 5:
                oppWinPercentage = 100

            j = ''
            if team_name == "Arsenal":
                j = 1
            if team_name == "Bournemouth":
                j = 127
            if team_name == "Burnley":
                j = 43
            if team_name == "Chelsea":
                j = 4
            if team_name == "Crystal Palace":
                j = 6
            if team_name == "Everton":
                j = 7
            if team_name == "Hull City":
                j = 41
            if team_name == "Leicester City":
                j = 26
            if team_name == "Liverpool":
                j = 10
            if team_name == "Manchester City":
                j = 11
            if team_name == "Manchester United":
                j = 12
            if team_name == "Middlesbrough":
                j = 13
            if team_name == "Southampton":
                j = 20
            if team_name == "Stoke City":
                j = 42
            if team_name == "Sunderland":
                j = 29
            if team_name == "Swansea City":
                j = 45
            if team_name == "Tottenham Hotspur":
                j = 21
            if team_name == "Watford":
                j = 33
            if team_name == "West Bromwich Albion":
                j = 36
            if team_name == "West Ham United":
                j = 25

            formSoup = make_soup("https://www.premierleague.com/clubs/" + str(j) + "/club/overview")

            teamLast5Games = ''
            teamWinCounter = 0
            teamWinPercentage = 0

            for teamFormContainer in formSoup.find_all('span', class_="teamForm"):
                teamLast5Games = teamLast5Games + teamFormContainer.get_text()
                if "W" in teamFormContainer:
                    teamWinCounter = teamWinCounter + 1

            if (teamWinCounter) == 0:
                teamWinPercentage = 0
            if (teamWinCounter) == 1:
                teamWinPercentage = 20
            if (teamWinCounter) == 2:
                teamWinPercentage = 40
            if (teamWinCounter) == 3:
                teamWinPercentage = 60
            if (teamWinCounter) == 4:
                teamWinPercentage = 80
            if (teamWinCounter) == 5:
                teamWinPercentage = 100


            socialMediaScore = 0
            positiveTweetsPercentage = 0
            negativeTweetsPercentage = 0
            # creating object of TwitterClient Class: based on library from http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
            api = TwitterClient()
            # calling function to get tweets
            tweets = api.get_tweets(query=forename + " " + surname, count=200)

            # picking positive tweets from tweets
            if(len(tweets)==0):
                socialMediaScore = 0
            else:
                # percentage of positive tweets
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                positiveTweetsPercentage = format(100 * len(ptweets) / len(tweets))
                # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                # percentage of negative tweets
                negativeTweetsPercentage = format(100 * len(ntweets) / len(tweets))

            posNegDifference = float(positiveTweetsPercentage) - float(negativeTweetsPercentage) #Difference in % between positive and negative tweets

            if (posNegDifference >= 50):
                socialMediaScore = 10
            if (posNegDifference >= 45 and posNegDifference < 50):
                socialMediaScore = 9
            if (posNegDifference >= 40 and posNegDifference < 45):
                socialMediaScore = 8
            if (posNegDifference >= 35 and posNegDifference < 40):
                socialMediaScore = 7
            if (posNegDifference >= 30 and posNegDifference < 35):
                socialMediaScore = 6
            if (posNegDifference >= 25 and posNegDifference < 30):
                socialMediaScore = 5
            if (posNegDifference >= 20 and posNegDifference < 25):
                socialMediaScore = 4
            if (posNegDifference >= 15 and posNegDifference < 20):
                socialMediaScore = 3
            if (posNegDifference >= 10 and posNegDifference < 15):
                socialMediaScore = 2
            if (posNegDifference >= 5 and posNegDifference < 10):
                socialMediaScore = 1
            if (posNegDifference >= 0 and posNegDifference < 5):
                socialMediaScore = 0
            if (posNegDifference >= -5 and posNegDifference < 0):
                socialMediaScore = -1
            if (posNegDifference >= -10 and posNegDifference < -5):
                socialMediaScore = -2
            if (posNegDifference >= -15 and posNegDifference < -10):
                socialMediaScore = -3
            if (posNegDifference >= -20 and posNegDifference < -15):
                socialMediaScore = -4
            if (posNegDifference >= -25 and posNegDifference < -20):
                socialMediaScore = -5
            if (posNegDifference >= -30 and posNegDifference < -25):
                socialMediaScore = -6
            if (posNegDifference >= -35 and posNegDifference < -30):
                socialMediaScore = -7
            if (posNegDifference >= -40 and posNegDifference < -35):
                socialMediaScore = -8
            if (posNegDifference >= -45 and posNegDifference < -40):
                socialMediaScore = -9
            if (posNegDifference < -45):
                socialMediaScore = -10

            if(int(goals)==0):
                goalRatio = 5 #if player has no goals, give him ratio of 5 (which is a poor performance return), we will see why below
            if(int(goals) > 0):
                goalRatio = int(games_played) / int(goals) #calculate ratio: games played before scoring a goal, on average

            if(int(assists)==0):
                assistRatio = 5
            if(int(assists)>0):
                assistRatio = int(games_played) / int(assists) #Same reasoning for goals ratio
            concedingRatio = 0 #Initialising variable for number of goals conceded per game, on average
            scoringChance = 0 #initialising variable for chance % of player scoring a goal
            assistChance = 0 #initialising variable for chance % of player assisting a goal
            cardedChance = 0 #initialising variable for chance % of player being punished with a yellow or red card
            concedingChance = 0 #initialising variable for chance % of player conceding a goal
            shotRatio = 0 #Initialising variable for number of shots taken before hitting a shot on target, on average
            if(int(goals)==0):
                minsPerGoal=0 #if the player has scored no goals, set minsPerGoal to 0 as a default value, it won't affect anything
            else: minsPerGoal = int(mins_played) / int(goals) #Number of minutes gone before a player scores, on average

            if(int(assists)==0):
                minsPerAssist =0
            else: minsPerAssist = int(mins_played) / int(assists) #Same reasoning as for minutes per goal

            # goal prediction
            if (int(games_played) >= 3): #Player must have played 3+ games to get an accurate prediction
                if (goalRatio < 1):
                    scoringChance = 70 #If player scores a goal in less than a full game, on average, he has 70% chance of scoring as he is very likely to score based on current seasons stats
                if (goalRatio >= 1 and goalRatio < 2): #As ratio decreases, so does chance of scoring
                    scoringChance = 60
                if (goalRatio >= 2 and goalRatio < 3):
                    scoringChance = 50
                if (goalRatio >= 3 and goalRatio < 4):
                    scoringChance = 40
                if (goalRatio >=4):
                    scoringChance = 30
            else:
                scoringChance = 30 #If player has played less than 3 games, we give him a default low chance of scoring as we don't have enough data to form an accurate prediction

            if(int(shots) or int(shots_on_goal) == 0):
                shotRatio = 5
            else: shotRatio = int(shots)/int(shots_on_goal)

            if(shotRatio<2):
                    scoringChance = scoringChance + 5 #If player gets a shot on target in less than two shots on average, he has a higher chance of scoring as he is accurate in front of goal


            # Assist prediction
            if (int(games_played) >= 3): #Assist chance based on assist ratio, very similar reasoning to goal ratio and chance of scoring above
                if (assistRatio < 1):
                    assistChance = 70
                if (assistRatio >= 1 and assistRatio < 2):
                    assistChance = 60
                if (assistRatio >= 2 and assistRatio < 3):
                    assistChance = 50
                if (assistRatio >= 3 and assistRatio < 4):
                    assistChance = 40
                if (assistRatio >=4):
                    assistChance = 30
            else: assistChance = 30

            # Carded prediction
            if (int(games_played) >= 3):
                if (int(yellows) == 0 or int(reds) == 0):
                    cardedChance = 25 #General low chance of scoring if no cards received all season
                else: cardedChance = 100 / (int(games_played) / (int(yellows) + int(reds))) #else if they have cards, calculate chance of receiving one
            else:
                cardedChance = 30

            # Conceding prediction
            if (int(games_played) >= 3):
                concedingRatio = int(teamGoalsConceded) / int(games_played)
                if (concedingRatio < 1):
                    concedingChance = 40
                if (concedingRatio >= 1 and concedingRatio < 2):
                    concedingChance = 50
                if (concedingRatio >= 2 and concedingRatio < 3):
                    concedingChance = 60
                if (concedingRatio >= 3):
                    concedingChance = 70
            else: concedingChance = 30

            if (socialMediaScore == -10):
                scoringChance = scoringChance - 10 #Negative twitter feedback results in less chance of scoring
                assistChance = assistChance - 10 #Negative twitter feedback results in less chance of assisting
                cardedChance = cardedChance + 10 #Negative twitter feedback results in higher chance of receiving a card (for being erratic or abusive for example)
                concedingChance = concedingChance + 10 #Negative twitter feedback results in higher chance of conceding a goal, player may feel less confident
            if (socialMediaScore == -9):
                scoringChance = scoringChance - 9
                assistChance = assistChance - 9
                cardedChance = cardedChance + 9
                concedingChance = concedingChance + 9
            if (socialMediaScore == -8):
                scoringChance = scoringChance - 8
                assistChance = assistChance - 8
                cardedChance = cardedChance + 8
                concedingChance = concedingChance + 8
            if (socialMediaScore == -7):
                scoringChance = scoringChance - 7
                assistChance = assistChance - 7
                cardedChance = cardedChance + 7
                concedingChance = concedingChance + 7
            if (socialMediaScore == -6):
                scoringChance = scoringChance - 6
                assistChance = assistChance - 6
                cardedChance = cardedChance + 6
                concedingChance = concedingChance + 6
            if (socialMediaScore == -5):
                scoringChance = scoringChance - 5
                assistChance = assistChance - 5
                cardedChance = cardedChance + 5
                concedingChance = concedingChance + 5
            if (socialMediaScore == -4):
                scoringChance = scoringChance - 4
                assistChance = assistChance - 4
                cardedChance = cardedChance + 4
                concedingChance = concedingChance + 4
            if (socialMediaScore == -3):
                scoringChance = scoringChance - 3
                assistChance = assistChance - 3
                cardedChance = cardedChance + 3
                concedingChance = concedingChance + 3
            if (socialMediaScore == -2):
                scoringChance = scoringChance - 2
                assistChance = assistChance - 2
                cardedChance = cardedChance + 2
                concedingChance = concedingChance + 2
            if (socialMediaScore == -1):
                scoringChance = scoringChance - 1
                assistChance = assistChance - 1
                cardedChance = cardedChance + 1
                concedingChance = concedingChance + 1
            if (socialMediaScore == 0):
                scoringChance = scoringChance
                assistChance = assistChance
                cardedChance = cardedChance
                concedingChance = concedingChance
            if (socialMediaScore == 1):
                scoringChance = scoringChance + 1
                assistChance = assistChance + 1
                cardedChance = cardedChance - 1
                concedingChance = concedingChance - 1
            if (socialMediaScore == 2):
                scoringChance = scoringChance + 2
                assistChance = assistChance + 2
                cardedChance = cardedChance - 2
                concedingChance = concedingChance - 2
            if (socialMediaScore == 3):
                scoringChance = scoringChance + 3
                assistChance = assistChance + 3
                cardedChance = cardedChance - 3
                concedingChance = concedingChance - 3
            if (socialMediaScore == 4):
                scoringChance = scoringChance + 4
                assistChance = assistChance + 4
                cardedChance = cardedChance - 4
                concedingChance = concedingChance - 4
            if (socialMediaScore == 5):
                scoringChance = scoringChance + 5
                assistChance = assistChance + 5
                cardedChance = cardedChance - 5
                concedingChance = concedingChance - 5
            if (socialMediaScore == 6):
                scoringChance = scoringChance + 6
                assistChance = assistChance + 6
                cardedChance = cardedChance - 6
                concedingChance = concedingChance - 6
            if (socialMediaScore == 7):
                scoringChance = scoringChance + 7
                assistChance = assistChance + 7
                cardedChance = cardedChance - 7
                concedingChance = concedingChance - 7
            if (socialMediaScore == 8):
                scoringChance = scoringChance + 8
                assistChance = assistChance + 8
                cardedChance = cardedChance - 8
                concedingChance = concedingChance - 8
            if (socialMediaScore == 9):
                scoringChance = scoringChance + 9
                assistChance = assistChance + 9
                cardedChance = cardedChance - 9
                concedingChance = concedingChance - 9
            if (socialMediaScore == 10):
                scoringChance = scoringChance + 10
                assistChance = assistChance + 10
                cardedChance = cardedChance - 10
                concedingChance = concedingChance - 10

            if (winPercent >= 60):
                scoringChance = scoringChance + 5 #if player's team has won 60% of last 5 games, momentum will be on the player's side and may have a higher chance of scoring
                assistChance = assistChance + 5 #if player's team has won 60% of last 5 games, momentum will be on the player's side and may have a higher chance of assisting
            if (oppWinPercentage < 60):
                scoringChance = scoringChance + 5 #if opposition has won less than 60% of last 5 games, they may be low in confidence and player in question may have higher chance of scoring/assisting
                assistChance = assistChance + 5
            if (winPercent < 60):
                scoringChance = scoringChance - 5 #If team's form is not good, scoring/assisting chances may be lower due to confidence or team constantly defending as they're always losing
                assistChance = assistChance - 5
                concedingChance = concedingChance + 5
            if (oppWinPercentage >= 60): #if opposition is in good form, player may not feel that confident in scoring or assisting
                scoringChance = scoringChance - 5
                assistChance = assistChance - 5
                concedingChance = concedingChance + 5

            if (position == "Defender"):
                scoringChance = scoringChance - 5 #if player is defender, reduce scoring/assisting % by 5%. Defenders don't often get involved in goal scoring opportunities
                assistChance = assistChance - 5

            if (position =="Goalkeeper"): #it is extremely unlikely a goalkeeper will score/assist so percentages are set to 2%
                scoringChance = 2
                assistChance = 2
            #insert all data and predictions into database, in the outfield table
            cursor = conn.cursor()
            cursor.execute("INSERT INTO outfield (`Surname`, `Forename`, `Team`, `Position`, `Games Played`, `Games Started`, `Minutes Played`, `Goals`, `Assists`, `Shots`, `Shots on goal`, `Yellow cards`, `Red cards`, `Team goals scored`, `Team goals conceded`, `Next opposition`, `Next fixture date`, `Team last 5 matches`, `Team last 5 win percent`, `Opposition last 5 matches`, `Opposition last 5 win percent`, `Social Media Score`, `Minutes per goal`, `Minutes per assist`, `Chance of scoring`, `Chance of assisting`, `Chance of conceding a goal`, `Chance of being carded`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (last_name, first_name, team_name, position, games_played, games_started, mins_played, goals, assists, shots_on_goal, shots, yellows, reds, teamGoalsScored, teamGoalsConceded, nextGameOpposition, nextGameDate, teamLast5Games, teamWinPercentage, oppLast5Games,oppWinPercentage,socialMediaScore, minsPerGoal, minsPerAssist, scoringChance, assistChance, concedingChance, cardedChance))
            conn.commit()
        else:
            pass #if player has no team (due to not being in the premier league anymore or simply a technical issue) ignore them and move on to next player
        print(forename + " " + surname + ", " + team_name) #print what player has been analysed for debugging purposes

    print('Finished page ' + str(i)) #print page number when whole page has been fetched. Useful for debugging purposes

cursor.close()
conn.close() #close DB connection