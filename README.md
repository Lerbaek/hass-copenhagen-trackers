# Copenhagen Trackers Integration for Home Assistant

[![HACS Action](https://github.com/lerbaek/hass-copenhagen-trackers/actions/workflows/hacs.yaml/badge.svg)](https://github.com/lerbaek/hass-copenhagen-trackers/actions/workflows/hacs.yaml)
[![Validate with hassfest](https://github.com/lerbaek/hass-copenhagen-trackers/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/lerbaek/hass-copenhagen-trackers/actions/workflows/hassfest.yaml)

Copenhagen Trackers custom integration for Home Assistant allows you to seamlessly integrate your Copenhagen Trackers devices with Home Assistant, providing real-time monitoring.

## Features

- **Sensor Integration**: Monitor various sensor data such as location, geolocation, battery percentage, signal strength, and profile name.
- **Binary Sensor Integration**: Check device update capabilities and recommendations.
- **Switch Integration**: Force device updates with a simple switch.

## Installation

### HACS (Home Assistant Community Store)

1. Ensure you have [HACS](https://hacs.xyz/) installed.
2. Go to HACS > Integrations.
3. Click on the three dots in the top right corner and select "Custom repositories".
4. Add the repository URL: `https://github.com/lerbaek/hass-copenhagen-trackers` and select the category "Integration".
5. Find "Copenhagen Trackers" in the list and click "Install".

### Manual Installation

1. Download the `custom_components` folder from this repository.
2. Copy the `copenhagen_trackers` directory into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## Configuration

1. Go to Home Assistant > Configuration > Integrations.
2. Click on "Add Integration" and search for "Copenhagen Trackers".
3. Follow the setup instructions to enter your Copenhagen Trackers account credentials.

## Usage

Once configured, your Copenhagen Trackers devices will be available in Home Assistant. You can view sensor data, check for updates, and force updates directly from the Home Assistant interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/lerbaek/hass-copenhagen-trackers).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For any issues or questions, please open an issue on the [GitHub Issue Tracker](https://github.com/lerbaek/hass-copenhagen-trackers/issues).

## Acknowledgements

- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [Copenhagen Trackers](https://cphtrackers.com)