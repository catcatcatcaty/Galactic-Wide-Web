<a name="top"></a>
<div align="center">
  <img src="resources/gww-banner.png" width="800">
</div>
<h1 align="center">Galactic Wide Web: Fluxer Port</h1>
<p align="center">
    <a href="https://fluxer.gg/m50i6kcZ">
      <img alt="Support Server" src="https://img.shields.io/discord/1212722266392109088?style=for-the-badge&logo=discord&label=Support%20Server">
    </a>
	<a href="https://fluxer.gg/m50i6kcZ">
		<img alt="Servers" src="https://img.shields.io/badge/servers-5+-brightgreen?style=for-the-badge">
	</a>
	<a href="https://fluxer.gg/m50i6kcZ">
		<img alt="Visible Users" src="https://img.shields.io/badge/visible users-100+-brightgreen?style=for-the-badge">
	</a>
  <br>
  <a href="LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/Stonemercy/Galactic-Wide-Web?style=for-the-badge">
	</a>
	<img alt="Commits made" src="https://img.shields.io/github/last-commit/catcatcatcaty/Galactic-Wide-Web?style=for-the-badge">
  <img alt="Code Size" src="https://img.shields.io/github/languages/code-size/catcatcatcaty/Galactic-Wide-Web?style=for-the-badge">
  <img alt="Code Format" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge">
  <br>
  <a href="https://ko-fi.com/R6R51OSRX8">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg">
  </a>
</p>

<p align="center">
  Galactic Wide Web: Fluxer Port is a Fluxer bot for Helldivers 2 that provides real-time information on the Galactic War.
  <br>
  Disclaimer: This is a fork of the original Galactic Wide Web bot by StoneMercy. It is not feature complete and bugs are to be expected and reliability is not guaranteed. You have been warned!
  <br>
  It pulls live data from the official Helldivers 2 API and the Steam API, and keeps an auto-updating dashboard refreshed every 15 minutes with a strategic overview of the current war effort.<br><br>
  The bot includes commands, and embedded content. All interactions take place in text channels.
  <br>
  Server administrators (or those with Manage Server permissions) can configure which channels are used for dashboards and announcements.
  <br>
  The bot has a variety of Helldivers 2 data, including:
</p>
<p align="center">
    - Personal Orders - <b>EXCLUSIVE!</b> - UNAVAILABLE on the Fluxer port due to private API usage<br>
    - DSS Vote counts - <b>EXCLUSIVE!</b> - UNAVAILABLE on the Fluxer port due to private API usage<br>
    - Major Orders<br>
    - Control Centre (campaigns) - NYI on the Fluxer port<br>
    - Superstore - UNAVAILABLE on the Fluxer port due to private API usage<br>
    - Warbonds - UNAVAILABLE on the Fluxer port due to private API usage<br>
    - Dispatches<br>
    - Global Events<br>
    - DSS movements and Tactical Action updates<br>
    - Planetary Region changes<br>
    - Campaign wins and losses<br>
    - and Steam patch notes.<br>
    <br>
    The bot also supports multilingual output, currently offering English, French, German, Italian, Portuguese (BR),
    <br>
  Built using a butchered version of Disnake (ported to Fluxer), it stores settings in PostgreSQL and uses Pillow and opencv to generate maps.
</p>

## Quick Navigation
- [Inviting the Bot](#inviting-the-galactic-wide-web)
- [Examples](#examples) (to be updated)

| Here are the bots commands |   |   |
|---|---|---|
| [`/check_missing_translations`](#check_missing_translations-language_to_check-fr) | [`/community_servers`](#community_servers) | [`/control_centre`](#control_centre) |
| [`/dispatches`](#dispatches) | [`/dss`](#dss) | [`/dss_votes`](#dss_votes) |
| [`/global_events`](#global_events) | [`/major_order`](#major_order) | [`/map`](#map) |
| [`/personal_order`](#personal_order) | [`/planet`](#planet-planet-124-bore-rock) | [`/setup`](#setup) |
| [`/steam`](#steam) | [`/subfaction`](#subfaction) | [`/superstore`](#superstore) |
| [`/warbonds`](#warbonds) | [`/warfront`](#warfront-faction-automaton) | |

- [Support](#support)
- [Contributing](#contributing)

## Inviting the Galactic Wide Web
Want to try out the GWW on your server? [Invite Link](https://web.fluxer.app/oauth2/authorize?client_id=1476519709822349355&scope=bot)

## Examples
### `/check_missing_translations language_to_check: fr`
<img src="resources/readme/check_missing_translations.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/community_servers`
<img src="resources/readme/community_servers.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/control_centre`
<img src="resources/readme/control_centre.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/dispatches`
<img src="resources/readme/dispatches.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/dss`
<img src="resources/readme/dss.png">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/dss_votes`
<img src="resources/readme/dss_votes.png">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/global_events`
<img src="resources/readme/global_events.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/help command: check_missing_translations`
<img src="resources/readme/help.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/major_order`
<img src="resources/readme/major_order.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/map`
<img src="resources/readme/map.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/personal_order`
<img src="resources/readme/personal_order.png">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/planet planet: 124-BORE ROCK`
<img src="resources/readme/planet.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/setup`
<img src="resources/readme/setup.png">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/steam`
<img src="resources/readme/steam.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/subfaction`
<img src="resources/readme/subfaction.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/superstore`
<img src="resources/readme/superstore.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/warbonds`
<img src="resources/readme/warbonds.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/warfront faction: Automaton`
<img src="resources/readme/warfront.png">
<p align="right"><a href="#top">Back to Top ↑</a></p>

## Support
Available here: [Fluxer Support Server](https://fluxer.gg/m50i6kcZ)
<p align="right"><a href="#top">Back to Top ↑</a></p>

## Contributing
Contributions are welcome!

To contribute to localization (upstream only):
1. Open an issue with the Language Request template
2. Create a pull request and add a .json file to the [data/languages/](https://github.com/Stonemercy/Galactic-Wide-Web/tree/main/data/languages) folder

or just head to the Fluxer Support Server above
<p align="right"><a href="#top">Back to Top ↑</a></p>
