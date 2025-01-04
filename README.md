# Copenhagen Trackers Integration for Home Assistant

[![HACS Action][hass-action-shield]][hass-action]
[![Validate with hassfest][hassfest-shield]][hassfest]  
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

Copenhagen Trackers custom integration for Home Assistant allows you to seamlessly integrate your Copenhagen Trackers devices with Home Assistant, providing real-time monitoring.

## Features

- **Device Tracker Integration**: Monitor device location and geolocation data
- **Sensor Integration**: Monitor battery percentage, signal strength, and profile name
- **Binary Sensor Integration**: Check device update capabilities and recommendations
- **Switch Integration**: Force device updates with a simple switch

## Installation

### HACS (Home Assistant Community Store)

1. Ensure you have [HACS](https://hacs.xyz/) installed.
2. Go to HACS > Integrations.
3. Click on the three dots in the top right corner and select "Custom repositories".
4. Add the repository URL: `https://github.com/Lerbaek/hass-copenhagen-trackers` and select the category "Integration".
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

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/Lerbaek/hass-copenhagen-trackers).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For any issues or questions, please open an issue on the [GitHub Issue Tracker](https://github.com/Lerbaek/hass-copenhagen-trackers/issues).

## Acknowledgements

- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [Copenhagen Trackers](https://cphtrackers.com)

---

[buymecoffee]: https://www.buymeacoffee.com/Lerbaek
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge
[commits]: https://github.com/Lerbaek/hass-copenhagen-trackers/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40Lerbaek-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge
[releases]: https://github.com/Lerbaek/hass-copenhagen-trackers/releases
[user_profile]: https://github.com/Lerbaek
[hassfest]: https://github.com/Lerbaek/hass-copenhagen-trackers/actions/workflows/hassfest.yml
[hassfest-shield]: https://img.shields.io/github/actions/workflow/status/Lerbaek/hass-copenhagen-trackers/hassfest.yml?style=for-the-badge&label=Validate%20with%20hassfest
[hass-action-shield]: https://img.shields.io/github/actions/workflow/status/Lerbaek/hass-copenhagen-trackers/validate.yml?style=for-the-badge&label=Validate
[hass-action]: https://github.com/Lerbaek/hass-copenhagen-trackers/actions/workflows/validate.yml