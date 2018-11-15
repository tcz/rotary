from phue import Bridge

class RomanticLights:
    BRIDGE_IP = '192.168.1.91'

    def __init__(self, logger):
        self.bridge = Bridge(RomanticLights.BRIDGE_IP)
        self.logger = logger

    def respond_to(self, command_text):
        if command_text not in ('romantic lights', 'romantic mood'):
            return

        for light in self.bridge.lights:
            if '[R]' not in light.name:
                self.logger.info('Turning off light ' + light.name)
                light.on = False
            else:
                self.logger.info('Turning on ' + light.name)
                light.on = True
                light.transitiontime = 10
                light.brightness = 250
                light.hue = 5215
                light.saturation = 221


# Initial setup
if __name__ == "__main__":
    print "Setting up Hue"
    raw_input("Press the button on the bridge and then press enter right after.")
    bridge = Bridge(RomanticLights.BRIDGE_IP)
    bridge.connect()
    print "Bridge connected. Lights:"

    for light in bridge.lights:
        print ' - ' + light.name, light.brightness, light.hue, light.saturation
