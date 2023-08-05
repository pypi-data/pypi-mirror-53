class Update:
    def __init__(self,node):
        self.node = node
        self.blackboard_pub = node.new_pub("/blackboard","json")
        self.whiteboard_pub = node.new_pub("/whiteboard","json")

    def blackboard(self, social_primtive,input_name, intensity, robot = "pepper"):
        data = {"primitive":social_primtive, "input":{input_name:intensity}, "robot":robot}
        self.blackboard_pub.publish(data)

    def whiteboard(self, sensory_primtive,value,robot = "pepper"):
        data = {"primitive":sensory_primtive, "input":value, "robot":robot}
        self.whiteboard_pub.publish(data)
