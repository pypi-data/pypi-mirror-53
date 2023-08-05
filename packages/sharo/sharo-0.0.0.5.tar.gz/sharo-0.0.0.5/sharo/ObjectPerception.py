import sharo
import time
class ObjectPerception:
    def __init__(self,node, object_list, detected_deadline = 1, non_detected_deadline = 3, robot = "pepper"):
        self.node = node
        self.update = sharo.Update(node)
        self.detected = []
        self.non_detected = []
        self.start_detection = []
        self.start_alone = []
        self.dectected_flag = []
        self.object_list = object_list

        for i in range(len(object_list)):
            self.detected.append(0)
            self.non_detected.append(0) 
            self.start_detection.append(0)
            self.start_alone.append(0) 
            self.dectected_flag.append(False)
        
        self.social_primtive = "object"
        self.detected_deadline = detected_deadline
        self.non_detected_deadline = non_detected_deadline
        self.robot = robot
        
    def manage_objects(self, list_index):

        for i in range(len(self.object_list)):
            if i in list_index:
                self.update_object_detected(i)
            else:
                self.update_object_non_detected(i)


    def update_object_detected(self, i):
            self.detected[i] = self.detected[i] + 1
            self.non_detected[i] = 0
            if self.detected[i] == 1:
                self.start_detection[i] = time.time()
            if self.detected[i] > 1:
                end = time.time()
                time_detected = end - self.start_detection[i]
                if time_detected > self.detected_deadline and self.dectected_flag[i] == False:
                    self.update.blackboard(self.social_primtive,self.object_list[i], 1, self.robot)
                    self.dectected_flag[i] = True
                    print (self.social_primtive + " <" + str(self.object_list[i]) + "> detected")
        

                    self.non_detected[i] = 0


    def update_object_non_detected(self, i):
        self.non_detected[i] = self.non_detected[i] + 1
        self.detected[i] = 0
        if self.non_detected[i] == 1:
            self.start_alone[i] = time.time()
        if self.non_detected[i] > 1:
            end = time.time()
            time_non_detected = end - self.start_alone[i]
            if time_non_detected > 2 and self.dectected_flag[i] == True:
                self.update.blackboard(self.social_primtive,self.object_list[i], 0, self.robot)
                self.dectected_flag[i] = False
                print (self.social_primtive + " <" + str(self.object_list[i]) + "> non detected")
                self.detected[i] = 0