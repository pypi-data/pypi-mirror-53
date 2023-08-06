import sys, time
sys.path.append('../../api/python')
import motion_master_pb2
import zmq
import re


class SDOConfigParser:
    """
    SDO Config parser. File format is <index>,<subindex>,<value> as CSV
    """

    def __init__(self, file_name):
        """
        Initialized config parser.
        :param file_name: file name of CSV config file
        :type file_name: string
        """
        self.__file_name = file_name
        self.__file_handler = self._open_file()
        self.__re_csv_line = r'(-?0x[\da-fA-F]+|-?\d+\.?\d*),?'
        self.__re_comment = r'#.+'
        self.__re_compile = re.compile(self.__re_csv_line)


    def _open_file(self):
        """
        Tries to open the file.
        :return: file handle, or None
        :rtype: file handle
        """
        try:
            return open(self.__file_name, 'r')
        except IOError:
            pass

    def _close_file(self):
        self.__file_handler.close()

    def _remove_comments(self, line):
        return re.sub(self.__re_comment, '', line)

    def _parse_line(self, line):
        return self.__re_compile.findall(line)

    @staticmethod
    def _convert_str_to_number(value):
        """
        Convert string to float or to int
        :param value: number as string
        :type value: string
        :return: String as number
        :rtype: float or int
        """
        if '.' in value:
            return float(value)
        if 'x' in value:
            if value[0] == '-':
                return int(value[1:], 16) * -1
            return int(value, 16)
        return int(value)


    def _restructure_array(self, array):
        """
        Restructure array entry from
        [<index1>,<subindex1>,<value1_node1>,<value1_node2>,...]
        to
        [<index1>,<subindex1>,<value1>],[<index2>,<subindex2>,<value2>],...
        :param array: Array with input like csv file
        :type array: list of list
        :return: new arranged list
        :rtype: list of list
        """
        slave_count = len(array[0])-2
        slave_config_values = [[] * slave_count]

        for line in array:
            for node in range(slave_count):
                slave_config_values[node].append([int(line[0], 16), int(line[1]), self._convert_str_to_number(line[node+2]) ] )

        return slave_config_values

    def parse_file(self, axis_id):
        """
        Parse file and return values as array.
        :param axis_id: Axis ID
        :type axis_id:  uint
        :return: List with values for <axis_id>
        :rtype: list of tuple
        """
        sdo_array = []
        if self.__file_handler:

            for line in self.__file_handler:
                res = self._remove_comments(line)
                res = self._parse_line(res)
                if res and len(res) >= 3:
                    sdo_array.append(res)

            self._close_file()

            sdo_array = self._restructure_array(sdo_array)

            return sdo_array[axis_id]
        return sdo_array


