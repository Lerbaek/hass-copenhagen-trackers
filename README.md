# Copenhagen Trackers Integration for Home Assistant

|Project|Status|Usage|Community|
|---|---|---|---|
|[![releases-shield]][releases]|[![hass-action-shield]][hass-action]|[![hacsbadge]][hacs]|[![buymecoffeebadge]][buymecoffee]|
|[![maintenance-shield]][user_profile]|[![hassfest-shield]][hassfest]|[![stars-shield]][stars]|[![forum-shield]][forum]|
|[![license-shield]](LICENSE)|[![commits-shield]][commits]|[![downloads-shield]][downloads]
||[![Issues][issues-shield]][issues]

Copenhagen Trackers custom integration for Home Assistant allows you to seamlessly integrate your Copenhagen Trackers devices with Home Assistant, providing real-time monitoring.

## Disclaimers

### Affiliation
This project is an independent effort and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Copenhagen Trackers.

### Device Support
This integration has been developed with access to only the [Cobblestone] tracker.  
While it is has been developed with support for the [Gemstone] tracker and the [Gemstone Bike][Gemstone-Bike] tracker, this has not been confirmed.  
If you own these devices and encounter issues, please open an issue on GitHub.  
**And hey, Copenhagen Trackers, if you're reading this, feel free to send over some samples for thorough testing!**

[Cobblestone]: https://cphtrackers.com/products/cobblestone-gps-tracker
[Gemstone]: https://cphtrackers.com/products/gemstone
[Gemstone-Bike]: https://cphtrackers.com/products/gemstone-bike

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
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-brown.svg?style=for-the-badge&logo=buymeacoffee&logoColr
[commits-shield]: https://img.shields.io/github/commit-activity/y/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge&logo=git
[commits]: https://github.com/Lerbaek/hass-copenhagen-trackers/commits/main
[downloads-shield]: https://img.shields.io/github/downloads/lerbaek/hass-copenhagen-trackers/total?style=for-the-badge&label=Downloads
[downloads]: https://github.com/Lerbaek/hass-copenhagen-trackers/releases
[forum-shield]: https://img.shields.io/badge/community-forum-%2303A9F4.svg?style=for-the-badge&logo=homeassistantcommunitystore
[forum]: https://community.home-assistant.io/
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hass-action-shield]: https://img.shields.io/github/actions/workflow/status/Lerbaek/hass-copenhagen-trackers/validate.yml?style=for-the-badge&label=HACS
[hass-action]: https://github.com/Lerbaek/hass-copenhagen-trackers/actions/workflows/validate.yml
[hassfest-shield]: https://img.shields.io/github/actions/workflow/status/Lerbaek/hass-copenhagen-trackers/hassfest.yml?style=for-the-badge&label=Hassfest
[hassfest]: https://github.com/Lerbaek/hass-copenhagen-trackers/actions/workflows/hassfest.yml
[issues-shield]: https://img.shields.io/github/issues/Lerbaek/hass-copenhagen-trackers?style=for-the-badge
[issues]: https://github.com/Lerbaek/hass-copenhagen-trackers/issues
[license-shield]: https://img.shields.io/github/license/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40Lerbaek-blue.svg?style=for-the-badge&logo=github
[releases-shield]: https://img.shields.io/github/release/Lerbaek/hass-copenhagen-trackers.svg?style=for-the-badge&logo=semver
[releases]: https://github.com/Lerbaek/hass-copenhagen-trackers/releases
[stars-shield]: https://img.shields.io/github/stars/Lerbaek/hass-copenhagen-trackers?style=for-the-badge&logo=apachespark&logoColor=yellow
[stars]: https://github.com/Lerbaek/hass-copenhagen-trackers/stargazers
[user_profile]: https://github.com/Lerbaek