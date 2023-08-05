# Motion Master Bindings

This package contains Python bindings for the Synapticon Motion Master, a lightweight
master controller for EtherCAT devices.

Motion Master v3.x is supported. This package does not support previous versions.

## Installation

Using virtualenv or Python3's venv is recommended.

To install from PyPi, run

    $ pip install motion-master-bindings

## Documentation

The Motion Master branch of the documentation department is currently working
on something better, but here's an example to get you started.

    from motion_master_bindings.motion_master import MotionMaster
    from motion_master_proto.motion_master_pb2 import MotionMasterMessage

    mm = MotionMaster('127.0.0.1')
    mm.connect()
    mm.get_dealer_subject().subscribe(
        lambda message: print("Message: {}".format(message)))

    message = MotionMasterMessage()
    message.request.get_system_version.SetInParent()
    mm.send_message(message)

You should get a response printed from the DEALER subject:

    Message: [b'\xb2\x06\x12\xb2\x06\x0f\n\r3.0.0-alpha.1']

