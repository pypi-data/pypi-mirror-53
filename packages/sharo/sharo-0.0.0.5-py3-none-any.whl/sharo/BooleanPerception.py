import sharo
import time
class BooleanPerception:
    def __init__(self,node, social_primtive, input_name, detected_deadline = 1, non_detected_deadline = 3, robot = "pepper"):
        self.node = node
        self.update = sharo.Update(node)
        self.n_detected = 0
        self.non_detected = 0
        self.start_detection = 0
        self.start_alone = 0
        self.detected_msg_sended = False
        self.non_detected_msg_sended = False
        self.social_primtive = social_primtive
        self.input_name = input_name
        self.detected_deadline = detected_deadline
        self.non_detected_deadline = non_detected_deadline
        self.robot = robot

    def primitive_detected(self):
        self.n_detected = self.n_detected + 1
        self.non_detected = 0
        if self.n_detected == 1:
            self.start_detection = time.time()
        if self.n_detected > self.detected_deadline:
            end = time.time()
            time_detected = end - self.start_detection
            if time_detected >  self.detected_deadline and self.detected_msg_sended == False:
                self.update.blackboard(self.social_primtive,self.input_name, 1, self.robot)
                self.detected_msg_sended = True
                self.non_detected_msg_sended = False
                print (self.social_primtive + " detected")
                self.non_detected = 0

    def primitive_non_detected(self):
        self.non_detected = self.non_detected + 1
        self.n_detected = 0
        if self.non_detected == 1:
            self.start_alone = time.time()
        if self.non_detected > 1:
            end = time.time()
            time_non_detected = end - self.start_alone
            if time_non_detected > 2 and self.non_detected_msg_sended == False:
                self.update.blackboard(self.social_primtive,self.input_name, 0, self.robot)
                self.non_detected_msg_sended = True
                self.detected_msg_sended = False
                print (self.social_primtive + " non detected")
                self.n_detected = 0