class CommandMaster:
    def __init__(self, ip='127.0.0.1', port_command=62524, port_subscriber=62525):
        self.ip = ip
        self.port_command = port_command
        self.port_subscriber = port_subscriber
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect('tcp://'+self.ip+':'+str(self.port_command))
        self.heartbeat = False
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self.subscriber.setsockopt(zmq.CONFLATE, 1)
        self.subscriber.connect('tcp://'+self.ip+':'+str(self.port_subscriber))
        self.motion_command = motion_master_pb2.Command()

    def send_command(self, command):
        self.socket.send(command.SerializeToString())

    def send_motion_command(self):
        self.send_command(self.motion_command)

    def set_heartbeat(self):
        command = motion_master_pb2.Command()
        command.heartbeat.CopyFrom(motion_master_pb2.Heartbeat())
        self.send_command(command)

    def start_heartbeat(self, n=5):
        self.heartbeat = True
        try:
            while self.heartbeat:
                self.set_heartbeat()
                time.sleep(n)
        except KeyboardInterrupt:
            print()
            return

    def stop_heartbeat(self):
        self.heartbeat = False

    def scan_devices(self):
        command = motion_master_pb2.Command()
        command.devices.CopyFrom(motion_master_pb2.Devices())
        self.send_command(command)

        status = motion_master_pb2.Status()
        timeout = 1000
        while not status.HasField('devices') and timeout >= 0:
            data = self.socket.recv()
            status.ParseFromString(data)
            timeout -= 1
        if status.HasField('devices') :

            return len(status.devices.device)
        else :
            return 0

    def add_devices(self, number):
        command = motion_master_pb2.Command()
        self.multi_axis = self.motion_command.multi_axis
        for id in range(number):
            device = command.devices.device.add()
            device.device_id = id
            axis = self.multi_axis.single_axis.add()
            axis.device_id = id
        self.send_command(command)

    def get_axis_number(self):
        return len(self.multi_axis.single_axis)

    def enable_position_controller(self, id, filter):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.POSITION
        command.controller_operation.enabled = True
        command.controller_operation.filter = filter
        self.send_command(command)

    def disable_position_controller(self, id):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.POSITION
        command.controller_operation.enabled = False
        self.send_command(command)

    def enable_velocity_controller(self, id, filter):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.VELOCITY
        command.controller_operation.enabled = True
        command.controller_operation.filter = filter
        self.send_command(command)

    def disable_velocity_controller(self, id):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.VELOCITY
        command.controller_operation.enabled = False
        self.send_command(command)

    def enable_torque_controller(self, id, filter):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.TORQUE
        command.controller_operation.enabled = True
        command.controller_operation.filter = filter
        self.send_command(command)

    def disable_torque_controller(self, id):
        command = motion_master_pb2.Command()
        command.controller_operation.device_id = id
        command.controller_operation.controller = motion_master_pb2.TORQUE
        command.controller_operation.enabled = False
        self.send_command(command)

    def send_single_axis_torque_command(self, id, target):
        command = motion_master_pb2.Command()
        command.single_axis.device_id = id
        command.single_axis.controller = motion_master_pb2.TORQUE
        command.single_axis.target = target
        self.send_command(command)

    def set_torque(self, id, target):
        self.multi_axis.single_axis[id].target = target
        self.multi_axis.single_axis[id].controller = motion_master_pb2.TORQUE

    def set_position(self, id, target):
        self.multi_axis.single_axis[id].target = target
        self.multi_axis.single_axis[id].controller = motion_master_pb2.POSITION

    def set_velocity(self, id, target):
        self.multi_axis.single_axis[id].target = target
        self.multi_axis.single_axis[id].controller = motion_master_pb2.VELOCITY

    def set_ramp_profile_position(self, id, velocity, acceleration, deceleration, target, sustain):
        command = motion_master_pb2.Command()
        command.single_axis_profile.device_id = id
        command.single_axis_profile.controller = motion_master_pb2.POSITION
        command.single_axis_profile.type = motion_master_pb2.SingleAxisProfile.RAMP
        command.single_axis_profile.profile_velocity = velocity
        command.single_axis_profile.profile_acceleration = acceleration  
        command.single_axis_profile.profile_deceleration = deceleration     
        command.single_axis_profile.target = target
        command.single_axis_profile.sustain_time = sustain
        self.send_command(command)

    def set_ramp_profile_velocity(self, id, acceleration, deceleration, target, sustain):
        command = motion_master_pb2.Command()
        command.single_axis_profile.device_id = id
        command.single_axis_profile.controller = motion_master_pb2.VELOCITY
        command.single_axis_profile.type = motion_master_pb2.SingleAxisProfile.RAMP
        command.single_axis_profile.profile_acceleration = acceleration
        command.single_axis_profile.profile_deceleration = deceleration
        command.single_axis_profile.target = target
        command.single_axis_profile.sustain_time = sustain
        self.send_command(command)

    def set_ramp_profile_torque(self, id, slope, target, sustain):
        command = motion_master_pb2.Command()
        command.single_axis_profile.device_id = id
        command.single_axis_profile.controller = motion_master_pb2.TORQUE
        command.single_axis_profile.type = motion_master_pb2.SingleAxisProfile.RAMP
        command.single_axis_profile.torque_slope = slope
        command.single_axis_profile.target = target
        command.single_axis_profile.sustain_time = sustain
        self.send_command(command)

    def set_torque_offset(self, id, target):
        self.multi_axis.single_axis[id].torque_offset = target

    def set_velocity_offset(self, id, target):
        self.multi_axis.single_axis[id].velocity_offset = target

    def do_step(self, id, target, sustain=2000):
        command = motion_master_pb2.Command()
        command.single_axis_step_response.device_id = id
        command.single_axis_step_response.controller = motion_master_pb2.POSITION
        command.single_axis_step_response.type = motion_master_pb2.SingleAxisStepResponse.ADVANCED
        command.single_axis_step_response.target = target
        command.single_axis_step_response.sustain_time = sustain
        self.send_command(command)

    def do_quick_stop(self, id):
        command = motion_master_pb2.Command()
        command.single_axis_quick_stop.device_id = id
        self.send_command(command)

    def reset_fault(self, id):
        command = motion_master_pb2.Command()
        command.reset_fault.device_id = id
        self.send_command(command)

    def get_monitoring(self):
        status = motion_master_pb2.Status()
        timeout = 1000
        while not status.HasField('monitoring') and timeout >= 0:

            data = self.subscriber.recv()

            try: # FIXME: this is a workaround till a proper solution is found
                status.ParseFromString(data)
            except:
                #print("ERROR PARSING STATUS MESSAGE!")
                self.subscriber.close()
                self.subscriber = self.context.socket(zmq.SUB)
                self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
                self.subscriber.setsockopt(zmq.CONFLATE, 1)
                self.subscriber.connect('tcp://'+self.ip+':'+str(self.port_subscriber))

            timeout -= 1
        if status.HasField('monitoring'):
            return status.monitoring
        else:
            return []

    def get_position(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].actual_position
        return None

    def get_secondary_position(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].secondary_position
        return None

    def get_velocity(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].actual_velocity
        return None

    def get_secondary_velocity(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].secondary_velocity
        return None

    def get_torque(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].actual_torque
        return None

    def get_analog_input_1(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].analog_input_1
        return None

    def get_analog_input_2(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].analog_input_2
        return None

    def get_analog_input_3(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].analog_input_3
        return None

    def get_analog_input_4(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].analog_input_4
        return None

    def get_digital_input_1(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].digital_input_1
        return None

    def get_digital_input_2(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].digital_input_2
        return None

    def get_digital_input_3(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].digital_input_3
        return None

    def get_digital_input_4(self, id=0):
        single_axis_feedbacks = self.get_monitoring().single_axis_feedback
        if len(single_axis_feedbacks) > id:
            return single_axis_feedbacks[id].digital_input_4
        return None

    def do_reset_fault(self, id=0):
        command = motion_master_pb2.Command()
        command.reset_fault.device_id = id
        self.send_command(command)

    def do_offset_detection(self, id=0):
        command = motion_master_pb2.Command()
        command.offset_detection.device_id = id
        self.send_command(command)

        #read result
        status = motion_master_pb2.Status()
        timeout = 1000
        while not status.HasField('offset_detection') and timeout >= 0:
            data = self.socket.recv()
            status.ParseFromString(data)
            timeout -= 1
        if status.HasField('offset_detection'):
            return status.offset_detection.offset
        else:
            return None

    def set_parameter(self, id, index, subindex, value):
        command = motion_master_pb2.Command()
        command.configuration.device_id = id
        parameter = command.configuration.parameters.add()
        parameter.index = index
        parameter.subindex = subindex
        parameter.int_value = value #FIXME: motion master now supports int, float and string
        command.configuration.action = motion_master_pb2.Configuration.SET
        self.send_command(command)

    def get_parameter(self, id, index, subindex):
        #send get command
        command = motion_master_pb2.Command()
        command.configuration.device_id = id
        parameter = command.configuration.parameters.add()
        parameter.index = index
        parameter.subindex = subindex
        command.configuration.action = motion_master_pb2.Configuration.GET
        self.send_command(command)

        #read result
        status = motion_master_pb2.Status()
        timeout = 1000
        while not status.HasField('configuration') and timeout >= 0:
            data = self.socket.recv()
            status.ParseFromString(data)
            timeout -= 1
        if status.HasField('configuration') and len(status.configuration.parameters) > 0:
            _val = status.configuration.parameters[0]
            return getattr(_val, _val.WhichOneof('type_value'))
        else:
            return None

    def do_save_config(self, id=0):
        command = motion_master_pb2.Command()
        command.save_configuration.device_id = id
        self.send_command(command)


    def upload_config(self, file_name, id=0):
        parser = SDOConfigParser(file_name)
        config = parser.parse_file(id)

        for index, subindex, value in config:
            self.set_parameter(id, index, subindex, value)

        self.do_save_config(id)
