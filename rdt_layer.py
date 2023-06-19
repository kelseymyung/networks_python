from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    maxTime = 2                                         # timeout variable / max iteration count before retransmit
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.dataLength = 0
        self.dataReceived = ''
        self.currentIteration = 0
        self.inputIndex = -1
        self.unackedPacketsReceive = []
        self.unackedPacketsSent = {}
        self.charReceived = 0
        self.availableWindow = 15   # available window size
        self.prevAck = 0
        self.timeoutIteration = 0       # holds iteration for next timeout
        self.countSegmentTimeouts = 0
        # Add items as needed

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data
        self.dataLength = len(data)

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...
        return self.dataReceived

        # ############################################################################################################ #

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processReceiveAndSendRespond()   # flipped these two
        self.processSend()                      # flipped these two

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # ############################################################################################################ #

        # identifies client
        if self.dataToSend != "":

            # handle timeout, resend all unacked packets
            if self.currentIteration == self.timeoutIteration:
                self.countSegmentTimeouts += 1
                for key in self.unackedPacketsSent:
                    segment = self.unackedPacketsSent[key]
                    print("Sending segment: ", segment.to_string())

                    # Use the unreliable sendChannel to send the segment
                    self.sendChannel.send(segment)
                    self.timeoutIteration = self.currentIteration + self.maxTime

            print(f'Length of Receive Unacked Packets List: {len(self.unackedPacketsReceive)}')

            # if received ack from server indicates error with previous sent packet
            if self.inputIndex > self.prevAck:
                self.inputIndex = self.prevAck - 1
                self.availableWindow = self.FLOW_CONTROL_WIN_SIZE


            while self.availableWindow > 0:

                # if full data size is able to be used
                if self.availableWindow >= self.DATA_LENGTH:

                    # if inputIndex has not reached end of dataToSend
                    if self.inputIndex < (self.dataLength - 1):
                        segmentSend = Segment()
                        self.inputIndex += 1
                        seqnum = self.inputIndex
                        data = self.dataToSend[self.inputIndex:self.inputIndex + self.DATA_LENGTH]

                        # Display sending segment
                        segmentSend.setData(seqnum,data)
                        print("Sending segment: ", segmentSend.to_string())
                        self.availableWindow = self.availableWindow - len(segmentSend.payload)

                        # Use the unreliable sendChannel to send the segment
                        self.sendChannel.send(segmentSend)

                        self.unackedPacketsSent[segmentSend.seqnum] = segmentSend

                        # update variables
                        self.inputIndex = self.inputIndex + (self.DATA_LENGTH - 1)

                    else:
                        break

                # if partial data segment must be sent
                else:

                    # if inputIndex has not reached end of dataToSend
                    if self.inputIndex < (self.dataLength - 1):
                        segmentSend = Segment()
                        self.inputIndex += 1
                        seqnum = self.inputIndex
                        data = self.dataToSend[self.inputIndex:self.inputIndex + self.availableWindow]

                        # Display sending segment
                        segmentSend.setData(seqnum,data)
                        print("Sending segment: ", segmentSend.to_string())
                        self.availableWindow = self.availableWindow - len(segmentSend.payload)

                        # Use the unreliable sendChannel to send the segment
                        self.sendChannel.send(segmentSend)

                        self.unackedPacketsSent[segmentSend.seqnum] = segmentSend

                        # update variables
                        self.inputIndex = self.inputIndex + (len(segmentSend.payload) - 1)

                    else:
                        break

            # set timeout
            self.timeoutIteration = self.currentIteration + self.maxTime
            print(f'Length of Sent Unacked Packets List: {len(self.unackedPacketsSent)}')

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()     # Segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #

        # identifies client
        if self.dataToSend != "":

            # if ack received, stop timer
            if len(listIncomingSegments) != 0:
                self.timeoutIteration = self.currentIteration - 1

                # reopens window based on ack
                for index in range(len(listIncomingSegments)):
                    currentAck = listIncomingSegments[index]
                    self.availableWindow = self.availableWindow + (currentAck.acknum - self.prevAck - 1)

                    # unackedPacketsReceive acts as ack log for client
                    self.unackedPacketsReceive.append(currentAck)

                    # deletes packets from unacked list that are now acked
                    for num in range(currentAck.acknum):
                        if num in self.unackedPacketsSent:
                            del self.unackedPacketsSent[num]

                    self.prevAck = currentAck.acknum



        # identifies server
        if self.dataToSend == "":
            error_found = False

            # receive incoming packets
            self.unackedPacketsReceive = listIncomingSegments

            iterations = len(self.unackedPacketsReceive)
            for val in range(iterations):
                currentSegment = self.unackedPacketsReceive[0]
                # checks if first packet in list has correct expected ack number
                # if out of order packet, discard packet
                if currentSegment.seqnum != self.prevAck:
                    del self.unackedPacketsReceive[0]
                    error_found = True

                # if packet order is correct, verify correct checksum
                else:
                    # checksum is correct, add packet data to received data, delete packet, update variables
                    if currentSegment.checkChecksum():
                        add_str = currentSegment.payload
                        self.dataReceived = self.dataReceived + add_str
                        self.charReceived = self.charReceived + len(currentSegment.payload)
                        del self.unackedPacketsReceive[0]
                        self.prevAck = self.prevAck + len(currentSegment.payload)

                    # if checksum is incorrect, discard packet
                    else:
                        del self.unackedPacketsReceive[0]
                        error_found = True

            if error_found == False:
                acknum = self.charReceived + 1
            else:
                acknum = self.charReceived

            # Display response segment
            segmentAck.setAck(acknum)
            print("Sending ack: ", segmentAck.to_string())

            # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.send(segmentAck)

            print(f'Length of Receive Unacked Packets List: {len(self.unackedPacketsReceive)}')


        # ############################################################################################################ #


        # ############################################################################################################ #

# citations:
# https://stackoverflow.com/questions/8995611/removing-multiple-keys-from-a-dictionary-safely
# https://www.geeksforgeeks.org/python-ways-to-remove-a-key-from-dictionary/
# https://www.baeldung.com/cs/networking-go-back-n-protocol
