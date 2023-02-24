import time, threading
from tictactoe import playGame
from prettytable import PrettyTable
from board import Board
from constants import isAllowedToPrint



class SimThread(threading.Thread):
    def __init__(self, threadID, total_simultions, playerOne, playerTwo, boardSize, three_d, 
                 printStatusPeriodically=True, printTimeEestimation=True, simsBetweenStatusPrints=100, simsBeforeTimeEstimation=10):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.total_simultions = total_simultions
        self.playerOne = playerOne
        self.playerTwo = playerTwo

        #print settings
            #after every simsBetweenStatusPrints the thread will print how many sims to go, if printStatusPeriodically == true
        self.printStatusPeriodically = printStatusPeriodically
        self.simsBetweenStatusPrints = simsBetweenStatusPrints

            #if printTimeEestimation == true, thread will extrapolate remaining time after simsBeforeTimeEstimation simulations
        self.printTimeEstimation = printTimeEestimation
        self.simsBeforeTimeEstimation = simsBeforeTimeEstimation

        self.afterDecimals = 2

        #board settings
        self.boardSize = boardSize
        self.three_d = three_d

        #data about the similations done
        self.draws = 0
        self.playerOneWins = 0
        self.playerTwoWins = 0

        self.estimatedTime = 0


    def run(self):
        print("Thread #{0} started".format(self.threadID))
        startedSim = time.time()

        self.simulateGames()

        endedSim = time.time()
        total_time_taken = endedSim - startedSim
        print("Thread #{0} : Finished Simulations. Estimated time : {1}s, time taken : {2}s. Absolute estimation error : {3}s"
              .format(self.threadID, 
                      round(self.estimatedTime, self.afterDecimals), 
                      round(total_time_taken, self.afterDecimals),
                      round(total_time_taken - self.estimatedTime, self.afterDecimals)
                      ))
        

    def simulateGames(self):
        start = time.time()
        statusPrintCounter = 0
        for i in range(self.total_simultions):
            # simulate game adn reste board
            score = playGame(self.playerOne, self.playerTwo, boardsize=self.boardSize, threed=self.three_d)

            
            #time caption and estimation
            if (i == self.simsBeforeTimeEstimation and self.printTimeEstimation):
                end = time.time()
                time_checkpoint_time = end - start

                remainingTime = self.total_simultions / self.simsBeforeTimeEstimation * time_checkpoint_time
                remainingTimeInMin = remainingTime / 60
                self.estimatedTime = time_checkpoint_time + remainingTime

                print ("Thread #{0} : Time needed for {1} simulations : {2}s. Extrapolated remaining time : {3}s == {4}min".
                        format(self.threadID,
                                self.simsBeforeTimeEstimation + 1, 
                                round(time_checkpoint_time, self.afterDecimals), 
                                round(remainingTime, self.afterDecimals),
                                round(remainingTimeInMin, self.afterDecimals)
                                ))
            
            if (statusPrintCounter == self.simsBetweenStatusPrints and self.printStatusPeriodically):
                print("Thread #{0} : {1} Simulations complete. {2} to go.".format(self.threadID, i, self.total_simultions - i))
                statusPrintCounter = 0

            #update scores
            if score == 1:
                self.playerOneWins += 1
            if score == -1:
                self.playerTwoWins += 1
            if score == 0:
                self.draws += 1
            statusPrintCounter += 1


def simulate(amountThreads, amountSimulations, playerOne, playerTwo, boardSize, threed):
    threads = []
    simulationsPerThread = int(amountSimulations / amountThreads)
    for threadid in range(amountThreads):
        thread = SimThread(threadID = threadid,
                            total_simultions= simulationsPerThread,
                            playerOne=playerOne,
                            playerTwo=playerTwo,
                            boardSize=boardSize,
                            three_d=threed,
                            printStatusPeriodically=isAllowedToPrint(message_verbosity=2, msgWhenSimulating=True),
                            printTimeEestimation=isAllowedToPrint(message_verbosity=1, msgWhenSimulating=True),
                            simsBetweenStatusPrints=int(0.2*simulationsPerThread),
                            simsBeforeTimeEstimation= int(0.1*simulationsPerThread))
        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    overAllstats = [amountSimulations, 0,0,0] #draws, wins player one, wins player two
    for thread in threads:
        overAllstats[1] += thread.draws
        overAllstats[2] += thread.playerOneWins
        overAllstats[3] += thread.playerTwoWins

    table = PrettyTable()
    table.field_names = ["Total Amount", "Draws", "Wins : {0}".format(playerOne.getUniqueName()), "Wins : {0}".format(playerTwo.getUniqueName())]
    table.add_row(overAllstats)
    print(table)



