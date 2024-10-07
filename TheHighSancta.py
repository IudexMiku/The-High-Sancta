from math import comb

lossChance = 0.5

initialCounterlight = 100
counterlight = initialCounterlight
counterlightLossNormal = 5
counterlightLossSpecial = 1
dividingCounterlightPoint = 65
dividingViolantSkyPoint = (counterlight - dividingCounterlightPoint) / counterlightLossNormal
costPerLayer = 2.5

impressionsBaseGain = 850
impressionsVSMult = 100
impressionsScaling = 1250

defaultGain = 12.5
alternateGain = 12.6
alternateGainVSMin = 5
alternateGainVSMax = 8
alternateGainCards = 1
alternateGainPossibleCards = 9
handSize = 3

profit = 0
impressions = 0
actionsTaken = 2

data = []

def getExpectedValue(column, oddsColumn=3, row=0):
    if row >= len(data) - 1:
        return data[row][column]
    
    odds = data[row][oddsColumn]
    expectedValue = (1 - odds) * data[row][column] + odds * getExpectedValue(column, oddsColumn, row+1)
    return expectedValue
    
def getOdds(violantSky):
    if lossChance == 0:
        return counterlight
    if violantSky <= (dividingViolantSkyPoint / lossChance):
        return initialCounterlight - lossChance * counterlightLossNormal * violantSky
    else:
        return dividingCounterlightPoint + dividingViolantSkyPoint - lossChance * counterlightLossSpecial * violantSky

print(f'sky\tprofit\tacts\tprogression odds')
for violantSky in range(1, 13):
    #odds
    if violantSky != 1:
        counterlight = getOdds(violantSky)
    
    #profit
    if alternateGainVSMin <= violantSky and violantSky <= alternateGainVSMax:
        altGainOdds = (comb(alternateGainPossibleCards, handSize) - comb(alternateGainPossibleCards - alternateGainCards, handSize)) / comb(alternateGainPossibleCards, handSize)
        echoGain = defaultGain * (1 - altGainOdds) + alternateGain * altGainOdds - costPerLayer
    else:
        echoGain = defaultGain - costPerLayer
    #impressions
    impressions += impressionsBaseGain + impressionsVSMult * violantSky
    profit += echoGain + defaultGain * (impressions // impressionsScaling)
    impressions %= impressionsScaling
    
    #actions
    actionsTaken += 2
    
    print(f'{violantSky}\t\t{round(profit, 1)}\t\t{actionsTaken}\t\t{counterlight/100}')
    data.append([violantSky, profit, actionsTaken, counterlight/100])

#EPA calculation
print(f'Expected {round(getExpectedValue(1), 4)} echoes over {round(getExpectedValue(2), 4)} actions => {round(getExpectedValue(1) / getExpectedValue(2), 4)} EPA')

#Wiki table
print("""{| class="mw-collapsible mw-collapsed article-table"
!{{IL|Towards a Violant Sky|Appearance=Sky}}
!{{e}} Payout
!Actions
!Probability
|-""")
for row in data:
    for element in row:
        print(f'|{round(element, 2)}')
    print(f'|-')
print('|}')

