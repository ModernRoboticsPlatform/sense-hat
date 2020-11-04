from sense_hat import SenseHat
import redis
from time import sleep
import json
import os

REDIS_HOST = os.getenv('REDIS_HOST', default="redis" )
REDIS_PORT = os.getenv('REDIS_PORT', default=6379 )


#
# orientation
# 
class orientation: 
  def __init__( self, pitch, roll, yaw ):
    self.pitch = pitch
    self.roll = roll
    self.yaw = yaw
  def __str__(self):
    return "pitch: % s, roll: % s, yaw: % s " % (self.pitch, self.roll, self.yaw )
  def __eq__( self, other ):
    if( self.pitch != other.pitch ):
      return False
    if(self.roll != other.roll):
      return False
    if(self.yaw != other.yaw):
      return False
    return True

#
# compass
#
class compass:
  def __init__( self, degrees ):
    self.degrees = degrees
  def __str__(self):
    return "Degrees: % s " % (self.degrees )
  def __eq__( self, other ):
    if( self.degrees != other.degrees ):
      return False
    return True

#
# message
#
class message:
  def __init__(self, type = "", data = {} ):
    self.type = type
    self.data = data 

  def __str__(self):
    return( data.__str__ )

  def __eq__( self, other ):
    if( self.type != other.type ):
      return False
    if( self.data != other.data ):
      return False
    return True


# Setup Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
p = r.pubsub(ignore_subscribe_messages=True)

# Init the sense hat
sense = SenseHat()
sense.clear()

# Setup loop
old_orientation = message("ORIENTATION", orientation(0,0,0) )
old_acceleration = message("ACCELERATION", orientation(0,0,0) )
old_compass = message( "COMPASS", compass( 0 ) )


print( "Starting:" )
while True:
  sense.set_imu_config( False, True, True )
  o = sense.get_orientation_degrees()
  new_orientation = message( "ORIENTATION", orientation( round(  o["pitch"], 1 ), round( o["roll"], 1 ), round( o["yaw"], 1 ) ) )

  if( new_orientation != old_orientation ):
    r.publish('telemetry', json.dumps( new_orientation, default=lambda o: o.__dict__ ) )

  old_orientation = new_orientation


  o = sense.get_accelerometer_raw()
  new_acceleration = message( "ACCELERATION", orientation( round(  o["x"], 2 ), round( o["y"], 2 ), round( o["z"], 2 ) ) )

  if( new_acceleration != old_acceleration ):
    r.publish('telemetry', json.dumps( new_acceleration, default=lambda o: o.__dict__ ) )

  old_acceleration = new_acceleration


#  sense.set_imu_config(True, False, False) 
#  new_compass = message( "COMPASS", compass( sense.get_compass()) )
#  if( new_compass != old_compass ):
#    r.publish('telemetry', json.dumps( new_compass, default=lambda o: o.__dict__ ) )

#  old_compass = new_compass


